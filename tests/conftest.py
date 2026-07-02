import pytest
import os

# Prevent real API calls in tests
os.environ.setdefault("GROQ_API_KEY", "test-key-mock")


@pytest.fixture
def mock_intent():
    return {
        "pacing": "slow",
        "visual_style": "cinematic",
        "caption_tone": "emotional",
        "transition_preference": "fade",
        "emotion": "warm"
    }


@pytest.fixture
def mock_analyses():
    return [
        {
            "image_path": "images/photo1.jpg",
            "description": "Couple exchanging vows at altar",
            "quality_score": 0.95,
            "prominent_subjects": ["bride", "groom"],
            "mood": "romantic",
            "suggested_duration": 4.0,
        },
        {
            "image_path": "images/photo2.jpg",
            "description": "Guests celebrating at reception",
            "quality_score": 0.80,
            "prominent_subjects": ["guests", "dance floor"],
            "mood": "joyful",
            "suggested_duration": 2.5,
        },
        {
            "image_path": "images/photo3.jpg",
            "description": "Bride and groom first dance",
            "quality_score": 0.92,
            "prominent_subjects": ["bride", "groom"],
            "mood": "romantic",
            "suggested_duration": 3.5,
        },
    ]


@pytest.fixture
def mock_storyboard():
    return {
        "scenes": [
            {
                "image_path": "images/photo1.jpg",
                "duration": 4.0,
                "caption": "A moment to remember",
                "transition_in": "fade",
                "transition_out": "fade",
                "timing_offset": 0.0,
            },
            {
                "image_path": "images/photo3.jpg",
                "duration": 3.5,
                "caption": "Together forever",
                "transition_in": "fade",
                "transition_out": "fade",
                "timing_offset": 4.0,
            },
        ],
        "total_duration": 7.5,
        "style": "cinematic",
        "music_suggestion": "soft piano",
    }


@pytest.fixture
def base_state(mock_intent, mock_analyses, mock_storyboard):
    return {
        "user_prompt": "Cinematic wedding reel, slow and emotional, warm tones",
        "image_folder": "./images",
        "intent": mock_intent,
        "image_analyses": mock_analyses,
        "storyboard": mock_storyboard,
        "script_code": None,
        "compilation_result": None,
        "retry_count": 0,
        "max_retries": 3,
        "render_output_path": None,
        "status": "initialized",
        "error": None,
    }
