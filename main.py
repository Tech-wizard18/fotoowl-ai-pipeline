#!/usr/bin/env python3
"""FotoOwl AI — Image-to-Video Multiagent Pipeline entry point."""

import argparse
import json
import os
import sys
from pathlib import Path

from src.config import config
from src.graph import build_graph
from src.rag import RAGStore


def run_pipeline(image_folder: str, user_prompt: str) -> dict:
    """Run the full pipeline and return final state."""
    print(" FotoOwl AI Pipeline starting...")
    print(f"   Images: {image_folder}")
    print(f"   Prompt: {user_prompt}\n")

    # Init RAG
    print(" Initializing RAG store...")
    rag = RAGStore()
    rag.initialize()

    # Build graph
    graph = build_graph(rag)

    initial_state = {
        "user_prompt": user_prompt,
        "image_folder": image_folder,
        "intent": None,
        "image_analyses": [],
        "storyboard": None,
        "script_code": None,
        "compilation_result": None,
        "retry_count": 0,
        "max_retries": config.MAX_RETRIES,
        "render_output_path": None,
        "status": "initialized",
        "error": None,
    }

    # Stream and show progress
    final_state = None
    for step in graph.stream(initial_state):
        for node_name, state in step.items():
            status = state.get("status", "")
            retries = state.get("retry_count", 0)
            print(f"   ✓ [{node_name}] status={status} retries={retries}")
            final_state = state

    # Save outputs
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    if final_state:
        # Save pipeline state
        state_path = f"{config.OUTPUT_DIR}/pipeline_state.json"
        with open(state_path, "w") as f:
            safe_state = {k: v for k, v in final_state.items() if k != "script_code"}
            json.dump(safe_state, f, indent=2)

        # Save storyboard
        if final_state.get("storyboard"):
            sb_path = f"{config.OUTPUT_DIR}/storyboard.json"
            with open(sb_path, "w") as f:
                json.dump(final_state["storyboard"], f, indent=2)
            print(f"\n Storyboard saved → {sb_path}")

        # Save script
        if final_state.get("script_code"):
            sc_path = f"{config.OUTPUT_DIR}/composition.tsx"
            with open(sc_path, "w") as f:
                f.write(final_state["script_code"])
            print(f" Script saved     → {sc_path}")

        print(f" Pipeline state   → {state_path}")

        status = final_state.get("status")
        if status == "rendered":
            print(f"\n Video rendered   → {final_state.get('render_output_path')}")
        elif status == "render_failed":
            print(f"\n⚠  Render failed: {final_state.get('error')}")
            print("   Script and storyboard saved for review.")
        else:
            print(f"\n⚠  Pipeline ended with status: {status}")
            if final_state.get("error"):
                print(f"   Error: {final_state['error']}")

    return final_state or {}


def main():
    parser = argparse.ArgumentParser(description="FotoOwl AI — Image-to-Video Pipeline")
    parser.add_argument("--images", required=True, help="Folder containing event images")
    parser.add_argument("--prompt", required=True, help="Creative brief for the video")
    args = parser.parse_args()

    if not os.path.isdir(args.images):
        print(f"Error: '{args.images}' is not a valid directory.")
        sys.exit(1)

    if not config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY is not set in .env")
        print("Get a free key at: https://console.groq.com")
        sys.exit(1)

    run_pipeline(args.images, args.prompt)


if __name__ == "__main__":
    main()
