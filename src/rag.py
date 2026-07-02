"""
RAG layer — simple keyword-based retrieval (no embeddings needed).
"""
from typing import Dict, List


class RAGStore:
    """Simple keyword-based RAG — no embedding API calls."""
    
    def __init__(self):
        self.styles: Dict[str, str] = {}
        self.api_docs: Dict[str, str] = {}
    
    def initialize(self):
        # Style guides
        self.styles = {
            "cinematic": (
                "Cinematic: slow pacing (3-5s per image), warm color grading, fade transitions, "
                "emotional captions, intimate framing, golden-hour aesthetic, minimal text overlays, "
                "focus on faces and emotional moments."
            ),
            "upbeat": (
                "Upbeat: fast pacing (1-2s per image), vibrant saturated colors, cut/slide transitions, "
                "bold energetic ALL-CAPS captions, dynamic zoom effects, celebration-focused, "
                "multiple text overlays, high-contrast edits."
            ),
            "corporate": (
                "Corporate: medium pacing (2-3s per image), clean neutral tones, subtle slide transitions, "
                "professional concise captions, structured composition, brand-consistent layout, "
                "focus on achievement and teamwork."
            ),
            "documentary": (
                "Documentary: varied pacing with deliberate pauses, natural color grading, slow dissolve "
                "transitions, narrative captions that build a story, candid moment focus, "
                "chronological sequencing, wide establishing shots."
            ),
        }
        
        # Remotion API snippets
        self.api_docs = {
            "useCurrentFrame": "useCurrentFrame(): returns current frame number (0-indexed). const frame = useCurrentFrame();",
            "useVideoConfig": "useVideoConfig(): returns {fps, width, height, durationInFrames}. const {fps, durationInFrames} = useVideoConfig();",
            "interpolate": "interpolate(value, inputRange, outputRange, options): maps a value between ranges. const opacity = interpolate(frame, [0, 20], [0, 1], {extrapolateLeft:'clamp', extrapolateRight:'clamp'});",
            "spring": "spring({frame, fps, config}): spring animation returning 0→1. const scale = spring({frame, fps, config:{damping:200}});",
            "Sequence": "Sequence: renders children starting at a given frame. <Sequence from={60} durationInFrames={90}><Scene /></Sequence>",
            "AbsoluteFill": "AbsoluteFill: fills the entire video frame absolutely. <AbsoluteFill style={{backgroundColor:'#000'}}>{children}</AbsoluteFill>",
            "Img": "Img: Remotion image with preloading. import {Img, staticFile} from 'remotion'; <Img src={staticFile('photo.jpg')} style={{width:'100%',height:'100%',objectFit:'cover'}} />",
            "registerRoot": "registerRoot + Composition: required entry point. registerRoot(() => (<><Composition id='FotoOwlReel' component={MyVideo} durationInFrames={300} fps={30} width={1920} height={1080}/></>));",
        }
    
    def get_style_context(self, query: str, k: int = 2) -> str:
        """Retrieve style guides matching query keywords."""
        query_lower = query.lower()
        matches = []
        for style_name, content in self.styles.items():
            if style_name in query_lower or any(word in content.lower() for word in query_lower.split()):
                matches.append(content)
                if len(matches) >= k:
                    break
        # If no matches, return all
        if not matches:
            matches = list(self.styles.values())[:k]
        return "\n\n".join(matches)
    
    def get_api_context(self, query: str, k: int = 5) -> str:
        """Retrieve API docs matching query keywords."""
        query_lower = query.lower()
        matches = []
        for api_name, content in self.api_docs.items():
            if api_name.lower() in query_lower or any(word in content.lower() for word in query_lower.split()):
                matches.append(content)
                if len(matches) >= k:
                    break
        # If no matches, return most common ones
        if not matches:
            matches = [
                self.api_docs["Sequence"],
                self.api_docs["interpolate"],
                self.api_docs["AbsoluteFill"],
                self.api_docs["Img"],
                self.api_docs["registerRoot"],
            ][:k]
        return "\n\n".join(matches)
