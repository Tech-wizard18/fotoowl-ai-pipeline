import React from 'react';
import { AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, interpolate, staticFile, registerRoot, Composition } from 'remotion';

const scenes = [
  {
    "image_path": "_ASL9923.jpg",
    "duration": 5.0,
    "caption": "The couple's special day begins",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 0.0
  },
  {
    "image_path": "_ASL9969.jpg",
    "duration": 5.0,
    "caption": "Love is in the air",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 5.0
  },
  {
    "image_path": "_ASL9971.jpg",
    "duration": 5.0,
    "caption": "Cherishing the moment",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 10.0
  },
  {
    "image_path": "_ASL9984.jpg",
    "duration": 3.0,
    "caption": "Together forever",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 15.0
  },
  {
    "image_path": "_ASL9995.jpg",
    "duration": 3.0,
    "caption": "Happiness abounds",
    "transition_in": "fade",
    "transition_out": "fade",
    "timing_offset": 18.0
  }
];

const FotoOwlReel = () => {
  const { width, height } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {scenes.map((scene, index) => (
        <Sequence
          from={Math.round(scene.timing_offset * 30)}
          durationInFrames={Math.round(scene.duration * 30)}
          key={index}
        >
          <AbsoluteFill style={{ opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateRight: 'clamp' }) }}>
            <Img src={staticFile(scene.image_path)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            {scene.caption && (
              <div
                style={{
                  position: 'absolute',
                  bottom: 100,
                  left: 100,
                  fontSize: 40,
                  color: 'white',
                  fontWeight: 'bold',
                }}
              >
                {scene.caption}
              </div>
            )}
          </AbsoluteFill>
          <AbsoluteFill style={{ opacity: interpolate(frame, [Math.round(scene.duration * 30) - 15, Math.round(scene.duration * 30)], [1, 0], { extrapolateLeft: 'clamp' }) }}>
            <Img src={staticFile(scene.image_path)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            {scene.caption && (
              <div
                style={{
                  position: 'absolute',
                  bottom: 100,
                  left: 100,
                  fontSize: 40,
                  color: 'white',
                  fontWeight: 'bold',
                }}
              >
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
    durationInFrames={780}
    fps={30}
    width={1920}
    height={1080}
  />
));