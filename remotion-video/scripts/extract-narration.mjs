#!/usr/bin/env node
/**
 * Extract narration script from DocVideo.tsx
 * Outputs plain text with pauses for Piper TTS.
 *
 * Usage:
 *   node scripts/extract-narration.mjs > out/narration.txt
 *   piper --model en_US-lessac-medium --output_file out/narration.wav < out/narration.txt
 */

const narration = `
[INTRO]
Who actually runs this planet?
Hint... it's not who you voted for.
Geo-politics. No sugar coating.

...

[CHAPTER 1: THE PETRODOLLAR]
How one currency conquered Earth.

In 1944, 44 nations voluntarily pegged their currencies to the US dollar.
Translation: the guy with all the gold makes the rules. Thirty-five dollars an ounce.

In 1971, Nixon ditched the gold standard. Trust me, bro.
The dollar is now backed by vibes, aircraft carriers, and audacity.

In 1974, Kissinger told Saudi Arabia: price oil in dollars... or else.
The "or else" came with a very large military brochure.

Today, 88 percent of all foreign exchange transactions involve the dollar.
Not because the world loves it. Because they have no choice.

...

Now here's the fun part. What happens when you ditch the dollar?

In 2000, Iraq switched oil sales to euros. In 2003, the US invaded Iraq. Oil went back to dollars. Coincidence? WMDs were never found. But the dollar was restored.

In 2011, Libya proposed a gold-backed African currency. NATO intervened. Gaddafi was killed. The gold dinar died with him. Detecting a pattern yet?

Venezuela priced oil in yuan. Immediately sanctioned into the shadow realm.
Iran trades oil in euros. Has been on America's naughty list since 1979.

...

[CHAPTER 2: THE CHIP WAR]
Two superpowers fighting over sand. Expensive sand.

In 2019, Huawei was banned from US tech. National security concerns. Translation: they were about to beat us at 5G and we panicked.

Total chip cutoff in 2020. Scorched earth policy. Huawei phone sales crashed from 240 million to 35 million units in just two years.

The CHIPS Act threw 52.7 billion dollars of taxpayer money at the problem. Corporate welfare is fine when you call it national security.

But here's the twist. In 2023, Huawei built their own 7-nanometer chip. Analysts said it was impossible. Huawei said: hold my baijiu.

China controls 60 percent of rare earth mining and 90 percent of processing. Awkward when you need your rival to make your weapons.

90 percent of the world's most advanced chips are made by TSMC. On one island. Taiwan. What could possibly go wrong?

...

[CHAPTER 3: ENERGY CHESS]
Europe bet everything on Russian gas. Spoiler: bad idea.

Nord Stream 1: a 1,224-kilometer pipe under the Baltic Sea. 7.4 billion dollars to build. Europe's addiction to cheap gas? Priceless.

Nord Stream 2 was completed but never turned on. An 11-billion-dollar paperweight.

In September 2022, someone blew up three of four pipelines. Sabotage confirmed. The US denies it. Russia denies it. Everyone looks suspicious. Classic.

Before the war, Europe got 40 to 45 percent of its gas from Russia. Germany: 55 percent. Energy dependency? Nah, it's a partnership.

After? Russian gas to Europe dropped 80 percent. Now buying expensive American LNG. Freedom gas isn't free.

Sanctions froze 300 billion dollars of Russian assets. Russia said: that's fine. We don't need it anyway. Then pivoted East.

Russia-China bilateral trade hit 240 billion in 2023. Ninety percent settled in yuan and rubles.
Russia-India: 1.5 to 2 million barrels per day at 10 to 30 dollars discount. India said: cheap oil? We'll take all of it. Thanks, West.

...

[CHAPTER 4: BRICS RISING]
When the rest of the world starts its own group chat.

BRIC was formed in 2006. Named by a Goldman Sachs economist. Wall Street named the alliance that wants to destroy Wall Street. Ironic.

South Africa joined in 2010. BRICS now represents 40 percent of the world's population. The "global minority" is actually the majority.

They created their own World Bank. In Shanghai. Flexing. 50 billion dollars in capital. No structural adjustment required.

In 2023, six more nations were invited. Argentina said yes, then elected a libertarian who said no. Drama.

Saudi Arabia is hedging its bets. Still friends with the US. Also friends with China. Playing both sides like a pro.

Central banks are buying gold at record rates. Like doomsday preppers with PhDs.

...

[CHAPTER 5: MIDDLE EAST CHESS]
Where everyone's playing 4D chess and nobody's winning.

In April 2020, oil went negative. Minus 37 dollars and 63 cents per barrel. They literally paid you to take it.

By June 2022, oil surged to 120 dollars per barrel. OPEC popped champagne. Your gas bill tripled. Their yacht collection doubled.

OPEC Plus cut 2 million barrels per day. A middle finger to Biden. The US said please pump more. OPEC said: new phone, who dis?

OPEC Plus controls 40 percent of production and 80 percent of reserves. A cartel by any other name would smell as profitable.

In March 2023, China brokered a peace deal between Saudi Arabia and Iran. In Beijing. While America wasn't looking. Awkward.

...

[CHAPTER 6: THE WATCHERS]
Your phone knows more about you than your therapist.

Five Eyes was formed in 1946. Five countries pinky-swore to spy on everyone. Together. The OG group chat. Still active. Reading yours right now.

In 2013, Snowden told the world: the NSA reads all your stuff. PRISM gave direct access to Google, Facebook, Apple, and Microsoft servers.

XKeyscore: a search engine for spies. Search anyone's emails and browsing. No warrant needed.

Every single US domestic phone call. Metadata collected. They're not listening. They're just recording who, when, where, and how long.

Snowden fled to Russia and got citizenship. Fled a surveillance state. Moved to a surveillance state. Make it make sense.

China has 600 million surveillance cameras. One for every 2.4 citizens. 20 million flights blocked by social credit. Black Mirror was a documentary.

The product is you. You're not even getting a cut. Google processes 8.5 billion searches per day. Meta has 3 billion monthly users. The US data broker industry is worth over 200 billion dollars per year.

...

[CHAPTER 7: WAR MACHINE]
886 billion dollars per year. Somebody's making a killing. Literally.

The United States spends more on defense than the next 10 countries combined. For defense. Sure.

The F-35 program costs 1.7 trillion dollars over its lifetime. A plane that still has software bugs. Agile development, military edition.

750 military bases in over 80 countries. That's not defense. That's a franchise.

Afghanistan: 20 years, 2.3 trillion dollars. The Taliban waited it out with flip phones. They're back in charge.

Iraq: 2 trillion dollars searching for WMDs that never existed. Found lots of oil though.

Total cost of post-9/11 wars: over 8 trillion dollars. 900,000 dead. Brown University did the math. The Pentagon did not want them to.

1,700 senior Pentagon officials now work for arms companies. Approve the weapons. Retire. Sell the weapons. Nice gig if you can get it.

America is the world's number one arms dealer. 40 percent of global weapons sales. Top customer: Saudi Arabia. What they do with them? Don't ask.

...

[OUTRO]
Stay curious. Trust nobody.
Subscribe before they take this down.
All facts. All sourced. All uncomfortable.
Do your own research.
`;

process.stdout.write(narration.trim() + '\n');
