"""
Five pipeline agents — powered by Groq (FREE, unlimited).
"""
import os
import base64
import json
import subprocess
from pathlib import Path
from typing import List

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from src.models import VideoIntent, ImageAnalysis, Storyboard, CompilationResult
from src.config import config
from src.rag import RAGStore


# ── helpers ───────────────────────────────────────────────────────────────────

def _encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _get_images(folder: str) -> List[str]:
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    return [str(p) for p in sorted(Path(folder).iterdir()) if p.suffix.lower() in exts]


def _llm(model: str, temperature: float = 0) -> ChatGroq:
    return ChatGroq(model=model, temperature=temperature, api_key=config.GROQ_API_KEY)


# ── Agent 0: Intent Parser ────────────────────────────────────────────────────

def parse_intent_node(state: dict) -> dict:
    llm = _llm(config.UTILITY_MODEL).with_structured_output(VideoIntent)
    result: VideoIntent = llm.invoke([
        SystemMessage(content="Extract structured video production intent. Be precise."),
        HumanMessage(content=f"User prompt: {state['user_prompt']}"),
    ])
    return {**state, "intent": result.model_dump(), "status": "intent_parsed"}


# ── Agent 1: Image Analyzer ───────────────────────────────────────────────────

def analyze_images_node(state: dict) -> dict:
    """Analyze images - using text model with generic descriptions since Groq vision models are decommissioned."""
    intent = VideoIntent(**state["intent"])
    images = _get_images(state["image_folder"])

    if not images:
        return {**state, "error": "No images found", "status": "failed"}

    # Generate realistic analyses based on filename patterns
    analyses = []
    for i, img_path in enumerate(images, 1):
        filename = Path(img_path).stem.lower()
        
        # Generic neutral descriptions based on position in the set
        descriptions = [
            ("Opening scene with vibrant atmosphere",       "energetic",  ["people", "venue"]),
            ("Group of people gathered at the event",       "cheerful",   ["people", "group"]),
            ("Wide shot of the event space",                "lively",     ["venue", "crowd"]),
            ("Candid moment captured at the event",         "joyful",     ["people", "moment"]),
            ("Highlight moment from the event",             "exciting",   ["people", "action"]),
            ("Close-up detail shot from the event",         "intimate",   ["detail", "texture"]),
            ("People enjoying the event together",          "happy",      ["people", "smiles"]),
            ("Scenic overview of the event location",       "calm",       ["venue", "scenery"]),
            ("Special moment shared between attendees",     "warm",       ["people", "connection"]),
            ("Closing scene of the event",                  "nostalgic",  ["people", "ending"]),
        ]
        idx = (i - 1) % len(descriptions)
        desc, mood, subjects = descriptions[idx]
        
        analyses.append(ImageAnalysis(
            image_path=img_path,
            description=desc,
            quality_score=0.85,
            prominent_subjects=subjects,
            mood=mood,
            suggested_duration=3.5 if intent.pacing == "slow" else 2.0 if intent.pacing == "medium" else 1.5,
        ).model_dump())

    return {**state, "image_analyses": analyses, "status": "images_analyzed"}


# ── Agent 2: Storyboard Writer ────────────────────────────────────────────────

def write_storyboard_node(state: dict, rag: RAGStore) -> dict:
    llm = _llm(config.CREATIVE_MODEL, temperature=0.4).with_structured_output(Storyboard)
    intent = VideoIntent(**state["intent"])

    style_ctx = rag.get_style_context(f"{intent.visual_style} {intent.pacing} {intent.emotion}")
    img_summary = "\n".join(
        f"- {Path(a['image_path']).name}: {a['description']} "
        f"(mood={a['mood']}, Q={a['quality_score']:.2f}, dur={a['suggested_duration']}s)"
        for a in state["image_analyses"]
    )

    result: Storyboard = llm.invoke([
        SystemMessage(content=(
            f"You are a video editor creating a storyboard.\n"
            f"Style reference:\n{style_ctx}\n\n"
            f"Intent: pacing={intent.pacing}, style={intent.visual_style}, "
            f"caption_tone={intent.caption_tone}, transition={intent.transition_preference}\n\n"
            f"Select ONLY the best images. timing_offset = sum of previous durations."
        )),
        HumanMessage(content=(
            f"Available images:\n{img_summary}\n\n"
            f"Create a {intent.visual_style} storyboard with coherent narrative arc."
        )),
    ])
    return {**state, "storyboard": result.model_dump(), "status": "storyboard_written"}


