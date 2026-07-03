import React from 'react';
import { AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, interpolate, staticFile, registerRoot, Composition } from 'remotion';

const FotoOwlReel: React.FC = () => {
  const { fps } = useVideoConfig();
  const scenes = [
    {
      "image_path": "_ASL9923.jpg",
      "duration": 1.0,
      "caption": "THEY LIVED HAPPILY EVER AFTER!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 0.0
    },
    {
      "image_path": "_ASL9969.jpg",
      "duration": 1.0,
      "caption": "TOGETHER FOREVER!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 1.0
    },
    {
      "image_path": "_ASL9971.jpg",
      "duration": 1.0,
      "caption": "WITH LOVE AND DEVOTION!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 2.0
    },
    {
      "image_path": "_ASL9976.jpg",
      "duration": 1.0,
      "caption": "THEIR LOVE STORY!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 3.0
    },
    {
      "image_path": "_ASL9984.jpg",
      "duration": 1.0,
      "caption": "A LOVE THAT LASTS!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 4.0
    },
    {
      "image_path": "_ASL9995.jpg",
      "duration": 1.0,
      "caption": "HAPPILY EVER AFTER!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 5.0
    },
    {
      "image_path": "AHD_6008.jpg",
      "duration": 1.0,
      "caption": "THE BRIDE PREPARES!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 6.0
    },
    {
      "image_path": "AHD_6020.jpg",
      "duration": 1.0,
      "caption": "THE GROOM PREPARES!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 7.0
    },
    {
      "image_path": "AHD_6024.jpg",
      "duration": 1.0,
      "caption": "THE CEREMONY!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 8.0
    },
    {
      "image_path": "AHD_6052.jpg",
      "duration": 1.0,
      "caption": "THE FEAST!",
      "transition_in": "cut",
      "transition_out": "cut",
      "timing_offset": 9.0
    }
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {scenes.map((scene, index) => (
        <Sequence
          from={Math.round(scene.timing_offset * 30)}
          durationInFrames={Math.round(scene.duration * 30)}
          key={index}
        >
          <AbsoluteFill>
            <Img
              src={staticFile(scene.image_path)}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
              }}
            />
            {scene.caption && (
              <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center' }}>
                <div
                  style={{
                    fontSize: 40,
                    color: 'white',
                    textShadow: '2px 2px 4px black',
                  }}
                >
                  {scene.caption}
                </div>
              </AbsoluteFill>
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
    durationInFrames={300}
    fps={30}
    width={1920}
    height={1080}
  />
));