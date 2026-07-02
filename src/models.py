from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class VideoIntent(BaseModel):
    """Structured video intent parsed from user prompt."""
    pacing: Literal["slow", "medium", "fast"] = Field(description="Video pacing speed")
    visual_style: str = Field(description="Visual treatment style (e.g., cinematic, upbeat, corporate)")
    caption_tone: str = Field(description="Tone for text overlays (e.g., emotional, energetic, professional)")
    transition_preference: Literal["fade", "cut", "slide", "zoom"] = Field(description="Preferred transition type")
    emotion: str = Field(description="Target emotional tone")


class ImageAnalysis(BaseModel):
    """Analysis result for a single image."""
    image_path: str
    description: str
    quality_score: float = Field(ge=0, le=1, description="Image quality (0-1)")
    prominent_subjects: List[str]
    mood: str
    suggested_duration: float = Field(description="Suggested display duration in seconds")


class StoryboardScene(BaseModel):
    """A single scene in the storyboard."""
    image_path: str
    duration: float = Field(description="Scene duration in seconds")
    caption: Optional[str] = None
    transition_in: str = Field(description="Transition type entering this scene")
    transition_out: str = Field(description="Transition type leaving this scene")
    timing_offset: float = Field(description="Start time in video timeline")


class Storyboard(BaseModel):
    """Complete storyboard with scenes."""
    scenes: List[StoryboardScene]
    total_duration: float
    style: str
    music_suggestion: Optional[str] = None


class CompilationResult(BaseModel):
    """Result from script compilation attempt."""
    success: bool
    error_message: Optional[str] = None
    error_line: Optional[int] = None
    suggestions: List[str] = Field(default_factory=list)


class PipelineState(BaseModel):
    """Shared state object for LangGraph."""
    user_prompt: str
    image_folder: str
    intent: Optional[VideoIntent] = None
    image_analyses: List[ImageAnalysis] = Field(default_factory=list)
    storyboard: Optional[Storyboard] = None
    script_code: Optional[str] = None
    compilation_result: Optional[CompilationResult] = None
    retry_count: int = 0
    max_retries: int = 3
    render_output_path: Optional[str] = None
    status: str = "initialized"
    error: Optional[str] = None
