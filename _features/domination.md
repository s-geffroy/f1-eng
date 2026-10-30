---
title: "Dominance: when a team, a driver or an engine maker crushes the field, and what innovations change"
ordre: 6
resume: "Seventy-six seasons of official results to measure the dominance of teams, drivers and engine makers, from the single season to hegemony, then set it against innovations, engineers and regulations, without mistaking coincidence for cause."
description: "Seventy-six seasons of official results to measure the dominance of teams, drivers and engine makers, from the single season to hegemony, then set it against innovations, engineers and regulations, without mistaking coincidence for cause."
redirect_from: "/en/features/hegemonies/"
---
{%- assign H = site.data.domination -%}
{%- assign P = H.parametres -%}
{%- assign EF = H.effectifs -%}
{%- assign CP = site.data.compteur -%}
{%- assign CR = site.data.croisement -%}
{%- assign TJ = H.temoin_jalons -%}
{%- assign BI = H.bilan_ingenieurs -%}
{%- assign TR = H.temoin_reglement -%}
{%- assign EJ = H.etude_jalons -%}
{%- assign IA = H.ingenieurs_apparies -%}
{%- assign RB = H.rebat -%}
{%- assign AM = H.amont -%}
The [ranking]({{ site.baseurl }}/en/features/methode/) of engineers refuses to measure influence by results. This feature asks the opposite question: **do the innovations on the [timeline]({{ site.baseurl }}/en/timeline/) show up in the results?** To answer it, we first need to know when a team, a driver or an engine maker truly dominated, and to what degree: one season, a few seasons, or a whole era. These periods of dominance are then set against three things: technical milestones, engineers' arrivals and departures, and regulation changes.

The figures come from Formula 1's official results: the winner of each of the {{ P.gp }} championship Grands Prix held from 1950 to 2025, and the final drivers' and constructors' standings. A win shared between two drivers (France 1951, Argentina 1956, Britain 1957) counts as a single race, credited to both. The figures are computed by a program, not copied by hand. The champions derived from them match, season by season, those on the [team pages]({{ site.baseurl }}/en/teams/).

## The essentials

- **Dominating is common; lasting is rare.** Every season has its champions, but in seventy-six seasons hegemony is reached only {{ EF.ecurie.hegemonie }} times by a team, {{ EF.pilote.hegemonie }} times by a driver and {{ EF.motoriste.hegemonie }} times by an engine maker.
- **Winning is not crushing.** Red Bull, from 2021 to 2023, wins 74% of the Grands Prix but starts from pole only half the time; Mercedes, from 2014 to 2021, combines wins, poles and one-twos.
- **An innovation pays, but not for long.** The innovating team goes on average from {{ EJ.jalons[2] | times: 100 | round }}% to {{ EJ.jalons[4] | times: 100 | round }}% of wins. It returns to its starting level within four seasons.
- **The innovations that open a long dominance almost all respond to new regulations**: {{ AM.ouvrants_regle }} out of {{ AM.ouvrants }}.
- **Banning an innovation does not topple the dominant team.**
- **The arrival of a Tier A engineer precedes a rise {{ IA[1].hausse }} times out of {{ IA[1].n }}**, where a comparable team would see only {{ IA[1].hausse_attendue }}. A departure changes nothing.
- **New regulations seem to shake up the order**: in seasons when a regulation change applies, the team with the most wins changes {{ RB.avec.changements | times: 100.0 | divided_by: RB.avec.saisons | round }}% of the time, compared with {{ RB.sans.changements | times: 100.0 | divided_by: RB.sans.saisons | round }}% in other seasons. It is a clue, not proof. Yet such changes do not create a long dominance more often.

Contents
{:.sommaire-titre}

* TOC
{:toc}

## What we call dominance

A title is not enough: it can be won narrowly. The number of wins alone is not enough either: a team can win a lot without being champion. Two criteria are therefore used. A season is **dominant** for a team, driver or engine maker that wins the title, **or** that wins at least {{ P.seuil | times: 100 | round }}% of the Grands Prix.

Dominance is then measured by how long it lasts. The dominant seasons of the same competitor, separated by at most one lean season, form a period, which has one of three degrees:

