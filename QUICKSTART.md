# FotoOwl AI — Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Setup Environment

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### Step 2: Add API Key

**Get a FREE Gemini API key:**
1. Go to: https://aistudio.google.com/apikey
2. Click "Create API key" (sign in with Google if needed)
3. Copy your key

Edit `.env` and paste your key:
```
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

This is **100% free** — no credit card needed. You get 1500 requests/day.

### Step 3: Add Images

Place 8-12 event photos in the `sample_images/` folder:
```
sample_images/
  ├── photo1.jpg
  ├── photo2.jpg
  └── ...
```

Download sample images from the Google Drive link in the task PDF.

### Step 4: Run Pipeline

```bash
# Activate venv first (if not already)
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Run with your creative prompt
python main.py --images sample_images --prompt "Cinematic wedding reel, slow and emotional, warm tones, minimal text"
```

### Step 5: Check Output

Results saved to `output/` folder:
- `storyboard.json` — Scene sequence with timing
- `composition.tsx` — Generated Remotion code
- `pipeline_state.json` — Full execution trace
- `reel.mp4` — Final video (if render succeeded)

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

All tests use mocked LLM calls — **no API key needed for testing**.

---

## 🎬 Try Different Styles

Run the demo to see how different prompts produce different results:

```bash
python run_demo.py
```

This runs the pipeline twice on the same images with contrasting prompts:
1. Cinematic (slow, emotional, warm)
2. Upbeat (fast, energetic, bold)

Compare the outputs to see how intent drives creative decisions.

---

## 📊 View Graph Diagram

The LangGraph flow is visualized in README.md (Mermaid diagram).

To render it:
1. View README.md on GitHub
2. Or use VSCode with Markdown Preview Mermaid Support extension
3. Or paste into https://mermaid.live

---

## 🐛 Troubleshooting

**"No images found in folder"**
→ Add .jpg or .png files to sample_images/

**"GOOGLE_API_KEY is not set"**
→ Edit .env and add your Gemini key from https://aistudio.google.com/apikey

**"ModuleNotFoundError"**
→ Activate venv: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)

**"npx: command not found"**
→ Install Node.js 18+ from https://nodejs.org

**Compilation fails but script looks correct**
→ This is expected sometimes. Check output/composition.tsx and manually fix if needed.

**Render fails with "Command not found"**
→ Run `cd remotion && npm install && cd ..`

---

## 💰 Cost Estimate

**100% FREE** with Google Gemini:
- All API calls use `gemini-2.0-flash` (free tier)
- Limit: 1500 requests/day
- A full pipeline run with 10 images uses ~15-20 requests
- You can run the pipeline ~75-100 times per day for FREE
- No credit card required

---

## 📚 Next Steps

- Read README.md for architecture details
- Check src/agents.py to understand each agent
- Review src/rag.py for RAG implementation
- Explore tests/test_pipeline.py for testing patterns
- Modify src/graph.py to add new nodes or edges

Happy building! 🦉
