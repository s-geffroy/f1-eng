---
title: "Hegemonies: when a team dominates, and what innovations change"
ordre: 6
resume: "Seventy-six seasons of official results to identify the periods of domination by teams, drivers and engine makers, then set them against innovations, engineers and regulations, without mistaking coincidence for cause."
description: "Seventy-six seasons of official results to identify the periods of domination by teams, drivers and engine makers, then set them against innovations, engineers and regulations, without mistaking coincidence for cause."
---
{%- assign H = site.data.hegemonies -%}
{%- assign P = H.parametres -%}
{%- assign TJ = H.temoin_jalons -%}
{%- assign BI = H.bilan_ingenieurs -%}
{%- assign TR = H.temoin_reglement -%}
{%- assign EJ = H.etude_jalons -%}
{%- assign IA = H.ingenieurs_apparies -%}
{%- assign RB = H.rebat -%}
{%- assign AM = H.amont -%}
The [ranking]({{ site.baseurl }}/en/features/methode/) of engineers refuses to measure influence by results. This feature asks the opposite question: **do the innovations on the [timeline]({{ site.baseurl }}/en/timeline/) show up in the results?** To answer it, we first need to know when a team, a driver or an engine maker truly dominated. These periods are then set against three things: technical milestones, engineers' arrivals and departures, and regulation changes.

The figures come from Formula 1's official results: the winner of each of the {{ P.gp }} championship Grands Prix held from 1950 to 2025, and the final drivers' and constructors' standings. A win shared between two drivers (France 1951, Argentina 1956, Britain 1957) counts as a single race, credited to both. The figures are computed by a program, not copied by hand. The champions derived from them match, season by season, those on the [team pages]({{ site.baseurl }}/en/teams/).

## The essentials

- **An innovation pays, but not for long.** The innovating team goes on average from {{ EJ.jalons[2] | times: 100 | round }}% to {{ EJ.jalons[4] | times: 100 | round }}% of wins. It returns to its starting level within four seasons.
- **The innovations that open a hegemony almost all respond to new regulations**: {{ AM.ouvrants_regle }} out of {{ AM.ouvrants }}.
- **Banning an innovation does not topple the dominant team.**
- **The arrival of a Tier A engineer precedes a rise {{ IA[1].hausse }} times out of {{ IA[1].n }}**, where a comparable team would see only {{ IA[1].hausse_attendue }}. A departure changes nothing.
- **New regulations seem to shake up the order**: in seasons when a regulation change applies, the team with the most wins changes {{ RB.avec.changements | times: 100.0 | divided_by: RB.avec.saisons | round }}% of the time, compared with {{ RB.sans.changements | times: 100.0 | divided_by: RB.sans.saisons | round }}% in other seasons. It is a clue, not proof. Yet such changes do not create a hegemony more often.

Contents
{:.sommaire-titre}

* TOC
{:toc}

## What we call a hegemony

A title is not enough: it can be won narrowly. The number of wins alone is not enough either: a team can win a lot without being champion. Two criteria are therefore used. A season is **dominant** for a team, driver or engine maker that wins the title, **or** that wins at least {{ P.seuil | times: 100 | round }}% of the Grands Prix.

A **hegemony** comprises at least three dominant seasons, separated by at most one lean season. The Williams of the 1990s is an example: beaten in 1995, it remains dominant before and after that season.

Two points to note:

- **Before 1958 there is no constructors' title.** The world champion's team stands in for it.
- **The thresholds are arbitrary**, as all thresholds are. The calculation is therefore repeated with two stricter variants: at least 50% of wins, then no lean season allowed. A hegemony found in both variants is called **robust**, even if its boundaries shift a little. (A looser variant, such as "two seasons are enough", would always find everything again: it would put nothing to the test.)

Hegemonies are counted at four levels:

