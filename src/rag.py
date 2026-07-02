"""RAG layer — real local vector store using ChromaDB, no API key required
(uses ChromaDB's default local embedding model, downloaded once on first run)."""
import chromadb
from chromadb.utils import embedding_functions

_EMBED_FN = embedding_functions.DefaultEmbeddingFunction()

STYLE_GUIDES = [
    {"id": "cinematic", "style": "cinematic", "text": (
        "Cinematic: slow pacing (3-5s per image), warm color grading, fade transitions, "
        "emotional captions, intimate framing, golden-hour aesthetic, minimal text overlays, "
        "focus on faces and emotional moments.")},
    {"id": "upbeat", "style": "upbeat", "text": (
        "Upbeat: fast pacing (1-2s per image), vibrant saturated colors, cut/slide transitions, "
        "bold energetic ALL-CAPS captions, dynamic zoom effects, celebration-focused, "
        "multiple text overlays, high-contrast edits.")},
    {"id": "corporate", "style": "corporate", "text": (
        "Corporate: medium pacing (2-3s per image), clean neutral tones, subtle slide transitions, "
        "professional concise captions, structured composition, brand-consistent layout, "
        "focus on achievement and teamwork.")},
    {"id": "documentary", "style": "documentary", "text": (
        "Documentary: varied pacing with deliberate pauses, natural color grading, slow dissolve "
        "transitions, narrative captions that build a story, candid moment focus, "
        "chronological sequencing, wide establishing shots.")},
]

API_DOCS = [
    {"id": "useCurrentFrame", "text": "useCurrentFrame(): returns current frame number (0-indexed). const frame = useCurrentFrame();"},
    {"id": "useVideoConfig", "text": "useVideoConfig(): returns {fps, width, height, durationInFrames}. const {fps, durationInFrames} = useVideoConfig();"},
    {"id": "interpolate", "text": "interpolate(value, inputRange, outputRange, options): maps a value between ranges. const opacity = interpolate(frame, [0, 20], [0, 1], {extrapolateLeft:'clamp', extrapolateRight:'clamp'});"},
    {"id": "spring", "text": "spring({frame, fps, config}): spring animation returning 0→1. const scale = spring({frame, fps, config:{damping:200}});"},
    {"id": "Sequence", "text": "Sequence: renders children starting at a given frame. <Sequence from={60} durationInFrames={90}><Scene /></Sequence>"},
    {"id": "AbsoluteFill", "text": "AbsoluteFill: fills the entire video frame absolutely. <AbsoluteFill style={{backgroundColor:'#000'}}>{children}</AbsoluteFill>"},
    {"id": "Img", "text": "Img: Remotion image with preloading. import {Img, staticFile} from 'remotion'; <Img src={staticFile('photo.jpg')} style={{width:'100%',height:'100%',objectFit:'cover'}} />"},
    {"id": "registerRoot", "text": "registerRoot + Composition: required entry point. registerRoot(() => (<><Composition id='FotoOwlReel' component={MyVideo} durationInFrames={300} fps={30} width={1920} height={1080}/></>));"},
    {"id": "missing_import_error", "text": "Error pattern: 'Cannot find name X' means X was used without being imported from 'remotion'. Fix by adding X to the existing import statement."},
    {"id": "duration_mismatch_error", "text": "Error pattern: durationInFrames on Composition must equal the last Sequence's from + durationInFrames, or the render cuts off early / has trailing black frames."},
]


class RAGStore:
    """Chroma-backed vector store — real semantic retrieval, not keyword matching."""

    def __init__(self, persist_dir: str = ".chroma"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.style_collection = self.client.get_or_create_collection(
            "style_guides", embedding_function=_EMBED_FN
        )
        self.api_collection = self.client.get_or_create_collection(
            "remotion_api", embedding_function=_EMBED_FN
        )

    def initialize(self):
        if self.style_collection.count() == 0:
            self.style_collection.add(
                ids=[d["id"] for d in STYLE_GUIDES],
                documents=[d["text"] for d in STYLE_GUIDES],
                metadatas=[{"style": d["style"]} for d in STYLE_GUIDES],
            )
        if self.api_collection.count() == 0:
            self.api_collection.add(
                ids=[d["id"] for d in API_DOCS],
                documents=[d["text"] for d in API_DOCS],
            )

    def get_style_context(self, query: str, k: int = 2) -> str:
        res = self.style_collection.query(query_texts=[query], n_results=k)
        return "\n\n".join(res["documents"][0])

    def get_api_context(self, query: str, k: int = 5) -> str:
        res = self.api_collection.query(query_texts=[query], n_results=k)
        return "\n\n".join(res["documents"][0])