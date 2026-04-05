// Cartoon Geo-Politics Theme
// Bold, saturated, comic-book inspired palette

export const C = {
  // Backgrounds
  bgDark: '#1a1025',
  bgPanel: '#231535',
  bgMap: '#0f1929',

  // Character colors
  charRed: '#e74c3c',
  charBlue: '#3498db',
  charGold: '#f1c40f',
  charGreen: '#2ecc71',
  charPurple: '#9b59b6',
  charOrange: '#e67e22',

  // UI
  speechBg: '#ffffff',
  speechBorder: '#2c3e50',
  speechText: '#1a1a2e',
  captionBg: 'rgba(0,0,0,0.75)',

  // Map colors
  mapLand: '#2c3e50',
  mapOcean: '#1a2533',
  mapHighlight: '#e74c3c',
  mapLine: '#f1c40f',

  // Accents
  danger: '#e74c3c',
  warning: '#f39c12',
  info: '#3498db',
  mystery: '#8e44ad',
  glow: '#f1c40f',

  // Text
  textWhite: '#ecf0f1',
  textLight: '#bdc3c7',
  textDark: '#2c3e50',
  textAccent: '#f1c40f',

  // Outline
  outline: '#2c3e50',
  outlineLight: '#34495e',
} as const;

export const CFONT = {
  title: 'Impact, "Arial Black", sans-serif',
  body: '"Comic Sans MS", "Chalkboard SE", cursive, sans-serif',
  mono: '"Courier New", monospace',
  caption: 'Georgia, serif',
} as const;

// Scene timings (frames at 30fps)
export const CARTOON_SCENES = {
  intro:      { start: 0,    duration: 120 },  // 4s - Title card
  scene1:     { start: 120,  duration: 210 },  // 7s - "The World Stage"
  scene2:     { start: 330,  duration: 240 },  // 8s - "Follow the Money"
  scene3:     { start: 570,  duration: 210 },  // 7s - "The Shadow Players"
  scene4:     { start: 780,  duration: 210 },  // 7s - "The Domino Effect"
  scene5:     { start: 990,  duration: 180 },  // 6s - "What They Don't Tell You"
  outro:      { start: 1170, duration: 120 },  // 4s - CTA
} as const;

export const CARTOON_TOTAL = 1290; // 43 seconds