- the **team name**;
- the **lineage**, that is, the same factory under several names, such as [Brackley]({{ site.baseurl }}/en/teams/), from Tyrrell to Mercedes;
- the **driver**;
- the **engine maker**.

## Teams

{% include hegemonies.html quoi="tableau" unite="ecurie" %}

Nine hegemonies in seventy-six seasons. Three features stand out.

- **The most crushing are the most recent.** [Mercedes]({{ site.baseurl }}/en/teams/mercedes/) wins 69% of the Grands Prix over eight seasons, from 2014 to 2021. [Red Bull]({{ site.baseurl }}/en/teams/red-bull/), from 2021 to 2023, wins 74% of them. The two hegemonies of the 1960s and 1970s, those of Lotus and Ferrari, win only about a third of them.
- **The longest is [Ferrari]({{ site.baseurl }}/en/teams/ferrari/)'s, from 1999 to 2008**: eight titles in ten seasons, with a single lean season, 2005.
- **[Lotus]({{ site.baseurl }}/en/teams/team-lotus/), from 1968 to 1973, is not robust.** It alternates titles and lean seasons, and never exceeds 47% of wins.

Dominations of only two seasons are not counted as hegemonies: {% include hegemonies.html quoi="courtes" unite="ecurie" %}. They would become hegemonies if two seasons were enough. The two fragile hegemonies are fragile for other reasons: Lotus's does not survive without a lean season, since it alternates titles and thin seasons; McLaren's, from 1998 to 2000, does not survive the 50% threshold, McLaren winning only 44% of the Grands Prix in 1999 and 41% in 2000.

At the level of **lineages**, the table is almost the same. Red Bull becomes Milton Keynes, Mercedes becomes Brackley, and Enstone has only two two-season dominations, under the names Benetton (1994-1995) and Renault (2005-2006). No lineage forms a hegemony by adding up its successive names. Brackley, for example, wins with Brawn in 2009 and then with Mercedes from 2014, but the four seasons in between remain too lean.

{% include hegemonies.html quoi="tableau" unite="lignee" %}

## Drivers

{% include hegemonies.html quoi="tableau" unite="pilote" %}

Drivers' hegemonies almost always follow their team's: Schumacher with Ferrari, Vettel and Verstappen with Red Bull, Hamilton with Mercedes. There are two exceptions:

- **Fangio**, from 1954 to 1957, dominates with Mercedes-Benz, Ferrari and Maserati.
- **Stewart**, from 1969 to 1973, dominates with Matra and then Tyrrell. His season with March, in 1970, is the lean season of his hegemony.

Their hegemonies span several teams: each driver changes car and keeps winning. Prost and Senna, for their part, share the same McLaren: their hegemonies overlap, and neither is robust.

Two-season dominations: {% include hegemonies.html quoi="courtes" unite="pilote" %}.

## Engine makers

{% include hegemonies.html quoi="tableau" unite="motoriste" %}

