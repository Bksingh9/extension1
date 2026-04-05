import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { C } from './theme';
import { CHAPTERS } from './docTimings';

// Components
import { ChapterTitle } from './components/ChapterTitle';
import { FactSequence } from './components/FactSequence';
import { DataBars } from './components/DataBars';
import { VsPanel } from './components/VsPanel';
import { QuoteSlide } from './components/QuoteSlide';
import { IntroCard } from './scenes/IntroCard';
import { OutroCard } from './scenes/OutroCard';
import { WorldMap } from './components/WorldMap';
import { CartoonBg } from './components/CartoonBg';
import { BigCaption } from './components/BigCaption';

// ============ MAIN DOCUMENTARY ============

export const DocVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0518' }}>

      {/* ===== TITLE CARD ===== */}
      <Sequence from={CHAPTERS.titleCard.start} durationInFrames={CHAPTERS.titleCard.duration}>
        <IntroCard />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 1: THE PETRODOLLAR SYSTEM            */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch1_title.start} durationInFrames={CHAPTERS.ch1_title.duration}>
        <ChapterTitle chapter={1} title="The Petrodollar" subtitle="How the US dollar conquered world trade" color={C.charGold} icon="💵" />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_bretton.start} durationInFrames={CHAPTERS.ch1_bretton.duration}>
        <FactSequence
          title="Birth of Dollar Dominance"
          titleColor={C.charGold}
          facts={[
            { year: '1944', text: 'Bretton Woods: 44 nations peg currencies to USD', detail: 'Dollar pegged to gold at $35/oz — the new world order', color: C.charGold, icon: '🏛️' },
            { year: '1971', text: 'Nixon Shock: US abandons gold standard', detail: 'Dollar becomes pure fiat — backed by nothing but trust', color: C.danger, icon: '💥' },
            { year: '1974', text: 'Kissinger-Saudi deal: oil priced in USD only', detail: 'Saudis get military protection, US gets petrodollar monopoly', color: C.charGold, icon: '🤝' },
            { year: 'NOW', text: '88% of forex transactions involve the dollar', detail: '40-50% of global trade invoiced in USD. 59% of reserves held in USD', color: C.charBlue, icon: '🌍' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_nixon.start} durationInFrames={CHAPTERS.ch1_nixon.duration}>
        <DataBars
          title="Dollar's Global Grip"
          titleColor={C.charGold}
          subtitle="Why the whole world dances to the dollar's tune"
          bars={[
            { label: 'Forex transactions involving USD', value: 88, maxValue: 100, displayValue: '88%', color: C.charGold, icon: '💱' },
            { label: 'Global oil trade in USD', value: 80, maxValue: 100, displayValue: '~80%', color: C.charOrange, icon: '🛢️' },
            { label: 'World reserves in USD', value: 59, maxValue: 100, displayValue: '59%', color: C.charBlue, icon: '🏦' },
            { label: 'Global trade invoiced in USD', value: 45, maxValue: 100, displayValue: '~45%', color: C.charGreen, icon: '📦' },
            { label: 'USD share in 2000 (was higher)', value: 71, maxValue: 100, displayValue: '71%', color: C.textMuted, icon: '📉' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_saudi.start} durationInFrames={CHAPTERS.ch1_saudi.duration}>
        <VsPanel
          title="The Petrodollar Deal"
          titleColor={C.charGold}
          left={{
            name: 'UNITED STATES',
            color: C.charBlue,
            points: ['Military protection', 'Arms sales', 'Political alliance'],
            expression: 'suspicious',
            accessory: 'tie',
            quote: 'Price oil in dollars... or else.',
          }}
          right={{
            name: 'SAUDI ARABIA',
            color: C.charGreen,
            points: ['Oil priced in USD', 'Buy US Treasury bonds', 'Invest petrodollars in US'],
            expression: 'neutral',
            accessory: 'crown',
            quote: 'We get security, you get dominance.',
          }}
          bottomQuote="This deal made the dollar the world's de facto currency — without a vote."
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_rebels.start} durationInFrames={CHAPTERS.ch1_rebels.duration}>
        <FactSequence
          title="Those Who Challenged the Dollar"
          titleColor={C.danger}
          facts={[
            { year: '2000', text: 'Iraq switches oil sales to euros', detail: 'Saddam Hussein under UN Oil-for-Food program', color: C.charOrange, icon: '🇮🇶' },
            { year: '2003', text: 'US invades Iraq — oil switched back to dollars', detail: 'Coincidence? $1.9 trillion war cost', color: C.danger, icon: '💣' },
            { year: '2011', text: 'Libya proposes gold-backed African currency', detail: 'Gaddafi plans gold dinar for oil trade', color: C.charGold, icon: '🇱🇾' },
            { year: '2011', text: 'NATO intervenes — Gaddafi killed', detail: 'Gold dinar plan dies with him. Another coincidence?', color: C.danger, icon: '⚔️' },
            { year: '2017', text: 'Venezuela prices oil in yuan', detail: 'Faces severe US sanctions', color: C.charPurple, icon: '🇻🇪' },
            { year: '2008+', text: 'Iran trades oil in euros', detail: 'Under escalating sanctions since 1979', color: C.mystery, icon: '🇮🇷' },
          ]}
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 2: US-CHINA TECH WAR                 */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch2_title.start} durationInFrames={CHAPTERS.ch2_title.duration}>
        <ChapterTitle chapter={2} title="The Chip War" subtitle="US vs China — the battle for technological supremacy" color={C.charBlue} icon="🔬" />
      </Sequence>

      <Sequence from={CHAPTERS.ch2_huawei.start} durationInFrames={CHAPTERS.ch2_huawei.duration}>
        <FactSequence
          title="The Huawei Takedown"
          titleColor={C.charBlue}
          facts={[
            { year: '2019', text: 'Huawei placed on Entity List — banned from US tech', detail: 'Cited: national security, espionage concerns', color: C.charBlue, icon: '🚫' },
            { year: '2020', text: 'Total chip cutoff — no US tech anywhere in supply chain', detail: 'Huawei phone sales crash: 240M → 35M units in 2 years', color: C.danger, icon: '📱' },
            { year: '2022', text: 'CHIPS Act: $52.7 billion to build US chip fabs', detail: '25% tax credit for semiconductor manufacturing', color: C.charGold, icon: '🏭' },
            { year: '2022', text: 'Sweeping export controls on China', detail: 'Advanced chips, equipment, even US persons restricted', color: C.danger, icon: '🔒' },
            { year: '2023', text: 'Huawei fights back with 7nm Kirin chip', detail: 'Made by SMIC — shocked analysts who said it was impossible', color: C.charRed, icon: '🔥' },
            { year: 'NOW', text: 'China controls 60% of rare earth mining, 90% of processing', detail: 'The ultimate leverage in the tech supply chain', color: C.charRed, icon: '⛏️' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch2_chips.start} durationInFrames={CHAPTERS.ch2_chips.duration}>
        <VsPanel
          title="The Tech Decoupling"
          titleColor={C.charBlue}
          left={{
            name: 'UNITED STATES',
            color: C.charBlue,
            points: ['CHIPS Act: $52.7B', 'Export controls', 'TSMC Arizona: $65B', 'TikTok ban'],
            expression: 'angry',
            accessory: 'tie',
            quote: 'No advanced chips for China.',
          }}
          right={{
            name: 'CHINA',
            color: C.charRed,
            points: ['Kirin 9000S chip', '60% rare earths', '$279B trade surplus', '150M TikTok US users'],
            expression: 'suspicious',
            accessory: 'hat',
            quote: 'We will be self-sufficient.',
          }}
          bottomQuote="$500+ billion in annual bilateral trade — and growing hostility."
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch2_taiwan.start} durationInFrames={CHAPTERS.ch2_taiwan.duration}>
        <DataBars
          title="The Taiwan Chip Bottleneck"
          titleColor={C.danger}
          subtitle="TSMC makes 90% of the world's most advanced chips — on one island"
          bars={[
            { label: 'TSMC: Advanced chips (sub-7nm)', value: 90, maxValue: 100, displayValue: '90%', color: C.danger, icon: '🇹🇼' },
            { label: 'TSMC 2023 Revenue', value: 69, maxValue: 100, displayValue: '$69B', color: C.charGold, icon: '💰' },
            { label: 'TSMC Arizona investment', value: 65, maxValue: 100, displayValue: '$65B', color: C.charBlue, icon: '🏗️' },
            { label: 'US-China trade deficit 2023', value: 279, maxValue: 400, displayValue: '$279B', color: C.charOrange, icon: '📊' },
            { label: 'Trade deficit peak (2018)', value: 418, maxValue: 500, displayValue: '$418B', color: C.textMuted, icon: '📉' },
          ]}
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 3: RUSSIA-UKRAINE & ENERGY           */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch3_title.start} durationInFrames={CHAPTERS.ch3_title.duration}>
        <ChapterTitle chapter={3} title="Energy Chess" subtitle="Russia, Europe, and the weaponization of gas" color={C.charOrange} icon="⛽" />
      </Sequence>

      <Sequence from={CHAPTERS.ch3_nordstream.start} durationInFrames={CHAPTERS.ch3_nordstream.duration}>
        <FactSequence
          title="The Nord Stream Saga"
          titleColor={C.charOrange}
          facts={[
            { year: '2011', text: 'Nord Stream 1 operational: 55 bcm/year capacity', detail: '1,224 km under the Baltic Sea. Cost: $7.4 billion', color: C.charBlue, icon: '🔵' },
            { year: '2021', text: 'Nord Stream 2 completed but never opened', detail: 'Cost: $11 billion. Germany suspended certification Feb 22, 2022', color: C.charOrange, icon: '🔴' },
            { year: '2022', text: 'Russia invades Ukraine — energy weapon unleashed', detail: 'Europe scrambles for alternatives', color: C.danger, icon: '💥' },
            { year: 'SEP 22', text: 'Explosions destroy 3 of 4 Nord Stream pipelines', detail: 'Sabotage confirmed. Whodunit? US? Ukraine? Russia? Still unclear.', color: C.danger, icon: '💣' },
            { year: 'BEFORE', text: 'EU imported 40-45% of gas from Russia', detail: 'Germany: 55% of gas from Russia', color: C.charPurple, icon: '🇪🇺' },
            { year: 'AFTER', text: 'Russian pipeline gas to Europe dropped 80%', detail: 'Now ~15% of EU imports. LNG from US, Norway, Qatar fills gap', color: C.charGreen, icon: '📉' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch3_sanctions.start} durationInFrames={CHAPTERS.ch3_sanctions.duration}>
        <DataBars
          title="Sanctions: The Economic War"
          titleColor={C.danger}
          subtitle="$300 billion in Russian assets frozen by Western nations"
          bars={[
            { label: 'Russian reserves frozen', value: 300, maxValue: 400, displayValue: '$300B', color: C.danger, icon: '🧊' },
            { label: 'EU sanction packages', value: 10, maxValue: 15, displayValue: '10+', color: C.charBlue, icon: '📜' },
            { label: 'Russia GDP drop 2022', value: 2.1, maxValue: 10, displayValue: '-2.1%', color: C.charOrange, icon: '📉' },
            { label: 'Russia inflation 2022', value: 12, maxValue: 20, displayValue: '~12%', color: C.warning, icon: '📈' },
            { label: 'Oil price cap (per barrel)', value: 60, maxValue: 120, displayValue: '$60', color: C.charGold, icon: '🛢️' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch3_pivot.start} durationInFrames={CHAPTERS.ch3_pivot.duration}>
        <VsPanel
          title="Russia's Eastern Pivot"
          titleColor={C.charPurple}
          left={{
            name: 'RUSSIA → CHINA',
            color: C.charPurple,
            points: ['$240B bilateral trade (2023)', '90% settled in yuan/rubles', 'Power of Siberia pipeline'],
            expression: 'suspicious',
            accessory: 'hat',
            quote: 'The West cut us off. The East opened up.',
          }}
          right={{
            name: 'RUSSIA → INDIA',
            color: C.charGreen,
            points: ['1.5-2M barrels/day of crude', '$10-30/barrel discounts', 'Russia: India\'s top oil supplier'],
            expression: 'happy',
            accessory: 'none',
            quote: 'Cheap oil? We\'ll take all of it.',
          }}
          bottomQuote="Sanctions pushed Russia into China and India's arms — was that the plan?"
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 4: BRICS RISING                      */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch4_title.start} durationInFrames={CHAPTERS.ch4_title.duration}>
        <ChapterTitle chapter={4} title="BRICS Rising" subtitle="The challenge to Western financial dominance" color={C.charGold} icon="🌍" />
      </Sequence>

      <Sequence from={CHAPTERS.ch4_expansion.start} durationInFrames={CHAPTERS.ch4_expansion.duration}>
        <FactSequence
          title="The BRICS Expansion"
          titleColor={C.charGold}
          facts={[
            { year: '2006', text: 'BRIC formed: Brazil, Russia, India, China', detail: 'The term coined by Goldman Sachs economist Jim O\'Neill', color: C.charGold, icon: '🤝' },
            { year: '2010', text: 'South Africa joins → BRICS', detail: 'Now: 40% of world population, 26% of GDP', color: C.charGreen, icon: '🇿🇦' },
            { year: '2014', text: 'New Development Bank created in Shanghai', detail: '$50B capital, $30B+ in loans approved', color: C.charBlue, icon: '🏦' },
            { year: '2023', text: '6 new nations invited: Saudi, Iran, UAE, Egypt, Ethiopia', detail: 'Argentina invited but declined under new president Milei', color: C.charOrange, icon: '📢' },
            { year: '2024', text: '5 new members officially join', detail: 'BRICS+ now represents even more of global GDP and population', color: C.charGold, icon: '🌐' },
            { year: 'KEY', text: 'Saudi Arabia at the table — petrodollar implications', detail: 'Saudi joined Shanghai Cooperation Organisation as dialogue partner', color: C.danger, icon: '⚠️' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch4_dedollar.start} durationInFrames={CHAPTERS.ch4_dedollar.duration}>
        <DataBars
          title="De-Dollarization in Action"
          titleColor={C.danger}
          subtitle="Central banks buying gold at record rates. Is the dollar losing its grip?"
          bars={[
            { label: 'Central bank gold buying 2022', value: 1136, maxValue: 1200, displayValue: '1,136 tonnes', color: C.charGold, icon: '🥇' },
            { label: 'Central bank gold buying 2023', value: 1037, maxValue: 1200, displayValue: '1,037 tonnes', color: C.charGold, icon: '🥇' },
            { label: 'China US Treasury holdings (peak)', value: 1300, maxValue: 1500, displayValue: '$1.3T → $775B', color: C.charRed, icon: '📉' },
            { label: 'Yuan share of global payments', value: 3.6, maxValue: 50, displayValue: '3.6% (was <2%)', color: C.charRed, icon: '💹' },
            { label: 'Dollar share of global payments', value: 47, maxValue: 50, displayValue: '~47%', color: C.charBlue, icon: '💵' },
          ]}
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 5: MIDDLE EAST CHESS                  */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch5_title.start} durationInFrames={CHAPTERS.ch5_title.duration}>
        <ChapterTitle chapter={5} title="Middle East Chess" subtitle="Oil, power, and shifting alliances" color={C.charOrange} icon="♟️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch5_opec.start} durationInFrames={CHAPTERS.ch5_opec.duration}>
        <FactSequence
          title="OPEC+ Moves the Board"
          titleColor={C.charOrange}
          facts={[
            { year: 'APR 20', text: 'Oil goes NEGATIVE: -$37.63/barrel', detail: 'COVID collapse + storage shortage = unprecedented', color: C.danger, icon: '📉' },
            { year: 'JUN 22', text: 'Oil surges to $120/barrel after Ukraine invasion', detail: 'Europe scrambles, prices skyrocket', color: C.charGold, icon: '📈' },
            { year: 'OCT 22', text: 'OPEC+ cuts 2 million barrels/day', detail: 'Largest cut since 2020 — defying US pressure', color: C.charOrange, icon: '✂️' },
            { year: '2023', text: 'Saudi adds voluntary 1M bpd cut', detail: 'Extended multiple times to prop up prices', color: C.charGreen, icon: '🇸🇦' },
            { year: 'KEY', text: 'OPEC+ controls 40% of oil production, 80% of reserves', detail: 'They decide who prospers and who pays', color: C.glow, icon: '⚡' },
            { year: '2019', text: 'Saudi Aramco IPO: $25.6B — largest IPO ever', detail: 'Briefly world\'s most valuable company at $2.4T', color: C.charGold, icon: '💰' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch5_china.start} durationInFrames={CHAPTERS.ch5_china.duration}>
        <VsPanel
          title="China Brokers Middle East Peace"
          titleColor={C.charRed}
          left={{
            name: 'SAUDI ARABIA',
            color: C.charGreen,
            points: ['Cut ties with Iran in 2016', 'Abraham Accords with Israel', 'OPEC+ production control'],
            expression: 'neutral',
            accessory: 'crown',
            quote: 'We\'re diversifying our alliances.',
          }}
          right={{
            name: 'IRAN',
            color: C.charPurple,
            points: ['Under US sanctions since 1979', 'Oil bourse trades in euros', 'Yemen proxy war vs Saudi'],
            expression: 'angry',
            accessory: 'none',
            quote: 'The enemy of our enemy...',
          }}
          bottomQuote="March 2023: China brokers Saudi-Iran peace deal in Beijing. A seismic shift."
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 6: SURVEILLANCE STATE                 */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch6_title.start} durationInFrames={CHAPTERS.ch6_title.duration}>
        <ChapterTitle chapter={6} title="The Watchers" subtitle="Surveillance, data, and the death of privacy" color={C.mystery} icon="👁️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch6_fiveeyes.start} durationInFrames={CHAPTERS.ch6_fiveeyes.duration}>
        <FactSequence
          title="Snowden Revealed the Machine"
          titleColor={C.mystery}
          facts={[
            { year: '1946', text: 'Five Eyes alliance formed: US, UK, Canada, Australia, NZ', detail: 'UKUSA Agreement — the oldest intelligence-sharing pact', color: C.charBlue, icon: '👁️' },
            { year: '2013', text: 'Edward Snowden leaks NSA PRISM program', detail: 'Direct access to Google, Facebook, Apple, Microsoft servers', color: C.danger, icon: '💥' },
            { year: '2013', text: 'XKeyscore: search anyone\'s emails and browsing', detail: 'No prior authorization needed for analysts', color: C.danger, icon: '🔍' },
            { year: '2013', text: 'Bulk phone metadata collection revealed', detail: 'Every US domestic call recorded under Section 215', color: C.mystery, icon: '📞' },
            { year: '2022', text: 'Snowden granted Russian citizenship', detail: 'Fled Hong Kong → Russia. Hero or traitor? You decide.', color: C.charPurple, icon: '🇷🇺' },
            { year: 'NOW', text: 'China: 500-600 million surveillance cameras', detail: '20M+ flights blocked by social credit system', color: C.charRed, icon: '📷' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch6_bigtech.start} durationInFrames={CHAPTERS.ch6_bigtech.duration}>
        <DataBars
          title="Big Tech Knows Everything"
          titleColor={C.mystery}
          subtitle="They sell your data. Governments buy your silence."
          bars={[
            { label: 'Google searches per day', value: 85, maxValue: 100, displayValue: '8.5 billion', color: C.charBlue, icon: '🔍' },
            { label: 'Meta monthly users', value: 75, maxValue: 100, displayValue: '3 billion', color: C.charBlue, icon: '👤' },
            { label: 'Meta ad revenue (data-driven)', value: 131, maxValue: 200, displayValue: '$131B/yr', color: C.charGold, icon: '💰' },
            { label: 'US data broker industry', value: 200, maxValue: 300, displayValue: '$200B+/yr', color: C.danger, icon: '🏢' },
            { label: 'GDPR fines total', value: 40, maxValue: 100, displayValue: '$4B+', color: C.charGreen, icon: '⚖️' },
            { label: 'Largest fine: Meta (2023)', value: 12, maxValue: 20, displayValue: '$1.2B', color: C.danger, icon: '🔨' },
          ]}
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 7: MILITARY INDUSTRIAL COMPLEX        */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch7_title.start} durationInFrames={CHAPTERS.ch7_title.duration}>
        <ChapterTitle chapter={7} title="War Machine" subtitle="$886 billion/year — who profits from conflict?" color={C.danger} icon="⚔️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch7_spending.start} durationInFrames={CHAPTERS.ch7_spending.duration}>
        <DataBars
          title="Follow the Defense Dollars"
          titleColor={C.danger}
          subtitle="US spends more than the next 10 nations combined — $886B in 2023"
          bars={[
            { label: 'United States', value: 886, maxValue: 900, displayValue: '$886B', color: C.charBlue, icon: '🇺🇸' },
            { label: 'Lockheed Martin (revenue)', value: 67, maxValue: 900, displayValue: '$67B', color: C.charOrange, icon: '🛩️' },
            { label: 'RTX/Raytheon (defense)', value: 39, maxValue: 900, displayValue: '$39B', color: C.charOrange, icon: '🚀' },
            { label: 'Northrop Grumman', value: 39, maxValue: 900, displayValue: '$39B', color: C.charOrange, icon: '✈️' },
            { label: 'F-35 lifetime cost', value: 850, maxValue: 1700, displayValue: '$1.7 TRILLION', color: C.danger, icon: '💸' },
            { label: 'US military bases worldwide', value: 750, maxValue: 800, displayValue: '750+ in 80+ countries', color: C.mystery, icon: '🗺️' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch7_cost.start} durationInFrames={CHAPTERS.ch7_cost.duration}>
        <FactSequence
          title="The True Cost of War"
          titleColor={C.danger}
          facts={[
            { year: '2001-21', text: 'Afghanistan War: $2.3 trillion direct cost', detail: 'Including veteran care: $4+ trillion projected', color: C.danger, icon: '🇦🇫' },
            { year: '2003-11', text: 'Iraq War: $1.9-2 trillion direct cost', detail: 'Long-term: $3+ trillion with veteran care', color: C.danger, icon: '🇮🇶' },
            { year: 'TOTAL', text: 'Post-9/11 wars: $8+ trillion, 900,000+ deaths', detail: 'Brown University Costs of War Project', color: C.danger, icon: '💀' },
            { year: 'DOOR', text: '1,700+ senior officials → defense contractors', detail: 'The revolving door between Pentagon and industry', color: C.mystery, icon: '🚪' },
            { year: 'ARMS', text: 'US is world\'s #1 arms exporter: 40% of global sales', detail: 'Top buyers: Saudi Arabia, Australia, Japan, NATO allies', color: C.charGold, icon: '🔫' },
          ]}
        />
      </Sequence>

      {/* ===== FINALE ===== */}
      <Sequence from={CHAPTERS.finale.start} durationInFrames={CHAPTERS.finale.duration}>
        <OutroCard />
      </Sequence>

    </AbsoluteFill>
  );
};
