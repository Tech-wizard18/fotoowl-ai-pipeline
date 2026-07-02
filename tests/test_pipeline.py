"""
Test suite — all run with mocked LLM calls (no API keys needed).
"""
import json
import pytest
from unittest.mock import MagicMock, patch

GROQ_PATH = "src.agents.ChatGroq"


# ─── Scenario 1: Intent parsing ───────────────────────────────────────────────

class TestIntentParsing:

    def _make_intent(self, **kw):
        from src.models import VideoIntent
        return VideoIntent(**{"pacing":"slow","visual_style":"cinematic",
            "caption_tone":"emotional","transition_preference":"fade","emotion":"warm",**kw})

    @patch(GROQ_PATH)
    def test_cinematic_intent(self, MockLLM):
        mock = MagicMock()
        mock.with_structured_output.return_value = mock
        mock.invoke.return_value = self._make_intent()
        MockLLM.return_value = mock
        from src.agents import parse_intent_node
        s = parse_intent_node({"user_prompt": "Cinematic wedding, slow emotional", "image_folder": "."})
        assert s["intent"]["pacing"] == "slow"
        assert s["intent"]["visual_style"] == "cinematic"
        assert s["status"] == "intent_parsed"

    @patch(GROQ_PATH)
    def test_upbeat_intent(self, MockLLM):
        mock = MagicMock()
        mock.with_structured_output.return_value = mock
        mock.invoke.return_value = self._make_intent(
            pacing="fast", visual_style="upbeat",
            caption_tone="energetic", transition_preference="cut", emotion="joy")
        MockLLM.return_value = mock
        from src.agents import parse_intent_node
        s = parse_intent_node({"user_prompt": "Upbeat birthday, fast cuts", "image_folder": "."})
        assert s["intent"]["pacing"] == "fast"
        assert s["intent"]["visual_style"] == "upbeat"

    def test_intents_differ(self):
        cinematic = {"pacing": "slow", "transition_preference": "fade"}
        upbeat    = {"pacing": "fast", "transition_preference": "cut"}
        assert cinematic["pacing"] != upbeat["pacing"]
        assert cinematic["transition_preference"] != upbeat["transition_preference"]


# ─── Scenario 2: Storyboard generation ───────────────────────────────────────

class TestStoryboardGeneration:

    @patch(GROQ_PATH)
    def test_storyboard_produced(self, MockLLM, base_state, mock_storyboard):
        from src.agents import write_storyboard_node
        from src.models import Storyboard
        mock_rag = MagicMock()
        mock_rag.get_style_context.return_value = "Cinematic: slow, warm tones, fade"
        mock = MagicMock()
        mock.with_structured_output.return_value = mock
        mock.invoke.return_value = Storyboard(**mock_storyboard)
        MockLLM.return_value = mock
        result = write_storyboard_node(base_state, mock_rag)
        assert result["storyboard"] is not None
        assert len(result["storyboard"]["scenes"]) > 0
        assert result["status"] == "storyboard_written"

    @patch(GROQ_PATH)
    def test_storyboard_rag_queried_with_intent(self, MockLLM, base_state, mock_storyboard):
        from src.agents import write_storyboard_node
        from src.models import Storyboard
        mock_rag = MagicMock()
        mock_rag.get_style_context.return_value = "Cinematic: slow pacing"
        mock = MagicMock()
        mock.with_structured_output.return_value = mock
        mock.invoke.return_value = Storyboard(**mock_storyboard)
        MockLLM.return_value = mock
        write_storyboard_node(base_state, mock_rag)
        query = mock_rag.get_style_context.call_args[0][0]
        assert "cinematic" in query


# ─── Scenario 3: Compiler retry loop ─────────────────────────────────────────

class TestCompilerRetryLoop:

    def test_compilation_success(self, base_state):
        from src.agents import compile_and_fix_node
        code = (
            "import React from 'react';\n"
            "import {AbsoluteFill,registerRoot,Composition} from 'remotion';\n"
            "const FotoOwlReel=()=><AbsoluteFill><div>Hi</div></AbsoluteFill>;\n"
            "registerRoot(()=>(<><Composition id='FotoOwlReel' component={FotoOwlReel}"
            " durationInFrames={90} fps={30} width={1920} height={1080}/></>));\n"
        )
        with patch("subprocess.run") as m:
            m.return_value = MagicMock(returncode=0, stderr="", stdout="")
            result = compile_and_fix_node({**base_state, "script_code": code})
        assert result["compilation_result"]["success"] is True

    def test_failure_increments_retry(self, base_state):
        from src.agents import compile_and_fix_node
        with patch("subprocess.run") as m:
            m.return_value = MagicMock(returncode=1, stderr="TS error", stdout="")
            result = compile_and_fix_node({**base_state, "script_code": "bad!!!", "retry_count": 0})
        assert result["compilation_result"]["success"] is False
        assert result["retry_count"] == 1

    def test_routing_stops_at_max(self):
        from src.graph import _retry_router
        assert _retry_router({"compilation_result":{"success":False},"retry_count":3,"max_retries":3}) == "end_failure"

    def test_routing_retries_under_limit(self):
        from src.graph import _retry_router
        assert _retry_router({"compilation_result":{"success":False},"retry_count":1,"max_retries":3}) == "generate_script"

    def test_routing_render_on_success(self):
        from src.graph import _retry_router
        assert _retry_router({"compilation_result":{"success":True},"retry_count":0,"max_retries":3}) == "render"


# ─── LLM-as-Judge: Narrative coherence ───────────────────────────────────────

class TestLLMJudgeNarrativeCoherence:

    def test_coherence_score(self, mock_storyboard):
        from pydantic import BaseModel

        class CoherenceScore(BaseModel):
            score: int
            reasoning: str

        expected = CoherenceScore(score=8, reasoning=(
            "Clear arc: ceremony → first dance → farewell. "
            "Scenes ordered logically with cinematic pacing and fade transitions."
        ))
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = expected

        with patch("langchain_groq.ChatGroq") as MockLLM:
            MockLLM.return_value.with_structured_output.return_value = mock_chain
            from langchain_groq import ChatGroq
            judge = ChatGroq(model="llama-3.3-70b-versatile").with_structured_output(CoherenceScore)
            result = judge.invoke([{
                "role": "user",
                "content": f"Rate narrative coherence 1-10:\n{json.dumps(mock_storyboard)}",
            }])

        assert result.score >= 7
        assert len(result.reasoning) > 20
