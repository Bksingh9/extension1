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
          title="How One Currency Conquered Earth"
          titleColor={C.charGold}
          facts={[
            { year: '1944', text: 'Bretton Woods: 44 nations "voluntarily" peg to USD', detail: 'Translation: The guy with all the gold makes the rules. $35/oz.', color: C.charGold, icon: '🏛️' },
            { year: '1971', text: 'Nixon ditches gold standard — "Trust me bro"', detail: 'Dollar now backed by vibes, aircraft carriers, and audacity', color: C.danger, icon: '💥' },
            { year: '1974', text: 'Kissinger to Saudi: "Price oil in dollars... or else"', detail: 'The "or else" came with a very large military brochure', color: C.charGold, icon: '🤝' },
            { year: 'NOW', text: '88% of forex transactions involve the dollar', detail: 'The whole planet uses it. Not because they love it.', color: C.charBlue, icon: '🌍' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_nixon.start} durationInFrames={CHAPTERS.ch1_nixon.duration}>
        <DataBars
          title="Dollar's Global Grip"
          titleColor={C.charGold}
          subtitle="Spoiler: It's not because of freedom and democracy"
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
            quote: 'Nice oil you got there. Would be a shame if someone... liberated it.',
          }}
          right={{
            name: 'SAUDI ARABIA',
            color: C.charGreen,
            points: ['Oil priced in USD', 'Buy US Treasury bonds', 'Invest petrodollars in US'],
            expression: 'smug',
            accessory: 'crown',
            quote: 'We get palaces, you get world domination. Deal.',
          }}
          bottomQuote="The most important handshake in history — and you weren't invited."
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch1_rebels.start} durationInFrames={CHAPTERS.ch1_rebels.duration}>
        <FactSequence
          title="What Happens When You Ditch the Dollar"
          titleColor={C.danger}
          facts={[
            { year: '2000', text: 'Iraq switches oil sales to euros', detail: 'Saddam: "I\'ll use euros." Narrator: This was a mistake.', color: C.charOrange, icon: '🇮🇶' },
            { year: '2003', text: 'US invades Iraq — oil switched back to dollars', detail: '"WMDs" never found. But the dollar was restored. Coincidence? 🤷', color: C.danger, icon: '💣' },
            { year: '2011', text: 'Libya proposes gold-backed African currency', detail: 'Gaddafi: "Africa should have its own money!" NATO: "lol no"', color: C.charGold, icon: '🇱🇾' },
            { year: '2011', text: 'NATO intervenes — Gaddafi killed', detail: 'Gold dinar dies with him. Detecting a pattern yet?', color: C.danger, icon: '⚔️' },
            { year: '2017', text: 'Venezuela prices oil in yuan', detail: 'Immediately sanctioned into the shadow realm', color: C.charPurple, icon: '🇻🇪' },
            { year: '2008+', text: 'Iran trades oil in euros', detail: 'Has been on America\'s naughty list since 1979', color: C.mystery, icon: '🇮🇷' },
          ]}
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 2: US-CHINA TECH WAR                 */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch2_title.start} durationInFrames={CHAPTERS.ch2_title.duration}>
        <ChapterTitle chapter={2} title="The Chip War" subtitle="Two superpowers fighting over sand. Expensive sand." color={C.charBlue} icon="🔬" />
      </Sequence>

      <Sequence from={CHAPTERS.ch2_huawei.start} durationInFrames={CHAPTERS.ch2_huawei.duration}>
        <FactSequence
          title="Operation: Delete Huawei"
          titleColor={C.charBlue}
          facts={[
            { year: '2019', text: 'Huawei banned — "national security concerns"', detail: 'Translation: They were about to beat us at 5G and we panicked', color: C.charBlue, icon: '🚫' },
            { year: '2020', text: 'Total chip cutoff — scorched earth policy', detail: 'Huawei phone sales: 240M → 35M. Mission accomplished?', color: C.danger, icon: '📱' },
            { year: '2022', text: 'CHIPS Act: $52.7B of taxpayer money for chip fabs', detail: 'Corporate welfare is fine when you call it "national security"', color: C.charGold, icon: '🏭' },
            { year: '2022', text: 'Export controls: "No chips for you, China"', detail: 'Even US citizens banned from helping. Land of the free!', color: C.danger, icon: '🔒' },
            { year: '2023', text: 'Huawei builds 7nm chip anyway', detail: 'Analysts: "Impossible!" Huawei: "Hold my baijiu." 🍶', color: C.charRed, icon: '🔥' },
            { year: 'NOW', text: 'China owns 60% of rare earths, processes 90%', detail: 'Awkward when you need your rival to make your weapons', color: C.charRed, icon: '⛏️' },
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
            quote: 'No chips for you! Also please keep making our iPhones.',
          }}
          right={{
            name: 'CHINA',
            color: C.charRed,
            points: ['Built their own chip anyway', '60% of YOUR rare earths', '$279B trade surplus', '150M Americans addicted to TikTok'],
            expression: 'smug',
            accessory: 'hat',
            quote: 'Self-sufficient? We already own the supply chain.',
          }}
          bottomQuote="$500B in trade annually. They hate each other but can't break up. It's complicated."
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch2_taiwan.start} durationInFrames={CHAPTERS.ch2_taiwan.duration}>
        <DataBars
          title="The Taiwan Chip Bottleneck"
          titleColor={C.danger}
          subtitle="90% of advanced chips made on one island. What could go wrong?"
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
        <ChapterTitle chapter={3} title="Energy Chess" subtitle="Europe bet everything on Russian gas. Spoiler: bad idea." color={C.charOrange} icon="⛽" />
      </Sequence>

      <Sequence from={CHAPTERS.ch3_nordstream.start} durationInFrames={CHAPTERS.ch3_nordstream.duration}>
        <FactSequence
          title="The $18 Billion Underwater Oopsie"
          titleColor={C.charOrange}
          facts={[
            { year: '2011', text: 'Nord Stream 1: 1,224 km pipe under the Baltic Sea', detail: '$7.4 billion to build. Europe\'s addiction to cheap gas: priceless', color: C.charBlue, icon: '🔵' },
            { year: '2021', text: 'Nord Stream 2 completed but never turned on', detail: '$11 billion paperweight. Germany "suspended" it. Chef\'s kiss.', color: C.charOrange, icon: '🔴' },
            { year: '2022', text: 'Russia invades Ukraine — turns off the gas tap', detail: '"Nice economy you have there, Europe. Shame if it got cold."', color: C.danger, icon: '💥' },
            { year: 'SEP 22', text: 'Someone blows up 3 of 4 pipelines', detail: 'Whodunit? US denies it. Russia denies it. Everyone looks suspicious.', color: C.danger, icon: '💣' },
            { year: 'BEFORE', text: 'EU got 40-45% of gas from Russia', detail: 'Germany: 55%. "Energy dependency? Nah, it\'s a partnership!" 🤡', color: C.charPurple, icon: '🇪🇺' },
            { year: 'AFTER', text: 'Russian gas to Europe dropped 80%', detail: 'Now buying expensive US LNG. Freedom gas isn\'t free.', color: C.charGreen, icon: '📉' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch3_sanctions.start} durationInFrames={CHAPTERS.ch3_sanctions.duration}>
        <DataBars
          title="Sanctions: The Economic War"
          titleColor={C.danger}
          subtitle="$300B frozen. Russia: 'That's fine, we didn't need it anyway.'"
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
            quote: 'You sanctioned us into a friendship with the world\'s factory.',
          }}
          right={{
            name: 'RUSSIA → INDIA',
            color: C.charGreen,
            points: ['1.5-2M barrels/day of crude', '$10-30/barrel discounts', 'Russia: India\'s #1 oil supplier now'],
            expression: 'happy',
            accessory: 'none',
            quote: 'Sanctions = cheap oil for us. Thanks, West!',
          }}
          bottomQuote="The West: 'We'll isolate Russia!' Russia: *makes new friends* 'K.'"
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 4: BRICS RISING                      */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch4_title.start} durationInFrames={CHAPTERS.ch4_title.duration}>
        <ChapterTitle chapter={4} title="BRICS Rising" subtitle="When the rest of the world starts its own group chat" color={C.charGold} icon="🌍" />
      </Sequence>

      <Sequence from={CHAPTERS.ch4_expansion.start} durationInFrames={CHAPTERS.ch4_expansion.duration}>
        <FactSequence
          title="The 'We're Tired of Your Rules' Alliance"
          titleColor={C.charGold}
          facts={[
            { year: '2006', text: 'BRIC formed — named by a Goldman Sachs guy, ironically', detail: 'Wall Street named the alliance that wants to destroy Wall Street', color: C.charGold, icon: '🤝' },
            { year: '2010', text: 'South Africa joins → BRICS', detail: '40% of humanity, 26% of GDP. The "global minority" is actually the majority', color: C.charGreen, icon: '🇿🇦' },
            { year: '2014', text: 'They make their own World Bank. In Shanghai. Flexing.', detail: '$50B capital, $30B+ in loans. No "structural adjustment" required', color: C.charBlue, icon: '🏦' },
            { year: '2023', text: '6 more nations invited — everyone wants in', detail: 'Argentina said yes then elected a libertarian who said no. Drama.', color: C.charOrange, icon: '📢' },
            { year: '2024', text: 'BRICS+ now has Saudi, Iran, UAE, Egypt, Ethiopia', detail: 'The cool kids table just got very crowded', color: C.charGold, icon: '🌐' },
            { year: 'KEY', text: 'Saudi Arabia is hedging its bets', detail: 'Still friends with US. Also friends with China. Playing both sides like a pro.', color: C.danger, icon: '⚠️' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch4_dedollar.start} durationInFrames={CHAPTERS.ch4_dedollar.duration}>
        <DataBars
          title="De-Dollarization in Action"
          titleColor={C.danger}
          subtitle="Central banks hoarding gold like doomsday preppers. Hmm."
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
        <ChapterTitle chapter={5} title="Middle East Chess" subtitle="Where everyone's playing 4D chess and nobody's winning" color={C.charOrange} icon="♟️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch5_opec.start} durationInFrames={CHAPTERS.ch5_opec.duration}>
        <FactSequence
          title="OPEC+: The Original Price Manipulators"
          titleColor={C.charOrange}
          facts={[
            { year: 'APR 20', text: 'Oil goes NEGATIVE. They literally paid you to take it.', detail: '-$37.63/barrel. Storage full. Traders in tears. Beautiful chaos.', color: C.danger, icon: '📉' },
            { year: 'JUN 22', text: 'Oil hits $120/barrel — OPEC pops champagne', detail: 'Your gas bill tripled. Their yacht collection doubled.', color: C.charGold, icon: '📈' },
            { year: 'OCT 22', text: 'OPEC+ cuts 2M barrels/day — middle finger to Biden', detail: 'US: "Please pump more." OPEC: "New phone who dis?"', color: C.charOrange, icon: '✂️' },
            { year: '2023', text: 'Saudi cuts another 1M bpd just because they can', detail: '"Voluntary" cuts. Voluntarily making you pay more.', color: C.charGreen, icon: '🇸🇦' },
            { year: 'KEY', text: 'OPEC+ controls 40% production, 80% of reserves', detail: 'A cartel by any other name would smell as profitable', color: C.glow, icon: '⚡' },
            { year: '2019', text: 'Aramco IPO: $25.6B — casually the biggest ever', detail: '$2.4 TRILLION valuation. Your entire country is worth less.', color: C.charGold, icon: '💰' },
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
            quote: 'Best friends with everyone. Especially whoever has money.',
          }}
          right={{
            name: 'IRAN',
            color: C.charPurple,
            points: ['Sanctioned since before you were born', 'Oil bourse in euros (bold move)', 'Proxy wars as a hobby'],
            expression: 'angry',
            accessory: 'none',
            quote: 'We have been patient for 45 years...',
          }}
          bottomQuote="China brokered their peace deal. In Beijing. While America wasn't looking. Awkward."
        />
      </Sequence>

      {/* ============================================ */}
      {/* CHAPTER 6: SURVEILLANCE STATE                 */}
      {/* ============================================ */}

      <Sequence from={CHAPTERS.ch6_title.start} durationInFrames={CHAPTERS.ch6_title.duration}>
        <ChapterTitle chapter={6} title="The Watchers" subtitle="Your phone knows more about you than your therapist" color={C.mystery} icon="👁️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch6_fiveeyes.start} durationInFrames={CHAPTERS.ch6_fiveeyes.duration}>
        <FactSequence
          title="That One IT Guy Who Ruined Everything"
          titleColor={C.mystery}
          facts={[
            { year: '1946', text: 'Five Eyes formed: 5 countries who pinky-swore to spy together', detail: 'The OG group chat. Still active. Reading yours right now.', color: C.charBlue, icon: '👁️' },
            { year: '2013', text: 'Snowden: "Hey, the NSA reads ALL your stuff"', detail: 'PRISM: direct access to Google, Facebook, Apple servers. Surprise!', color: C.danger, icon: '💥' },
            { year: '2013', text: 'XKeyscore: Google for spies. Search anyone. No warrant.', detail: '"Just trust us" — people who literally built a search engine for your secrets', color: C.danger, icon: '🔍' },
            { year: '2013', text: 'Every US phone call metadata collected. Every. Single. One.', detail: '"We\'re not listening!" (We\'re just recording who, when, where, how long)', color: C.mystery, icon: '📞' },
            { year: '2022', text: 'Snowden gets Russian citizenship. Peak irony.', detail: 'Fled surveillance state → moved to surveillance state. Make it make sense.', color: C.charPurple, icon: '🇷🇺' },
            { year: 'NOW', text: 'China: 600M cameras. One for every 2.4 citizens.', detail: '20M+ flights blocked by social credit. Black Mirror was a documentary.', color: C.charRed, icon: '📷' },
          ]}
        />
      </Sequence>

      <Sequence from={CHAPTERS.ch6_bigtech.start} durationInFrames={CHAPTERS.ch6_bigtech.duration}>
        <DataBars
          title="Big Tech Knows Everything"
          titleColor={C.mystery}
          subtitle="The product is you. You're not even getting a cut."
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
        <ChapterTitle chapter={7} title="War Machine" subtitle="$886B/year. Somebody's making a killing. Literally." color={C.danger} icon="⚔️" />
      </Sequence>

      <Sequence from={CHAPTERS.ch7_spending.start} durationInFrames={CHAPTERS.ch7_spending.duration}>
        <DataBars
          title="Follow the Defense Dollars"
          titleColor={C.danger}
          subtitle="More than the next 10 countries combined. For 'defense'. Sure."
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
          title="The Receipt Nobody Asked For"
          titleColor={C.danger}
          facts={[
            { year: '2001-21', text: 'Afghanistan: $2.3T. Taliban still in charge.', detail: '20 years, $4T+ with vet care. The Taliban waited it out with flip phones.', color: C.danger, icon: '🇦🇫' },
            { year: '2003-11', text: 'Iraq: $2T for WMDs that never existed', detail: 'Long-term: $3T+. Found zero WMDs. Found lots of oil though.', color: C.danger, icon: '🇮🇶' },
            { year: 'TOTAL', text: '$8+ TRILLION. 900,000+ dead. What did we get?', detail: 'Brown University did the math. The Pentagon did not want them to.', color: C.danger, icon: '💀' },
            { year: 'DOOR', text: '1,700 Pentagon officials now work for arms companies', detail: 'Approve the weapons → retire → sell the weapons. Nice gig.', color: C.mystery, icon: '🚪' },
            { year: 'ARMS', text: '#1 arms dealer on Earth. 40% of global weapons sales.', detail: 'Top customer: Saudi Arabia. What they do with them? Don\'t ask.', color: C.charGold, icon: '🔫' },
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
