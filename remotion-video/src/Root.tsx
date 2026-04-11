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
import { DocVideo } from './cartoon/DocVideo';
import { CARTOON_TOTAL } from './cartoon/theme';
import { DOC_TOTAL } from './cartoon/docTimings';
import { TOTAL_FRAMES } from './utils/timings';

// YouTube Shorts (9:16 vertical)
import { Short_Petrodollar } from './cartoon/shorts/Short_Petrodollar';
import { Short_ChipWar } from './cartoon/shorts/Short_ChipWar';
import { Short_NordStream } from './cartoon/shorts/Short_NordStream';
import { Short_BRICS } from './cartoon/shorts/Short_BRICS';
import { Short_Oil } from './cartoon/shorts/Short_Oil';
import { Short_Surveillance } from './cartoon/shorts/Short_Surveillance';
import { Short_WarMachine } from './cartoon/shorts/Short_WarMachine';

// Geo-Politics Channel Branding
import { GeoPoliticsBanner } from './cartoon/branding/GeoPoliticsBanner';
import { GeoPoliticsProfile } from './cartoon/branding/GeoPoliticsProfile';
import {
  Thumb_Documentary,
  Thumb_Petrodollar,
  Thumb_ChipWar,
  Thumb_NordStream,
  Thumb_BRICS,
  Thumb_Oil,
  Thumb_Surveillance,
  Thumb_WarMachine,
} from './cartoon/branding/Thumbnail';

const SHORT_DURATION = 1710; // 57 seconds (3s hook + 42s facts + 12s CTA)

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

      {/* Documentary: Geo-Politics Deep Dive (7 chapters, real data) */}
      <Composition
        id="GeoPoliticsDoc"
        component={DocVideo}
        durationInFrames={DOC_TOTAL}
        fps={30}
        width={1920}
        height={1080}
      />

      {/* ═══ YouTube Shorts (9:16 vertical, 57s each) ═══ */}
      <Composition id="Short-Petrodollar" component={Short_Petrodollar} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-ChipWar" component={Short_ChipWar} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-NordStream" component={Short_NordStream} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-BRICS" component={Short_BRICS} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-Oil" component={Short_Oil} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-Surveillance" component={Short_Surveillance} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />
      <Composition id="Short-WarMachine" component={Short_WarMachine} durationInFrames={SHORT_DURATION} fps={30} width={1080} height={1920} />

      {/* Channel art: banner and profile picture (Dev Tool channel) */}
      <Still id="ChannelBanner" component={ChannelBanner} width={2560} height={1440} />
      <Still id="ProfilePicture" component={ProfilePicture} width={800} height={800} />

      {/* ═══ Geo-Politics Channel Branding ═══ */}
      <Still id="GeoBanner" component={GeoPoliticsBanner} width={2560} height={1440} />
      <Still id="GeoProfile" component={GeoPoliticsProfile} width={800} height={800} />

      {/* ═══ YouTube Thumbnails (1280x720) ═══ */}
      <Still id="Thumb-Documentary" component={Thumb_Documentary} width={1280} height={720} />
      <Still id="Thumb-Petrodollar" component={Thumb_Petrodollar} width={1280} height={720} />
      <Still id="Thumb-ChipWar" component={Thumb_ChipWar} width={1280} height={720} />
      <Still id="Thumb-NordStream" component={Thumb_NordStream} width={1280} height={720} />
      <Still id="Thumb-BRICS" component={Thumb_BRICS} width={1280} height={720} />
      <Still id="Thumb-Oil" component={Thumb_Oil} width={1280} height={720} />
      <Still id="Thumb-Surveillance" component={Thumb_Surveillance} width={1280} height={720} />
      <Still id="Thumb-WarMachine" component={Thumb_WarMachine} width={1280} height={720} />
    </>
  );
};
