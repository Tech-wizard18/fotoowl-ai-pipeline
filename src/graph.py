"""LangGraph StateGraph — five-agent pipeline with conditional retry loop."""
from typing import TypedDict, Optional, List, Any

from langgraph.graph import StateGraph, END

from src.agents import (
    parse_intent_node, analyze_images_node, write_storyboard_node,
    generate_script_node, compile_and_fix_node, render_node,
)
from src.rag import RAGStore
from src.config import config


class State(TypedDict):
    user_prompt: str
    image_folder: str
    intent: Optional[dict]
    image_analyses: List[dict]
    storyboard: Optional[dict]
    script_code: Optional[str]
    compilation_result: Optional[dict]
    retry_count: int
    max_retries: int
    render_output_path: Optional[str]
    status: str
    error: Optional[str]


def _retry_router(state: State) -> str:
    """Conditional edge: route after compile_and_fix."""
    comp = state.get("compilation_result") or {}
    if comp.get("success"):
        return "render"
    if state.get("retry_count", 0) >= state.get("max_retries", config.MAX_RETRIES):
        return "end_failure"
    return "generate_script"


def build_graph(rag: RAGStore) -> Any:
    """Build and compile the LangGraph pipeline."""
    graph = StateGraph(State)

    graph.add_node("parse_intent", parse_intent_node)
    graph.add_node("analyze_images", analyze_images_node)
    graph.add_node("write_storyboard", lambda s: write_storyboard_node(s, rag))
    graph.add_node("generate_script", lambda s: generate_script_node(s, rag))
    graph.add_node("compile_and_fix", compile_and_fix_node)
    graph.add_node("render", render_node)

    graph.set_entry_point("parse_intent")
    graph.add_edge("parse_intent", "analyze_images")
    graph.add_edge("analyze_images", "write_storyboard")
    graph.add_edge("write_storyboard", "generate_script")
    graph.add_edge("generate_script", "compile_and_fix")

    graph.add_conditional_edges(
        "compile_and_fix",
        _retry_router,
        {"render": "render", "generate_script": "generate_script", "end_failure": END},
    )
    graph.add_edge("render", END)

    return graph.compile()
