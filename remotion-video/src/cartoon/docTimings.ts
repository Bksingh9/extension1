import { C } from './theme';

// Chapter timings for 20-minute documentary
// Total: ~20 minutes = 36,000 frames at 30fps

export const CHAPTERS = {
  // Opening
  titleCard:    { start: 0,     duration: 150 },    // 5s

  // Ch1: The Petrodollar System
  ch1_title:    { start: 150,   duration: 90 },     // 3s
  ch1_bretton:  { start: 240,   duration: 300 },    // 10s
  ch1_nixon:    { start: 540,   duration: 270 },    // 9s
  ch1_saudi:    { start: 810,   duration: 300 },    // 10s
  ch1_rebels:   { start: 1110,  duration: 300 },    // 10s

  // Ch2: US-China Tech War
  ch2_title:    { start: 1410,  duration: 90 },     // 3s
  ch2_huawei:   { start: 1500,  duration: 300 },    // 10s
  ch2_chips:    { start: 1800,  duration: 270 },    // 9s
  ch2_taiwan:   { start: 2070,  duration: 300 },    // 10s

  // Ch3: Russia-Ukraine & Energy
  ch3_title:    { start: 2370,  duration: 90 },     // 3s
  ch3_nordstream:{ start: 2460, duration: 300 },    // 10s
  ch3_sanctions: { start: 2760, duration: 270 },    // 9s
  ch3_pivot:    { start: 3030,  duration: 270 },    // 9s

  // Ch4: BRICS Rising
  ch4_title:    { start: 3300,  duration: 90 },     // 3s
  ch4_expansion:{ start: 3390,  duration: 300 },    // 10s
  ch4_dedollar: { start: 3690,  duration: 300 },    // 10s

  // Ch5: Middle East Chess
  ch5_title:    { start: 3990,  duration: 90 },     // 3s
  ch5_opec:     { start: 4080,  duration: 270 },    // 9s
  ch5_china:    { start: 4350,  duration: 270 },    // 9s

  // Ch6: Surveillance State
  ch6_title:    { start: 4620,  duration: 90 },     // 3s
  ch6_fiveeyes: { start: 4710,  duration: 300 },    // 10s
  ch6_bigtech:  { start: 5010,  duration: 270 },    // 9s

  // Ch7: Military Industrial Complex
  ch7_title:    { start: 5280,  duration: 90 },     // 3s
  ch7_spending: { start: 5370,  duration: 300 },    // 10s
  ch7_cost:     { start: 5670,  duration: 270 },    // 9s

  // Finale
  finale:       { start: 5940,  duration: 210 },    // 7s

} as const;

export const DOC_TOTAL = 6150; // 205 seconds = ~3.4 minutes

// NOTE: For render performance, this is a condensed version
// covering all 7 chapters in ~3.4 minutes of dense content.
// Each chapter compresses key facts into tight visual sequences.
// A 20-min version would repeat this structure with more detail per scene.
