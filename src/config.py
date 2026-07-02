import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # All free unlimited via Groq  
    # Vision: llama-3.2-90b-vision-preview is decommissioned, use llama-3.2-11b-vision-preview
    VISION_MODEL: str   = os.getenv("VISION_MODEL",   "llama-3.2-11b-vision-preview")
    CREATIVE_MODEL: str = os.getenv("CREATIVE_MODEL", "llama-3.3-70b-versatile")
    UTILITY_MODEL: str  = os.getenv("UTILITY_MODEL",  "llama-3.3-70b-versatile")

    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    OUTPUT_DIR: str  = "./output"
    REMOTION_DIR: str = "./remotion"


config = Config()
