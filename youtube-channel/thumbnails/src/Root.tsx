import React from 'react';
import { Composition, Still } from 'remotion';
import { Thumb01_PromptToVideo } from './compositions/Thumb01_PromptToVideo';
import { Thumb02_StockSim } from './compositions/Thumb02_StockSim';
import { Thumb03_RemotionGuide } from './compositions/Thumb03_RemotionGuide';
import { Thumb04_ClaudeCode } from './compositions/Thumb04_ClaudeCode';
import { Thumb05_Workflow } from './compositions/Thumb05_Workflow';

export const RemotionRoot: React.FC = () => (
  <>
    <Still id="Thumb01-PromptToVideo" component={Thumb01_PromptToVideo} width={1280} height={720} />
    <Still id="Thumb02-StockSim" component={Thumb02_StockSim} width={1280} height={720} />
    <Still id="Thumb03-RemotionGuide" component={Thumb03_RemotionGuide} width={1280} height={720} />
    <Still id="Thumb04-ClaudeCode" component={Thumb04_ClaudeCode} width={1280} height={720} />
    <Still id="Thumb05-Workflow" component={Thumb05_Workflow} width={1280} height={720} />
  </>
);