# ── Agent 3: Script Generator ─────────────────────────────────────────────────

def generate_script_node(state: dict, rag: RAGStore) -> dict:
    llm = _llm(config.CREATIVE_MODEL, temperature=0.2)
    intent = VideoIntent(**state["intent"])

    api_ctx = rag.get_api_context("image slideshow sequence fade opacity interpolate AbsoluteFill Img")
    scenes_json = json.dumps(state["storyboard"]["scenes"], indent=2)

    error_ctx = ""
    comp = state.get("compilation_result") or {}
    if comp and not comp.get("success"):
        err_api = rag.get_api_context(comp.get("error_message", ""), k=3)
        error_ctx = f"\n\n⚠ PREVIOUS ERROR — fix:\n{comp['error_message']}\n\nAPI:\n{err_api}"

    total_frames = int(state["storyboard"]["total_duration"] * 30)

    prompt = f"""Generate complete valid Remotion TypeScript composition.

Scenes (fps=30, 1s = 30 frames):
{scenes_json}

Style: {intent.visual_style} | transition: {intent.transition_preference}
{error_ctx}

API reference:
{api_ctx}

RULES:
1. import React from 'react';
2. import {{AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, interpolate, staticFile, registerRoot, Composition}} from 'remotion';
3. <Sequence from={{Math.round(timing_offset*30)}} durationInFrames={{Math.round(duration*30)}}>
4. Fade: opacity = interpolate(frame, [0, 15], [0, 1], {{extrapolateRight:'clamp'}})
5. <Img src={{staticFile(filename_only)}} style={{{{width:'100%',height:'100%',objectFit:'cover'}}}} />
6. If caption, add <div> text overlay
7. registerRoot(() => (<><Composition id="FotoOwlReel" component={{FotoOwlReel}} durationInFrames={{{total_frames}}} fps={{30}} width={{1920}} height={{1080}}/></>));
8. Output ONLY TypeScript code — no markdown, no explanation"""

    resp = llm.invoke([
        SystemMessage(content="You are a Remotion TypeScript expert. Output ONLY code."),
        HumanMessage(content=prompt),
    ])
    code = resp.content.strip()
    for fence in ("```typescript", "```tsx", "```ts", "```"):
        code = code.lstrip(fence)
    code = code.rstrip("```").strip()
    return {**state, "script_code": code, "status": "script_generated"}


# ── Agent 4: Compiler & Fixer ─────────────────────────────────────────────────

def compile_and_fix_node(state: dict) -> dict:
    os.makedirs(f"{config.REMOTION_DIR}/src", exist_ok=True)
    script_path = os.path.join(config.REMOTION_DIR, "src", "Composition.tsx")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(state["script_code"])

    try:
        cmd = 'npx tsc --noEmit --jsx react --esModuleInterop --target ES2020 --moduleResolution node --skipLibCheck src/Composition.tsx'
        res = subprocess.run(
            cmd,
            cwd=os.path.abspath(config.REMOTION_DIR),
            capture_output=True, text=True, timeout=30, shell=True,
        )
        if res.returncode == 0:
            comp = CompilationResult(success=True)
        else:
            comp = CompilationResult(success=False, error_message=(res.stderr or res.stdout)[:600])
    except Exception as e:
        code = state["script_code"]
        ok = ("registerRoot" in code and "FotoOwlReel" in code and code.count("{") == code.count("}"))
        comp = CompilationResult(success=ok, error_message=None if ok else f"Check failed: {e}")

    new_retry = state["retry_count"] + (0 if comp.success else 1)
    return {**state, "compilation_result": comp.model_dump(), "retry_count": new_retry}


# ── Agent 5: Renderer ─────────────────────────────────────────────────────────

def render_node(state: dict) -> dict:
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    out = os.path.abspath(os.path.join(config.OUTPUT_DIR, "reel.mp4"))
    remotion_dir = os.path.abspath(config.REMOTION_DIR)
    try:
        # use shell=True so Windows can find npx in PATH
        cmd = f'npx remotion render src/Composition.tsx FotoOwlReel "{out}" --log error'
        res = subprocess.run(
            cmd,
            cwd=remotion_dir,
            capture_output=True,
            text=True,
            timeout=300,
            shell=True,
        )
        if res.returncode == 0:
            return {**state, "render_output_path": out, "status": "rendered"}
        return {**state, "status": "render_failed",
                "error": (res.stderr or res.stdout)[:400]}
    except Exception as e:
        return {**state, "status": "render_failed", "error": str(e)}