1. **The dominant season**: a single season, with no follow-up. [Tyrrell]({{ site.baseurl }}/en/teams/tyrrell/) in 1971, [Brawn]({{ site.baseurl }}/en/teams/brawn/) in 2009.
2. **Dominance**: at least {{ P.duo }} dominant seasons. [McLaren]({{ site.baseurl }}/en/teams/mclaren/) in 1984 and 1985, for example.
3. **Hegemony**: at least {{ P.min }} dominant seasons, and a result that survives every variant of the threshold (see below). The Williams of the 1990s is an example: beaten in 1995, it remains dominant before and after that season.

Every season has a world champion, so every season is dominant for at least one driver, one team and one engine maker. The first degree is the most common. What is rare is lasting.

Three points to note:

- **Before 1958 there is no constructors' title.** The world champion's team stands in for it.
- **The thresholds are arbitrary**, as all thresholds are. The calculation is therefore repeated with two stricter variants: at least 50% of wins, then no lean season allowed. A period of at least {{ P.min }} dominant seasons found in both variants is called **robust**, even if its boundaries shift a little: this is what separates hegemony from other dominance. (A looser variant, such as "two seasons are enough", would always find everything again: it would put nothing to the test.)
- **The comparisons in the second part concern long dominance**: at least {{ P.min }} dominant seasons, robust or not. These are the hegemonies, plus a few fragile periods, such as Lotus's from 1968 to 1973.

Dominance is counted at four levels:

- the **team name**;
- the **lineage**, that is, the same factory under several names, such as [Brackley]({{ site.baseurl }}/en/teams/), from Tyrrell to Mercedes;
- the **driver**;
- the **engine maker**.

## Teams

{% include domination.html quoi="tableau" unite="ecurie" %}

In seventy-six seasons there are {{ EF.ecurie.hegemonie }} hegemonies and {{ EF.ecurie.domination }} other periods of dominance. Four features stand out.

- **The most crushing are the most recent.** [Mercedes]({{ site.baseurl }}/en/teams/mercedes/) wins 69% of the Grands Prix over eight seasons, from 2014 to 2021. [Red Bull]({{ site.baseurl }}/en/teams/red-bull/), from 2021 to 2023, wins 74% of them. The first hegemony, [Ferrari]({{ site.baseurl }}/en/teams/ferrari/)'s from 1975 to 1979, wins only about a third of them.
- **The longest is Ferrari's, from 1999 to 2008**: eight titles in ten seasons, with a single lean season, 2005.
- **Before 1975, no team reaches hegemony.** The 1950s and 1960s are played out in two-season dominance: Alfa Romeo, Ferrari, Mercedes-Benz, Cooper, Lotus, Brabham. The title changes hands too often for a team to settle in.
- **Two long periods of dominance are not hegemonies.** [Lotus]({{ site.baseurl }}/en/teams/team-lotus/), from 1968 to 1973, alternates titles and lean seasons, and never exceeds 47% of wins: it does not survive the variant with no lean season. McLaren, from 1998 to 2000, does not survive the 50% threshold: it wins only 44% of the Grands Prix in 1999 and 41% in 2000.

There are {{ EF.ecurie.saison }} dominant seasons with no follow-up: {% include domination.html quoi="saisons" unite="ecurie" %}. All are titles, sometimes won with few victories: McLaren in 1974 with 27% of the Grands Prix, Ferrari in 1964 with 30%.

At the level of **lineages**, the table is almost the same. Red Bull becomes Milton Keynes, Mercedes becomes Brackley, and Enstone has only two two-season periods of dominance, under the names Benetton (1994-1995) and Renault (2005-2006). No lineage reaches hegemony by adding up its successive names. Brackley, for example, wins with Brawn in 2009 and then with Mercedes from 2014, but the four seasons in between remain too lean.

{% include domination.html quoi="tableau" unite="lignee" %}

## Drivers

{% include domination.html quoi="tableau" unite="pilote" %}

Drivers' hegemonies follow their team's: Schumacher with Ferrari, Vettel and Verstappen with Red Bull, Hamilton with Mercedes. Only **Fangio**, from 1954 to 1957, reaches hegemony with three teams: Mercedes-Benz, Ferrari and Maserati.

Three long periods of driver dominance are not hegemonies:

