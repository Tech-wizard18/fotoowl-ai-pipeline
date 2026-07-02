import React from 'react';
import { AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, interpolate, staticFile, registerRoot, Composition } from 'remotion';

const scenes = [
  {
    "image_path": "photo01.jpg",
    "duration": 3.0,
    "caption": "Introduction",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 0.0
  },
  {
    "image_path": "photo02.jpg",
    "duration": 3.0,
    "caption": "Rising Action",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 3.0
  },
  {
    "image_path": "photo05.jpg",
    "duration": 5.0,
    "caption": "Climax",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 6.0
  },
  {
    "image_path": "photo04.jpg",
    "duration": 2.0,
    "caption": "Falling Action",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 11.0
  },
  {
    "image_path": "photo09.jpg",
    "duration": 2.0,
    "caption": "Resolution",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 13.0
  }
];

const FotoOwlReel: React.FC = () => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {scenes.map((scene, index) => (
        <Sequence
          from={Math.round(scene.timing_offset * fps)}
          durationInFrames={Math.round(scene.duration * fps)}
          key={index}
        >
          <AbsoluteFill style={{ opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }) }}>
            <Img src={staticFile(scene.image_path)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            {scene.caption && (
              <div style={{ fontSize: 40, fontWeight: 'bold', color: 'white', position: 'absolute', bottom: 20, left: 20 }}>
                {scene.caption}
              </div>
            )}
          </AbsoluteFill>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

registerRoot(() => (
  <Composition
    id="FotoOwlReel"
    component={FotoOwlReel}
    durationInFrames={540}
    fps={30}
    width={1920}
    height={1080}
  />
));