import React from 'react';
import { Composition, Still } from 'remotion';
import { MainVideo } from './MainVideo';
import { FullVideo } from './FullVideo';
import { IntroScene } from './scenes/IntroScene';
import { OutroScene } from './scenes/OutroScene';
import { Short01 } from './scenes/Short01';
import { ChannelBanner } from './scenes/ChannelBanner';
import { ProfilePicture } from './scenes/ProfilePicture';
import { CartoonVideo } from './cartoon/CartoonVideo';
import { CARTOON_TOTAL } from './cartoon/theme';
import { TOTAL_FRAMES } from './utils/timings';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Main demo video (no intro/outro) */}
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={TOTAL_FRAMES}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Full video: intro + main + outro */}
      <Composition
        id="FullVideo"
        component={FullVideo}
        durationInFrames={1335}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Standalone intro */}
      <Composition
        id="ChannelIntro"
        component={IntroScene}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Standalone outro */}
      <Composition
        id="ChannelOutro"
        component={OutroScene}
        durationInFrames={240}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* YouTube Short #1: Prompt to Video (vertical) */}
      <Composition
        id="Short01"
        component={Short01}
        durationInFrames={1650}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* Cartoon: Geo-Politics & Conspiracy Theory */}
      <Composition
        id="CartoonGeoPolitics"
        component={CartoonVideo}
        durationInFrames={CARTOON_TOTAL}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* Channel art: banner and profile picture */}
      <Still id="ChannelBanner" component={ChannelBanner} width={2560} height={1440} />
      <Still id="ProfilePicture" component={ProfilePicture} width={800} height={800} />
    </>
  );
};