- **Stewart**, from 1969 to 1973, dominates with Matra and then Tyrrell. His season with March, in 1970, is one of his lean seasons.
- **Prost** and **Senna** share the same McLaren: their periods of dominance overlap, and neither survives the threshold variants.

Drivers are where the isolated season is most frequent: {{ EF.pilote.saison }} cases, {% include domination.html quoi="saisons" unite="pilote" %}. A driver can be champion with few wins: Rosberg, in 1982, wins only one.

## Engine makers

{% include domination.html quoi="tableau" unite="motoriste" %}

This is the level of the longest dominance: that of the **Ford** engines, including the [Cosworth DFV]({{ site.baseurl }}/en/timeline/#j-dfv). They dominate every one of the fifteen seasons from 1968 to 1982 and win 70% of the Grands Prix, for Lotus, McLaren, Tyrrell and others.

The DFV is sold to everyone. There is therefore no matching team hegemony, but rather a succession of champion teams using the same engine. Climax before it, then Honda and Renault, dominate in the same way across several teams.

The Mercedes engine's dominance, from 2012 to 2021, begins before the Mercedes team's: it first wins with McLaren, then with Mercedes and Racing Point. Before that, the Mercedes engine had already had two long periods of dominance without reaching hegemony: from 1998 to 2000 with McLaren, then from 2005 to 2009 with McLaren and finally Brawn.

Red Bull's power unit from 2021 to 2023 is counted under the name **Honda**. The official results call it Honda in 2021, then RBPT and Honda RBPT, but Honda builds it throughout. This is a reading choice: with the three names kept apart, this hegemony disappears.

Isolated dominant seasons: {% include domination.html quoi="saisons" unite="motoriste" %}.

## Beyond wins: poles, podiums and one-twos

The degrees rest on titles and wins. Three other measures describe how a team dominates. They are recorded race by race from formula1.com:

- the **share of poles**: first place on the published starting grid, after any penalties;
- the **share of podium places**: out of the three places in each race;
- the **share of one-twos**: the first two places for the same team or engine maker. For a driver this measure makes no sense, so the tables give the share of podium places instead.

These measures describe dominance; they do not define it: a team does not change degree because of its poles. They appear in the tables above, together with the **composite index**: the simple average of the shares of wins, poles and podium places, out of 100. An index of 100 would mean winning everything, starting from pole at every race and filling the whole podium.

They add nuance to the record:

- **Mercedes, from 2014 to 2021, has it all**: 69% of wins, 74% of poles and a one-two in one race in three.
- **Red Bull, from 2021 to 2023, wins more (74%), but starts from pole less than half the time, and scores a one-two in only one race in six.** Its dominance rests mostly on one driver and on race pace.
- **McLaren, from 1988 to 1991, starts from pole 81% of the time**: the highest proportion among the hegemonies.
- **Ferrari, from 1975 to 1979, dominates with little**: 35% of wins, 24% of poles, 6% one-twos. It owes its hegemony to a run of titles more than to crushing the field.

### The most crushing seasons

The composite index also makes it possible to compare seasons with each other, regardless of degree.

{% include domination.html quoi="ecrasantes" unite="ecurie" %}

The 1950s rank high, but with few races: in 1952 Ferrari wins seven of the eight Grands Prix, the eighth being the Indianapolis 500, which it does not win. Since then, only McLaren in 1988 and Mercedes in 2014-2016 come close over a full season. Among drivers, no season reaches 60: a driver always shares the podium with a team-mate.

{% include domination.html quoi="ecrasantes" unite="pilote" %}

## The dominance gauge

Every [team page]({{ site.baseurl }}/en/teams/) carries a gauge. A dial gives the lineage's best season; below it, a curve follows the composite index season by season, for the factory under all its names. Titles, periods of dominance, timeline milestones and a threshold are marked on it.

The threshold is not chosen by hand. It is the index value that best separates dominant seasons (title or at least {{ P.seuil | times: 100 | round }}% of wins) from the others, in the sense of *Youden's index*, which adds the share of dominant seasons above the threshold to the share of other seasons below it. It is **{{ CP.seuil | times: 100 | round }}**. Of {{ CP.saisons }} measured lineage seasons, all {{ CP.dominantes }} dominant seasons exceed it ({{ CP.dominantes_au_dessus }}). {{ CP.au_dessus | minus: CP.dominantes_au_dessus }} others exceed it too: most often teams that finished second in the constructors' championship, beaten to the title.

## Innovations and results: four comparisons


Periods of dominance tell us who won. The question is what innovations change. Four questions are put to the data here:

1. What does an innovation bring to the team behind it, and for how long?
2. Do the chains of causes traced by the timeline, from regulations to innovation, lead to wins?
3. Does a team win more after an engineer arrives?
4. Does a regulation change reshuffle the pack?

The answers are summarised [at the top of the page](#the-essentials).

### Method

All the measures concern the team's **share of Grands Prix won**. A **long dominance** has at least {{ P.min }} dominant seasons, hegemony or not: for teams, these are the {{ EF.ecurie.hegemonie }} hegemonies, plus Lotus from 1968 to 1973 and McLaren from 1998 to 2000. Two windows are compared:

- **before**: the two seasons preceding the event;
- **after**: the three seasons starting with it.

Each difference is compared with a **control**. The control is the same calculation carried out for the same team in any other season, one in which nothing in particular happened.

For engineers, the control is **matched on the starting level**. A team that won nothing can only go up, and a team that won everything can only go down: this is *regression to the mean*. Without this precaution, that natural movement would be taken for the effect of an engineer.

When cases are few, we compute the **probability of a result at least as clear-cut by chance alone**. Below 5%, the difference is hard to put down to luck. Above it, it is a clue, not a demonstration.

Finally, the vocabulary is that of the [feature on causality]({{ site.baseurl }}/en/features/causalite/). A measured difference remains a **chronological** overlap. Only links the timeline already establishes with a source go further.

### 1. What an innovation brings, and for how long

We take the {{ EJ.n }} milestones attached to the team behind them. For each one, we follow the team's share of wins from three seasons before the milestone to five seasons after.

<figure class="figure">
{% include domination/etude-jalons-en.svg %}
<figcaption>Average share of Grands Prix won by the team, season by season around the milestone (solid line), and by the same team in any season (dashes). The values for each milestone are in the detailed table below.</figcaption>
</figure>

Three seasons before the milestone, nothing sets the team apart from its usual level.

- **In the milestone season, the team's share of wins jumps**, then peaks the following season.
- **The average difference between the two windows is +{{ EJ.gain | times: 100 | round }} points**, compared with {{ EJ.gain_temoin | times: 100 | round | replace: "-", "−" }} for the control.
- **The rise concerns about half the cases**: {{ EJ.hausses }} milestones out of {{ EJ.n }} are followed by a gain of more than 5 points. Two milestones of the same team in the same year (Benetton in 1993, McLaren in 2009) count only once.
- **The lead then fades**: four seasons after the milestone, the team is back to its previous level. An innovation gives a lead of two to three seasons. The data do not say why it fades: copying by rivals, a ban under the regulations (part 2), or simply the passage of time.

**Not all technical tracks of the timeline pay off equally.** **Architecture** milestones (the Coopers' rear engine, the Lotus 25 monocoque, the MP4/1's carbon, the MP4/4) pay off best: five out of six are followed by a rise. **Aerodynamics** provides the most milestones, but each one pays off less, perhaps because its ideas are copied faster. The numbers are too small to go further.

{% include domination.html quoi="voies" %}

**An innovation rarely founds a long dominance on its own.** Of {{ TJ.n }} milestones introduced by a team that was not yet dominating, **{{ TJ.ouvre }} shortly precede a long dominance**:

- the [DFV]({{ site.baseurl }}/en/timeline/#j-dfv) at Lotus in 1967;
- the [312T]({{ site.baseurl }}/en/timeline/#j-ferrari-312t) at Ferrari in 1975;
- the [MP4/4]({{ site.baseurl }}/en/timeline/#j-mp4-4) at McLaren in 1988;
- the [RB6]({{ site.baseurl }}/en/timeline/#j-rb6) at Red Bull in 2010;
- the [hybrid power unit]({{ site.baseurl }}/en/timeline/#j-hybride) at Mercedes in 2014.

The control expects {{ TJ.attendu }}. Chance alone would produce at least as many with a probability of {{ H.p_hasard | times: 100 | round }}%. It is a clue, not proof.

The counter-examples are instructive:

- **Innovation with no sequel.** The [Lotus 78]({{ site.baseurl }}/en/timeline/#j-lotus-78) takes Lotus from 3% to 27% of wins, with no long dominance following. The [1993 Benetton]({{ site.baseurl }}/en/timeline/#j-cfd-benetton) takes its team from 6% to 40%, but for only two seasons of domination. The [double diffuser]({{ site.baseurl }}/en/timeline/#j-double-diffuseur) brings Brawn a title, then the team changes name. The carbon [MP4/1]({{ site.baseurl }}/en/timeline/#j-mp4-1) brings McLaren only 13% of wins from 1981 to 1983: the 1984 and 1985 titles come with the [MP4/2]({{ site.baseurl }}/en/timeline/#j-mp4-2) and its TAG-Porsche engine.
- **Innovation that extends a dominance.** The [Lotus 72]({{ site.baseurl }}/en/timeline/#j-lotus-72), the [FW14B]({{ site.baseurl }}/en/timeline/#j-fw14b) and the [RB18]({{ site.baseurl }}/en/timeline/#j-rb18) arrive when their team is already dominating.
- **Dominance without a milestone.** No milestone accompanies Ferrari in 1999-2008, nor McLaren in 1998-2000. The milestones on the timeline do not explain them.

<details>
<summary>The {{ EJ.n }} milestones one by one</summary>
{% include domination.html quoi="jalons" %}
</details>

### 2. From regulations to wins: the sourced chains

The timeline links context events (regulations, economics, techniques from elsewhere) to the milestones they made possible or ended. Each link carries its mechanism and its level of evidence. A complete chain can therefore be followed: a regulation, the innovation it prompts, then the wins that follow.

**The innovations that found a long dominance almost all respond to new regulations.** Of the {{ AM.ouvrants }} milestones that precede a long dominance, {{ AM.ouvrants_regle }} are linked by the timeline to a regulation change:

- the DFV to the [3-litre formula]({{ site.baseurl }}/en/timeline/#c-formule-3-litres) (established link);
- the MP4/4 to the [restricted turbos and the 150-litre fuel allowance]({{ site.baseurl }}/en/timeline/#c-turbo-bride) (attested);
- the RB6 to the [2009 aerodynamic overhaul]({{ site.baseurl }}/en/timeline/#c-refonte-aero-2009) (disputed);
- the hybrid engine to the [mandatory power unit]({{ site.baseurl }}/en/timeline/#c-groupe-propulseur-2014) of 2014 (established).

Across all milestones, the proportion is only {{ AM.avec_regle }} out of {{ AM.jalons }}.

New regulations reset everyone to zero. Whoever answers them best starts with a lead the others can only close over several seasons. But with only {{ AM.ouvrants }} cases, chance would produce such a gap with a probability of {{ AM.p | times: 100 | round }}%: it is a tendency, not a law.

<details>
<summary>The chains that open or transfer an innovation</summary>
{% include domination.html quoi="chaines" ferme="non" %}
</details>

**Banning an innovation does not topple the dominant team.** When the regulations close the door on an innovation, the effect on the team that had it varies: the team sometimes falls back, but rises just as often. Twice, the ban hits a team at the top, and the team stays there:

- **Williams in 1994**, with the [ban on electronic aids]({{ site.baseurl }}/en/timeline/#c-fin-aides-electroniques): it goes from 62% to 49% of wins, but its hegemony lasts until 1997.
- **Red Bull in 2012**, with the [restrictions on exhausts]({{ site.baseurl }}/en/timeline/#c-echappements-2012): it goes from 55% to 40%, but still dominates until 2013.

What makes a domination last does not, then, come down to a single part of the car.

{% include domination.html quoi="chaines" ferme="oui" %}

### 3. Engineers

For each arrival, the team's share of wins is compared over the two seasons before and the three starting with the engineer. For each departure, the last two seasons with him are compared with the next three. A rise or fall of more than 5 points is counted as such. Arrivals too recent to have three seasons of hindsight are left out.

<figure class="figure">
{% include domination/ingenieurs-en.svg %}
<figcaption>Share of cases followed by a rise of more than 5 points (solid dot), and the share expected from the control matched on the starting level (circle). In brackets, the number of cases.</figcaption>
</figure>

**After an arrival, the team improves markedly more often than expected**: {{ IA[0].hausse }} cases out of {{ IA[0].n }}, where the matched control expects {{ IA[0].hausse_attendue }}. Chance alone would produce such a gap with a probability below 0.1%.

**The gap is largest for Tier A**: {{ IA[1].hausse }} rises out of {{ IA[1].n }} arrivals, for {{ IA[1].hausse_attendue }} expected, and an average gain of +{{ IA[1].gain | times: 100 | round }} points; chance alone would produce such a gap with a probability of {{ IA[1].p | times: 100 | round }}%. These are the arrivals of [Adrian Newey]({{ site.baseurl }}/en/engineers/adrian-newey/) and [John Barnard]({{ site.baseurl }}/en/engineers/john-barnard/). Rises follow Newey at Williams (1990) and McLaren (1997), and Barnard at McLaren (1972 and 1980) and Ferrari (1987). The others are not followed by one: Newey at Fittipaldi (1980), March (1988) and Red Bull (2006), where the first win waits until 2009, and Barnard on his return to Ferrari (1992). Nine cases is few: the gap is clear, but it rests on two men.

For Tiers B to D the gap is smaller: chance alone would produce it with a probability of {{ IA[2].p | times: 100 | round }}%. For unranked engineers the gap is smaller still, but it remains clear over {{ IA[3].n }} cases.

**A departure changes nothing**: {{ IA[4].hausse }} rises for {{ IA[4].hausse_attendue }} expected. A team keeps its momentum for a few seasons after an engineer leaves.

This does not prove that the engineer makes the team win. The control neutralises the starting level, not the trajectory or the budget. A great engineer also chooses a rising team, and a rising team has the means to hire him. But the ranking was not drawn up from results, and yet it is the Tier A engineers whose arrival most clearly precedes a rise. The two measures, one technical and one sporting, point the same way.

**Who was there when each long dominance began?** An engineer is counted if he arrived before the dominance began and did not leave more than three seasons before it began. When his departure date is not known and he arrived more than three seasons earlier, his presence is marked as uncertain.

{% include domination.html quoi="racines" %}

[Adrian Newey]({{ site.baseurl }}/en/engineers/adrian-newey/) is present at the start of four of the {{ EF.ecurie.longue }} long periods of team dominance: Williams 1991, McLaren 1998, Red Bull 2010 and Red Bull 2021. Two engineers are present at the start of three:

- [Paddy Lowe]({{ site.baseurl }}/en/engineers/paddy-lowe/): Williams 1991, McLaren 1998 and Mercedes 2014;
- [Geoff Willis]({{ site.baseurl }}/en/engineers/geoff-willis/): Williams 1991, Red Bull 2010 and Mercedes 2014. For Red Bull, the three-season rule counts him, but he left the team in 2009, before the 2010 season.

[Ross Brawn]({{ site.baseurl }}/en/engineers/ross-brawn/) and [John Barnard]({{ site.baseurl }}/en/engineers/john-barnard/) are present at the start of two: Ferrari 1999 and Mercedes 2014 for Brawn, McLaren 1988 and Ferrari 1999 for Barnard, each having left shortly before.

<details>
<summary>The summary and the moves one by one</summary>
{% include domination.html quoi="ingenieurs" %}
</details>

### 4. Regulations: reshuffling the pack without creating a dynasty

From one season to the next, the team winning the most Grands Prix often changes. It changes **{{ RB.avec.changements }} times out of {{ RB.avec.saisons }}** in seasons when a regulation change on the timeline comes into force, against **{{ RB.sans.changements }} times out of {{ RB.sans.saisons }}** in other seasons. Chance alone would produce such a gap with a probability of {{ RB.p | times: 100 | round }}%, above the usual 5% threshold. **New regulations therefore seem to shake up the order, though the data are not enough to prove it.**

Yet they do not create dynasties more often. {{ TR.debuts_regle }} starts of long dominance out of {{ TR.debuts }}, and {{ TR.fins_regle }} ends out of {{ TR.fins }}, coincide with a regulation change. Here, "coincide" means that the regulation applies in the same season or the one before; with that window, {{ TR.avec_regle }} seasons out of {{ TR.annees }} are in that situation: the proportion is roughly the same.

The regulations redeal the cards. Someone still has to know how to play the new hand, and this is where parts 1 to 3 meet. The clearest coincidences:

- the [mandatory hybrid power unit]({{ site.baseurl }}/en/timeline/#c-groupe-propulseur-2014) of 2014 shortly precedes the hegemonies of Mercedes and of Hamilton;
- the [2009 aerodynamic overhaul]({{ site.baseurl }}/en/timeline/#c-refonte-aero-2009) precedes Red Bull's;
- the [return of ground effect]({{ site.baseurl }}/en/timeline/#c-retour-effet-de-sol), in 2022, shortly follows the end of Mercedes';
- the [3-litre formula]({{ site.baseurl }}/en/timeline/#c-formule-3-litres), in 1966, shortly follows the end of Climax's;
- the [flat bottom]({{ site.baseurl }}/en/timeline/#c-fond-plat), in 1983, shortly follows the end of Ford's.

### What to take away

Lasting dominance is rarely built on a single idea. The data rather suggest a sequence:

1. **new regulations** reset the order to zero;
2. a team answers them with an **innovation** that gives it two to three seasons' lead;
3. it keeps that lead if it has managed to attract, or keep, the **engineers** able to renew the idea before it is copied;
4. a **ban** on the innovation is not enough to end its domination: that takes the next set of regulations.

Mercedes in 2014 and Red Bull in 2010 follow this pattern almost step by step. Ferrari in 1999-2008 does not fit it, for lack of a milestone on the timeline.

## Limits

- **Wins are not the only measure.** They ignore teams that improve without winning, and they also reflect the driver's talent, reliability and budgets.
- **The milestones are a selection.** The timeline keeps the innovations that changed how cars are designed, not those that won races. A dominance without a milestone may hide an innovation the timeline does not include.
- **Milestones are attached to teams according to the team pages.** Four milestones are attached to no team, and are therefore not counted: the [Cooper 500 prototype]({{ site.baseurl }}/en/timeline/#j-cooper-500), the [FVA]({{ site.baseurl }}/en/timeline/#j-dfv-fva), [pneumatic valve springs]({{ site.baseurl }}/en/timeline/#j-rappel-pneumatique) and the [Renault V10]({{ site.baseurl }}/en/timeline/#j-v10-renault).
- **Engineers' dates are sometimes incomplete.** Those of the engineers named in this feature have been checked against their pages; others remain approximate. A missing departure date makes a presence uncertain, and the table says so.
- **The Indianapolis 500 (1950-1960) counted for the championship.** It is therefore included here, won by American constructors: [Kurtis Kraft]({{ site.baseurl }}/en/teams/kurtis-kraft/) has a page, Kuzma, Watson and Epperly do not.
- **The thresholds remain choices.** The "Degree" column shows which long periods of dominance withstand them: these are the hegemonies.

## Sources

Results consulted on 29 October 2026 on formula1.com, for each season from 1950 to 2025:

- Grand Prix winners: `https://www.formula1.com/en/results/<year>/races`;
- constructors' standings, since 1958: `…/<year>/team`;
- drivers' standings: `…/<year>/drivers`;
- for each race, the podium and the starting grid: `…/<year>/races/<race>/race-result` and `…/starting-grid`.

The link to each race is kept in the site's data.

These results were compared race by race with a second source, the open [Jolpica]({{ CR.source }}) database (successor to Ergast). Winners agree for {{ CR.bilan.vainqueur.concordants }} races out of {{ P.gp }}, poles for {{ CR.bilan.pole.concordants }}, second places for {{ CR.bilan.deuxieme.concordants }} and third places for {{ CR.bilan.troisieme.concordants }}. The only disagreement concerns the 1983 Brazilian Grand Prix: formula1.com leaves vacant the second place of the disqualified Keke Rosberg and ranks Niki Lauda third; Jolpica moves everyone up one place and ranks Jacques Laffite third. This feature follows formula1.com. Engineers, milestones and regulations come from the [team pages]({{ site.baseurl }}/en/teams/) and the [timeline]({{ site.baseurl }}/en/timeline/), where each has its own sources.
