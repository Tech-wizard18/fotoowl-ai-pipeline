import React from 'react';
import { AbsoluteFill, Sequence, Img, useCurrentFrame, useVideoConfig, interpolate, staticFile, registerRoot, Composition } from 'remotion';

const FotoOwlReel = () => {
  const scenes = [
    {
      "image_path": "photo01.jpg",
      "duration": 3.5,
      "caption": "The event begins",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 0.0
    },
    {
      "image_path": "photo02.jpg",
      "duration": 3.5,
      "caption": "Attendees gather and socialize",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 3.5
    },
    {
      "image_path": "photo03.jpg",
      "duration": 3.5,
      "caption": "The event space comes alive",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 7.0
    },
    {
      "image_path": "photo04.jpg",
      "duration": 3.5,
      "caption": "A candid moment of joy",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 10.5
    },
    {
      "image_path": "photo05.jpg",
      "duration": 3.5,
      "caption": "The highlight of the event",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 14.0
    },
    {
      "image_path": "photo06.jpg",
      "duration": 3.5,
      "caption": "An intimate moment shared",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 17.5
    },
    {
      "image_path": "photo07.jpg",
      "duration": 3.5,
      "caption": "Attendees enjoy the event together",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 21.0
    },
    {
      "image_path": "photo08.jpg",
      "duration": 3.5,
      "caption": "A scenic overview of the location",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 24.5
    },
    {
      "image_path": "photo09.jpg",
      "duration": 3.5,
      "caption": "A special moment between attendees",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 28.0
    },
    {
      "image_path": "photo10.jpg",
      "duration": 3.5,
      "caption": "The event comes to a close",
      "transition_in": "fade",
      "transition_out": "fade",
      "timing_offset": 31.5
    }
  ];

  const { width, height } = useVideoConfig();

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
            {scene.transition_in === 'fade' && (
              <AbsoluteFill
                style={{
                  opacity: interpolate(useCurrentFrame(), [0, 15], [0, 1], {
                    extrapolateRight: 'clamp',
                  }),
                }}
              />
            )}
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
    durationInFrames={1050}
    fps={30}
    width={1920}
    height={1080}
  />
));