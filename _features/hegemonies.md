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
The [ranking]({{ site.baseurl }}/en/features/methode/) of engineers refuses to measure influence by results. This feature asks the opposite question: **do the innovations on the [timeline]({{ site.baseurl }}/en/timeline/) show up in the results?** To answer it, we first need to know when a team, a driver or an engine maker truly dominated. These periods are then set against three things: technical milestones, engineers' arrivals and departures, and changes of regulations.

The figures come from Formula 1's official results: the winner of each of the {{ P.gp }} championship Grands Prix held from 1950 to 2025, and the final drivers' and constructors' standings. They are computed by a program, not copied by hand. The champions derived from them match, season by season, those on the [team pages]({{ site.baseurl }}/en/teams/).

## What we call a hegemony

A title is not enough: it can be won narrowly. The number of wins alone is not enough either: a team can win a lot without being champion. Two criteria are therefore used. A season is **dominant** for a team, a driver or an engine maker if it is champion, **or** if it wins at least {{ P.seuil | times: 100 | round }}% of the Grands Prix.

A **hegemony** counts at least {{ P.min }} dominant seasons, separated by at most {{ P.creux }} lean season. The Williams of the 1990s is an example: beaten in 1995, it remains dominant before and after that season.

Two points to note:

- **Before 1958 there is no constructors' title.** The world champion's team stands in for it.
- **The thresholds are arbitrary.** Any threshold is. The calculation is therefore redone with three variants: more than 50% of wins, two seasons are enough, no lean season allowed. A hegemony found in all three variants is called **robust**, even if its limits shift a little.

Four levels are counted:

- the **team name**;
- the **lineage**, that is the same factory under several names, such as [Brackley]({{ site.baseurl }}/en/teams/), from Tyrrell to Mercedes;
- the **driver**;
- the **engine maker**.

## Teams

{% include hegemonies.html quoi="tableau" unite="ecurie" %}

Nine hegemonies in seventy-six seasons. Three features stand out.

- **The most crushing are the most recent.** [Mercedes]({{ site.baseurl }}/en/teams/mercedes/) wins 69% of the Grands Prix over eight seasons, from 2014 to 2021. [Red Bull]({{ site.baseurl }}/en/teams/red-bull/), from 2021 to 2023, wins 74% of them. The two hegemonies of the 1960s and 1970s, those of Lotus and Ferrari, win only about a third.
- **The longest is [Ferrari]({{ site.baseurl }}/en/teams/ferrari/)'s, from 1999 to 2008**: eight titles in ten seasons, interrupted only by 2005.
- **[Lotus]({{ site.baseurl }}/en/teams/team-lotus/), from 1968 to 1973, is not robust.** It alternates titles and lean seasons, and never exceeds 47% of wins.

Dominations of only two seasons are not counted as hegemonies: {% include hegemonies.html quoi="courtes" unite="ecurie" %}. They reappear as soon as the threshold is lowered to two seasons, and they are what makes the hegemonies of Lotus and of McLaren in 1998-2000 fragile.

At the level of **lineages** the table is almost the same. Red Bull becomes Milton Keynes, Mercedes becomes Brackley, and Enstone has only two dominations of two seasons, under the names Benetton (1994-1995) and Renault (2005-2006). No lineage forms a hegemony by adding up its successive names. Brackley, for example, wins with Brawn in 2009 and then with Mercedes from 2014, but the four seasons in between remain too lean.

{% include hegemonies.html quoi="tableau" unite="lignee" %}

## Drivers

{% include hegemonies.html quoi="tableau" unite="pilote" %}

Drivers' hegemonies almost always follow their team's: Schumacher with Ferrari, Vettel and Verstappen with Red Bull, Hamilton with Mercedes. There are two exceptions:

- **Fangio**, from 1954 to 1957, dominates with Mercedes-Benz, Ferrari and Maserati.
- **Stewart**, from 1969 to 1973, dominates with Matra, March and Tyrrell.

Their hegemony spans several teams: the driver changes car and keeps winning. Prost and Senna, for their part, share the same McLaren: their hegemonies overlap, and neither is robust.

Two-season dominations: {% include hegemonies.html quoi="courtes" unite="pilote" %}.

## Engine makers

{% include hegemonies.html quoi="tableau" unite="motoriste" %}