This is the level of the longest domination: that of the **Ford** engines, including the [Cosworth DFV]({{ site.baseurl }}/en/timeline/#j-dfv). They dominate every one of the fifteen seasons from 1968 to 1982 and win 70% of the Grands Prix, for Lotus, McLaren, Tyrrell and others.

The DFV is sold to everyone. There is therefore no matching team hegemony, but rather a succession of champion teams using the same engine. Climax before it, then Honda and Renault, dominate in the same way across several teams.

The Mercedes engine's domination, from 2012 to 2021, begins before the Mercedes team's: it first wins with McLaren, then with Mercedes and Racing Point.

Red Bull's power unit from 2021 to 2023 is counted under the name **Honda**. The official results call it Honda in 2021, then RBPT and Honda RBPT, but Honda builds it throughout. This is a reading choice: with the three names kept apart, this hegemony disappears.

## Innovations and results: four comparisons


Hegemonies tell us who won. The question is what innovations change. Four questions are put to the data here:

1. What does an innovation bring to the team behind it, and for how long?
2. Do the chains of causes traced by the timeline, from regulations to innovation, lead to wins?
3. Does a team win more after an engineer arrives?
4. Does a regulation change reshuffle the pack?

The answers are summarised [at the top of the page](#the-essentials).

### Method

All the measures concern the team's **share of Grands Prix won**. Two windows are compared:

- **before**: the two seasons preceding the event;
- **after**: the three seasons starting with it.

Each difference is compared with a **control**. The control is the same calculation carried out for the same team in any other season, one in which nothing in particular happened.

For engineers, the control is **matched on the starting level**. A team that won nothing can only go up, and a team that won everything can only go down: this is *regression to the mean*. Without this precaution, that natural movement would be taken for the effect of an engineer.

When cases are few, we compute the **probability of a result at least as clear-cut by chance alone**. Below 5%, the difference is hard to put down to luck. Above it, it is a clue, not a demonstration.

Finally, the vocabulary is that of the [feature on causality]({{ site.baseurl }}/en/features/causalite/). A measured difference remains a **chronological** overlap. Only links the timeline already establishes with a source go further.

### 1. What an innovation brings, and for how long

We take the {{ EJ.n }} milestones attached to the team behind them. For each one, we follow the team's share of wins from three seasons before the milestone to five seasons after.

<figure class="figure">
{% include hegemonies/etude-jalons-en.svg %}
<figcaption>Average share of Grands Prix won by the team, season by season around the milestone (solid line), and by the same team in any season (dashes). The values for each milestone are in the detailed table below.</figcaption>
</figure>

Three seasons before the milestone, nothing sets the team apart from its usual level.

- **In the milestone season, the team's share of wins jumps**, then peaks the following season.
- **The average difference between the two windows is +{{ EJ.gain | times: 100 | round }} points**, compared with {{ EJ.gain_temoin | times: 100 | round | replace: "-", "−" }} for the control.
- **The rise concerns about half the cases**: {{ EJ.hausses }} milestones out of {{ EJ.n }} are followed by a gain of more than 5 points. Two milestones of the same team in the same year (Benetton in 1993, McLaren in 2009) count only once.
- **The lead then fades**: four seasons after the milestone, the team is back to its previous level. An innovation gives a lead of two to three seasons. The data do not say why it fades: copying by rivals, a ban under the regulations (part 2), or simply the passage of time.

**Not all technical tracks of the timeline pay off equally.** **Architecture** milestones (the Coopers' rear engine, the Lotus 25 monocoque, the MP4/1's carbon, the MP4/4) pay off best: five out of six are followed by a rise. **Aerodynamics** provides the most milestones, but each one pays off less, perhaps because its ideas are copied faster. The numbers are too small to go further.

{% include hegemonies.html quoi="voies" %}

**An innovation rarely founds a hegemony on its own.** Of {{ TJ.n }} milestones introduced by a team that was not yet dominating, **{{ TJ.ouvre }} shortly precede a hegemony**:

- the [DFV]({{ site.baseurl }}/en/timeline/#j-dfv) at Lotus in 1967;
- the [312T]({{ site.baseurl }}/en/timeline/#j-ferrari-312t) at Ferrari in 1975;
- the [MP4/4]({{ site.baseurl }}/en/timeline/#j-mp4-4) at McLaren in 1988;
- the [RB6]({{ site.baseurl }}/en/timeline/#j-rb6) at Red Bull in 2010;
- the [hybrid power unit]({{ site.baseurl }}/en/timeline/#j-hybride) at Mercedes in 2014.

The control expects {{ TJ.attendu }}. Chance alone would produce at least as many with a probability of {{ H.p_hasard | times: 100 | round }}%. It is a clue, not proof.

The counter-examples are instructive:

- **Innovation with no sequel.** The [Lotus 78]({{ site.baseurl }}/en/timeline/#j-lotus-78) takes Lotus from 3% to 27% of wins, with no hegemony following. The [1993 Benetton]({{ site.baseurl }}/en/timeline/#j-cfd-benetton) takes its team from 6% to 40%, but for only two seasons of domination. The [double diffuser]({{ site.baseurl }}/en/timeline/#j-double-diffuseur) brings Brawn a title, then the team changes name. The carbon [MP4/1]({{ site.baseurl }}/en/timeline/#j-mp4-1) brings McLaren only 13% of wins from 1981 to 1983: the 1984 and 1985 titles come with the [MP4/2]({{ site.baseurl }}/en/timeline/#j-mp4-2) and its TAG-Porsche engine.
- **Innovation that extends a hegemony.** The [Lotus 72]({{ site.baseurl }}/en/timeline/#j-lotus-72), the [FW14B]({{ site.baseurl }}/en/timeline/#j-fw14b) and the [RB18]({{ site.baseurl }}/en/timeline/#j-rb18) arrive when their team is already dominating.
- **Hegemony without a milestone.** No milestone accompanies Ferrari in 1999-2008, nor McLaren in 1998-2000. The milestones on the timeline do not explain them.

<details>
<summary>The {{ EJ.n }} milestones one by one</summary>
{% include hegemonies.html quoi="jalons" %}
</details>

### 2. From regulations to wins: the sourced chains

The timeline links context events (regulations, economics, techniques from elsewhere) to the milestones they made possible or ended. Each link carries its mechanism and its level of evidence. A complete chain can therefore be followed: a regulation, the innovation it prompts, then the wins that follow.

**The innovations that found a hegemony almost all respond to new regulations.** Of the {{ AM.ouvrants }} milestones that precede a hegemony, {{ AM.ouvrants_regle }} are linked by the timeline to a regulation change:

- the DFV to the [3-litre formula]({{ site.baseurl }}/en/timeline/#c-formule-3-litres) (established link);
- the MP4/4 to the [restricted turbos and the 150-litre fuel allowance]({{ site.baseurl }}/en/timeline/#c-turbo-bride) (attested);
- the RB6 to the [2009 aerodynamic overhaul]({{ site.baseurl }}/en/timeline/#c-refonte-aero-2009) (disputed);
- the hybrid engine to the [mandatory power unit]({{ site.baseurl }}/en/timeline/#c-groupe-propulseur-2014) of 2014 (established).

Across all milestones, the proportion is only {{ AM.avec_regle }} out of {{ AM.jalons }}.

New regulations reset everyone to zero. Whoever answers them best starts with a lead the others can only close over several seasons. But with only {{ AM.ouvrants }} cases, chance would produce such a gap with a probability of {{ AM.p | times: 100 | round }}%: it is a tendency, not a law.

<details>
<summary>The chains that open or transfer an innovation</summary>
{% include hegemonies.html quoi="chaines" ferme="non" %}
</details>

**Banning an innovation does not topple the dominant team.** When the regulations close the door on an innovation, the effect on the team that had it varies: the team sometimes falls back, but rises just as often. Twice, the ban hits a team at the top, and the team stays there:

- **Williams in 1994**, with the [ban on electronic aids]({{ site.baseurl }}/en/timeline/#c-fin-aides-electroniques): it goes from 62% to 49% of wins, but its hegemony lasts until 1997.
- **Red Bull in 2012**, with the [restrictions on exhausts]({{ site.baseurl }}/en/timeline/#c-echappements-2012): it goes from 55% to 40%, but still dominates until 2013.

What makes a domination last does not, then, come down to a single part of the car.

{% include hegemonies.html quoi="chaines" ferme="oui" %}

### 3. Engineers

For each arrival, the team's share of wins is compared over the two seasons before and the three starting with the engineer. For each departure, the last two seasons with him are compared with the next three. A rise or fall of more than 5 points is counted as such. Arrivals too recent to have three seasons of hindsight are left out.

<figure class="figure">
{% include hegemonies/ingenieurs-en.svg %}
<figcaption>Share of cases followed by a rise of more than 5 points (solid dot), and the share expected from the control matched on the starting level (circle). In brackets, the number of cases.</figcaption>
</figure>

**After an arrival, the team improves markedly more often than expected**: {{ IA[0].hausse }} cases out of {{ IA[0].n }}, where the matched control expects {{ IA[0].hausse_attendue }}. Chance alone would produce such a gap with a probability below 0.1%.

**The gap is largest for Tier A**: {{ IA[1].hausse }} rises out of {{ IA[1].n }} arrivals, for {{ IA[1].hausse_attendue }} expected, and an average gain of +{{ IA[1].gain | times: 100 | round }} points; chance alone would produce such a gap with a probability of {{ IA[1].p | times: 100 | round }}%. These are the arrivals of [Adrian Newey]({{ site.baseurl }}/en/engineers/adrian-newey/) and [John Barnard]({{ site.baseurl }}/en/engineers/john-barnard/). Rises follow Newey at Williams (1990) and McLaren (1997), and Barnard at McLaren (1972 and 1980) and Ferrari (1987). The others are not followed by one: Newey at Fittipaldi (1980), March (1988) and Red Bull (2006), where the first win waits until 2009, and Barnard on his return to Ferrari (1992). Nine cases is few: the gap is clear, but it rests on two men.

For Tiers B to D the gap is smaller: chance alone would produce it with a probability of {{ IA[2].p | times: 100 | round }}%. For unranked engineers the gap is smaller still, but it remains clear over {{ IA[3].n }} cases.

**A departure changes nothing**: {{ IA[4].hausse }} rises for {{ IA[4].hausse_attendue }} expected. A team keeps its momentum for a few seasons after an engineer leaves.

This does not prove that the engineer makes the team win. The control neutralises the starting level, not the trajectory or the budget. A great engineer also chooses a rising team, and a rising team has the means to hire him. But the ranking was not drawn up from results, and yet it is the Tier A engineers whose arrival most clearly precedes a rise. The two measures, one technical and one sporting, point the same way.

**Who was there when each hegemony began?** An engineer is counted if he arrived before the hegemony began and did not leave more than three seasons before it began. When his departure date is not known and he arrived more than three seasons earlier, his presence is marked as uncertain.

{% include hegemonies.html quoi="racines" %}

[Adrian Newey]({{ site.baseurl }}/en/engineers/adrian-newey/) is present at the start of four of the nine team hegemonies: Williams 1991, McLaren 1998, Red Bull 2010 and Red Bull 2021. Two engineers are present at the start of three:

- [Paddy Lowe]({{ site.baseurl }}/en/engineers/paddy-lowe/): Williams 1991, McLaren 1998 and Mercedes 2014;
- [Geoff Willis]({{ site.baseurl }}/en/engineers/geoff-willis/): Williams 1991, Red Bull 2010 and Mercedes 2014. For Red Bull, the three-season rule counts him, but he left the team in 2009, before the 2010 season.

[Ross Brawn]({{ site.baseurl }}/en/engineers/ross-brawn/) and [John Barnard]({{ site.baseurl }}/en/engineers/john-barnard/) are present at the start of two: Ferrari 1999 and Mercedes 2014 for Brawn, McLaren 1988 and Ferrari 1999 for Barnard, each having left shortly before.

<details>
<summary>The summary and the moves one by one</summary>
{% include hegemonies.html quoi="ingenieurs" %}
</details>

### 4. Regulations: reshuffling the pack without creating a dynasty

From one season to the next, the team winning the most Grands Prix often changes. It changes **{{ RB.avec.changements }} times out of {{ RB.avec.saisons }}** in seasons when a regulation change on the timeline comes into force, against **{{ RB.sans.changements }} times out of {{ RB.sans.saisons }}** in other seasons. Chance alone would produce such a gap with a probability of {{ RB.p | times: 100 | round }}%, above the usual 5% threshold. **New regulations therefore seem to shake up the order, though the data are not enough to prove it.**

Yet they do not create dynasties more often. {{ TR.debuts_regle }} hegemony starts out of {{ TR.debuts }}, and {{ TR.fins_regle }} ends out of {{ TR.fins }}, coincide with a regulation change. Here, "coincide" means that the regulation applies in the same season or the one before; with that window, {{ TR.avec_regle }} seasons out of {{ TR.annees }} are in that situation: the proportion is roughly the same.

The regulations redeal the cards. Someone still has to know how to play the new hand, and this is where parts 1 to 3 meet. The clearest coincidences:

- the [mandatory hybrid power unit]({{ site.baseurl }}/en/timeline/#c-groupe-propulseur-2014) of 2014 shortly precedes the hegemonies of Mercedes and of Hamilton;
- the [2009 aerodynamic overhaul]({{ site.baseurl }}/en/timeline/#c-refonte-aero-2009) precedes Red Bull's;
- the [return of ground effect]({{ site.baseurl }}/en/timeline/#c-retour-effet-de-sol), in 2022, shortly follows the end of Mercedes';
- the [3-litre formula]({{ site.baseurl }}/en/timeline/#c-formule-3-litres), in 1966, shortly follows the end of Climax's;
- the [flat bottom]({{ site.baseurl }}/en/timeline/#c-fond-plat), in 1983, shortly follows the end of Ford's.

### What to take away

A hegemony is rarely built on a single idea. The data rather suggest a sequence:

1. **new regulations** reset the order to zero;
2. a team answers them with an **innovation** that gives it two to three seasons' lead;
3. it keeps that lead if it has managed to attract, or keep, the **engineers** able to renew the idea before it is copied;
4. a **ban** on the innovation is not enough to end its domination: that takes the next set of regulations.

Mercedes in 2014 and Red Bull in 2010 follow this pattern almost step by step. Ferrari in 1999-2008 does not fit it, for lack of a milestone on the timeline.

## Limits

- **Wins are not the only measure.** They ignore teams that improve without winning, and they also reflect the driver's talent, reliability and budgets.
- **The milestones are a selection.** The timeline keeps the innovations that changed how cars are designed, not those that won races. A hegemony without a milestone may hide an innovation the timeline does not include.
- **Milestones are attached to teams according to the team pages.** Four milestones are attached to no team, and are therefore not counted: the [Cooper 500 prototype]({{ site.baseurl }}/en/timeline/#j-cooper-500), the [FVA]({{ site.baseurl }}/en/timeline/#j-dfv-fva), [pneumatic valve springs]({{ site.baseurl }}/en/timeline/#j-rappel-pneumatique) and the [Renault V10]({{ site.baseurl }}/en/timeline/#j-v10-renault).
- **Engineers' dates are sometimes incomplete.** Those of the engineers named in this feature have been checked against their pages; others remain approximate. A missing departure date makes a presence uncertain, and the table says so.
- **The Indianapolis 500 (1950-1960) counted for the championship.** It is therefore included here, won by American constructors: [Kurtis Kraft]({{ site.baseurl }}/en/teams/kurtis-kraft/) has a page, Kuzma, Watson and Epperly do not.
- **The thresholds remain choices.** The "Robust" column shows which hegemonies withstand them.

## Sources

Results consulted on 29 October 2026 on formula1.com, for each season from 1950 to 2025:

- Grand Prix winners: `https://www.formula1.com/en/results/<year>/races`;
- constructors' standings, since 1958: `…/<year>/team`;
- drivers' standings: `…/<year>/drivers`.

The link to each race is kept in the site's data. Engineers, milestones and regulations come from the [team pages]({{ site.baseurl }}/en/teams/) and the [timeline]({{ site.baseurl }}/en/timeline/), where each has its own sources.
