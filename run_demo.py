#!/usr/bin/env python3
"""
Demo script showing two different prompts on the same image set.
Demonstrates that intent, storyboard, and script differ based on prompt.
"""
import os
import sys
import json
from pathlib import Path

from main import run_pipeline


def demo():
    """Run pipeline with two contrasting prompts."""
    
    # Check for images
    image_folder = "./sample_images"
    images = list(Path(image_folder).glob("*.jpg")) + list(Path(image_folder).glob("*.png"))
    
    if len(images) < 3:
        print("⚠️  Please add at least 3 images to sample_images/ folder")
        print("   You can download sample images from the Google Drive link in the task PDF")
        sys.exit(1)
    
    print(f"Found {len(images)} images\n")
    
    # Prompt 1: Cinematic
    print("=" * 70)
    print("DEMO 1: Cinematic Wedding Style")
    print("=" * 70)
    prompt1 = "Cinematic wedding reel, slow and emotional, warm tones, minimal text"
    state1 = run_pipeline(image_folder, prompt1)
    
    print("\n" + "=" * 70)
    print("DEMO 2: Upbeat Birthday Style")
    print("=" * 70)
    prompt2 = "Upbeat birthday reel, fast cuts, bold captions, energetic"
    state2 = run_pipeline(image_folder, prompt2)
    
    # Compare outputs
    print("\n" + "=" * 70)
    print("COMPARISON OF OUTPUTS")
    print("=" * 70)
    
    if state1.get("intent") and state2.get("intent"):
        print("\n📊 Intent Differences:")
        print(f"   Pacing:     {state1['intent']['pacing']:10s} vs {state2['intent']['pacing']}")
        print(f"   Style:      {state1['intent']['visual_style']:10s} vs {state2['intent']['visual_style']}")
        print(f"   Tone:       {state1['intent']['caption_tone']:10s} vs {state2['intent']['caption_tone']}")
        print(f"   Transition: {state1['intent']['transition_preference']:10s} vs {state2['intent']['transition_preference']}")
    
    if state1.get("storyboard") and state2.get("storyboard"):
        sb1 = state1["storyboard"]
        sb2 = state2["storyboard"]
        print("\n📋 Storyboard Differences:")
        print(f"   Scene count:    {len(sb1['scenes'])} vs {len(sb2['scenes'])}")
        print(f"   Total duration: {sb1['total_duration']:.1f}s vs {sb2['total_duration']:.1f}s")
        print(f"   Avg scene time: {sb1['total_duration']/len(sb1['scenes']):.1f}s vs {sb2['total_duration']/len(sb2['scenes']):.1f}s")
    
    if state1.get("script_code") and state2.get("script_code"):
        print("\n📝 Script Differences:")
        print(f"   Code length:    {len(state1['script_code'])} chars vs {len(state2['script_code'])} chars")
        print(f"   Unique:         Scripts are {'identical' if state1['script_code'] == state2['script_code'] else 'DIFFERENT'}")
    
    print("\n✅ Demo complete! Check output/ folder for detailed results.")
    print("   - output/storyboard.json")
    print("   - output/composition.tsx")
    print("   - output/pipeline_state.json")
    if state1.get("render_output_path"):
        print(f"   - {state1['render_output_path']}")


if __name__ == "__main__":
    demo()