This is the level of the longest domination: that of the **Ford** engines, including the [Cosworth DFV]({{ site.baseurl }}/en/timeline/#j-dfv). They are dominant fifteen seasons out of fifteen, from 1968 to 1982, and win 70% of the Grands Prix, for Lotus, McLaren, Tyrrell and others.

The DFV is sold to everyone. So there is no team hegemony that matches it, but a succession of champion teams with the same engine. Climax before it, then Honda and Renault, dominate in the same way across several teams.

The Mercedes engine of 2012-2021 begins before the Mercedes team. It first wins with McLaren, then with Mercedes and Racing Point.

## Innovations and results: three comparisons

### Method

The word "correlation" would be misleading: the timeline has 43 milestones, far too few for statistics. The comparisons are therefore **before / after**, and each is measured against a **control**. The control is what would be observed at any season, for the same teams.

The vocabulary is that of the [feature on causality]({{ site.baseurl }}/en/features/causalite/). That a hegemony follows a milestone is a **chronological** overlap, never proof. A link is more than chronological only if the timeline already establishes it with a source.

### 1. Technical milestones

Each milestone is attached to the team that carried it, according to the team pages. Its share of wins is compared over the two seasons before the milestone and the three seasons starting with it. We also check whether a hegemony begins within two years.

{% include hegemonies.html quoi="jalons" %}

Of {{ TJ.n }} milestones carried by a team that was not yet dominating, **{{ TJ.ouvre }} shortly precede a hegemony**:

- the [DFV]({{ site.baseurl }}/en/timeline/#j-dfv) at Lotus in 1967;
- the [312T]({{ site.baseurl }}/en/timeline/#j-ferrari-312t) at Ferrari in 1975;
- the [MP4/4]({{ site.baseurl }}/en/timeline/#j-mp4-4) at McLaren in 1988;
- the [RB6]({{ site.baseurl }}/en/timeline/#j-rb6) at Red Bull in 2010;
- the [hybrid power unit]({{ site.baseurl }}/en/timeline/#j-hybride) at Mercedes in 2014.

The control takes the same teams at any season in which they do not dominate. It expects about {{ TJ.attendu }}. **Milestones therefore precede a hegemony about twice as often as chance, but on five cases.** It is a clue, not a demonstration.

The counter-examples outnumber the examples, and they are instructive.

- **Innovation without hegemony.** The [Lotus 78]({{ site.baseurl }}/en/timeline/#j-lotus-78) takes Lotus from 3% to 27% of wins, with no hegemony following. The [1993 Benetton]({{ site.baseurl }}/en/timeline/#j-cfd-benetton) takes its team from 6% to 40%, for only two seasons of domination. The [double diffuser]({{ site.baseurl }}/en/timeline/#j-double-diffuseur) brings Brawn a title in 2009, then the team changes name. The carbon [MP4/1]({{ site.baseurl }}/en/timeline/#j-mp4-1) leads McLaren to only two titles, in 1984 and 1985.
- **Innovation during a hegemony.** The [FW14B]({{ site.baseurl }}/en/timeline/#j-fw14b), the [Lotus 72]({{ site.baseurl }}/en/timeline/#j-lotus-72) and the [RB18]({{ site.baseurl }}/en/timeline/#j-rb18) arrive when their team is already dominating. They extend it; they do not open it.
- **Hegemony without a milestone.** No timeline milestone accompanies Ferrari's in 1999-2008, nor McLaren's in 1998-2000. The milestones on the timeline do not explain them: they rest on something else, or on innovations the timeline does not include.

### 2. Engineers

The team pages date each engineer's arrival and departure. For an **arrival**, the team's share of wins is compared over the two seasons before and the three starting with the engineer. For a **departure**, the last two seasons with him are compared with the next three. A difference of more than 5 points counts as a rise or a fall.

{% include hegemonies.html quoi="ingenieurs" %}

Two findings:

- **A team improves after an arrival more often than at any season**: {{ BI.arrivee.hausse | times: 100.0 | divided_by: BI.arrivee.n | round }}% of cases, against {{ BI.temoin.hausse | times: 100.0 | divided_by: BI.temoin.n | round }}% for the control.
- **A departure changes almost nothing.** Rises and falls balance out, roughly as in the control.

The simplest reading, "the engineer makes the team win", is not the only one. A rising team also has the means to recruit. The arrival may therefore accompany the rise as much as cause it. A departure with no visible effect suggests that an organisation keeps its momentum for a few seasons after an engineer leaves.

The reverse view is more telling: who was there when each hegemony began? An engineer is counted if he arrived before the start and left at most three seasons before it. When his departure date is not known and he arrived more than three seasons earlier, his presence is marked as uncertain.

{% include hegemonies.html quoi="racines" %}

Two engineers are present at the start of three of the nine team hegemonies:

- [Adrian Newey]({{ site.baseurl }}/en/engineers/adrian-newey/): Williams 1991, McLaren 1998 and Red Bull 2010, plus Red Bull 2021, where his presence is uncertain because no departure date from Red Bull is recorded;
- [Geoff Willis]({{ site.baseurl }}/en/engineers/geoff-willis/): Williams 1991, Red Bull 2010 and Mercedes 2014.

[Ross Brawn]({{ site.baseurl }}/en/engineers/ross-brawn/) is present at the start of two hegemonies, Ferrari 1999 and Mercedes 2014, and perhaps a third, Williams 1991. This does not measure their merit, which the [ranking]({{ site.baseurl }}/en/features/methode/) assesses differently: it locates where they were.

### 3. Regulations

For each start of a hegemony, whether of a team, a driver or an engine maker, we look for a change of regulations on the timeline in the same year or the year before. For each end, we look for one in the year of the last dominant season or the year after.

**{{ TR.debuts_regle }} starts out of {{ TR.debuts }}** coincide with a change of regulations, and **{{ TR.fins_regle }} ends out of {{ TR.fins }}**. But these changes are so frequent that {{ TR.avec_regle }} seasons out of {{ TR.annees }} have one in the same window: roughly the same proportion. **On average, a change of regulations does not open or close a hegemony more often than an ordinary season.**

Some coincidences are nevertheless clear:

- the [mandatory hybrid power unit]({{ site.baseurl }}/en/timeline/#c-groupe-propulseur-2014) of 2014 shortly precedes the hegemonies of Mercedes and of Hamilton;
- the [2009 aerodynamic overhaul]({{ site.baseurl }}/en/timeline/#c-refonte-aero-2009) precedes Red Bull's;
- the [return of ground effect]({{ site.baseurl }}/en/timeline/#c-retour-effet-de-sol), in 2022, shortly follows the end of Mercedes';
- the [3-litre formula]({{ site.baseurl }}/en/timeline/#c-formule-3-litres), in 1966, shortly follows the end of Climax's;
- the [flat bottom]({{ site.baseurl }}/en/timeline/#c-fond-plat), in 1983, shortly follows the end of Ford's.

In all five cases it is an overall redesign of the cars or engines, not a mere adjustment. These coincidences remain chronological: the timeline draws no sourced link between these regulations and the results.

## Limits

- **Wins are not the only measure.** They ignore teams that improve without winning, and they also reflect the driver's talent, reliability and budgets.
- **The milestones are a selection.** The timeline keeps the innovations that changed how cars are designed, not those that won races. A hegemony without a milestone may hide an innovation the timeline does not include.
- **Attaching a milestone to a team follows the team pages.** Four milestones are attached to no team, and are therefore not counted: the [Cooper 500 prototype]({{ site.baseurl }}/en/timeline/#j-cooper-500), the [FVA]({{ site.baseurl }}/en/timeline/#j-dfv-fva), [pneumatic valve springs]({{ site.baseurl }}/en/timeline/#j-rappel-pneumatique) and the [Renault V10]({{ site.baseurl }}/en/timeline/#j-v10-renault).
- **Engineers' dates are sometimes incomplete.** A missing departure date makes a presence uncertain, and the table says so.
- **The Indianapolis 500 (1950-1960) counted for the championship.** It is therefore included here, won by American constructors that have no page on the site.
- **The thresholds remain choices.** The "Robust" column shows which hegemonies withstand them.

## Sources

Results consulted on 29 October 2026 on formula1.com, for each season from 1950 to 2025:

- Grand Prix winners: `https://www.formula1.com/en/results/<year>/races`;
- constructors' standings, since 1958: `…/<year>/team`;
- drivers' standings: `…/<year>/drivers`.

The link to each race is kept in the site's data. Engineers, milestones and regulations come from the [team pages]({{ site.baseurl }}/en/teams/) and the [timeline]({{ site.baseurl }}/en/timeline/), where each has its own sources.
