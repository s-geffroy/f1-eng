---
title: "Regulation cycles: a new order for every rulebook?"
ordre: 7
resume: "Eleven cycles from 1950 to 2025: who dominates each new set of rules, how fast the order settles, and whether the team leading at the end of a cycle keeps its place in the next."
description: "Eleven cycles from 1950 to 2025: who dominates each new set of rules, how fast the order settles, and whether the team leading at the end of a cycle keeps its place in the next."
---
{%- assign CY = site.data.compteur.cycles -%}
{%- assign CP = site.data.compteur -%}
Formula 1's technical regulations change every year, but some seasons reset them almost completely: a new engine capacity, the end of the turbo, the hybrid power unit. This feature divides seventy-six seasons into {{ CY.size }} major cycles, each opened by one of these resets, and asks four questions:

1. Who dominates each cycle?
2. How locked is the cycle?
3. How fast does the order settle?
4. Does the team leading at the end of a cycle keep its place in the next?

The measures are those of the [Dominance feature]({{ site.baseurl }}/en/features/domination/): titles, wins and the composite index, the average share of wins, poles and podium places, out of 100.

## The essentials

- **New regulations almost always change the leader.** The team that wins most in the last season of a cycle stays ahead at the start of the next only 2 times out of 10: McLaren in 1989 and Red Bull in 2022.
- **The first season does not tell who will dominate.** It points to the cycle's dominant team 5 times out of 11. Brawn in 2009, Benetton in 1994 and Mercedes-Benz in 1954 lead the first season, then fade.
- **Recent cycles are the most locked.** Since 2009, the dominant team wins at least half the races of its cycle. The two longest cycles, 1954-1960 and 1966-1982, are the most open: their dominant team wins only a fifth of them.
- **A cycle can belong to an engine maker rather than a team.** From 1966 to 1982, no team wins more than 21% of the races, but Ford engines win 66% of them.

Contents
{:.sommaire-titre}

* TOC
{:toc}

## Eleven cycles

Each cycle opens with a reset of the technical regulations, described and sourced on the [timeline]({{ site.baseurl }}/en/timeline/): click on the dates in the table to read it. The first cycle covers the championship's first two seasons; in 1952 and 1953 the championship was run to Formula Two rules, which forms a cycle of its own. The last cycle ends in 2025: the [2026 regulations]({{ site.baseurl }}/en/timeline/#c-reglement-2026) open a new one.

<figure class="figure">
{% include domination/cycles-courbe-en.svg %}
<figcaption>The composite index of the strongest team in each season (hover over a dot to name it). Bands separate the cycles; above them, the cycle's opening year and the team that wins most in it. Red dashes: the threshold of {{ CP.seuil | times: 100 | round }}, above which a season is usually dominant.</figcaption>
</figure>

{% include domination.html quoi="cycles" %}

The cycles are of very unequal length, from two to seventeen seasons. Smaller rule changes stay within a cycle: high wings banned in 1969, the end of skirts in 1981, the restricted turbo of 1987-1988 or the switch to V8s in 2006.

## Who dominates each cycle

<figure class="figure">
{% include domination/cycles-cadrans-en.svg %}
<figcaption>One dial per cycle: the average index of the team that wins most in it (needle), and its best season of the cycle (black mark). Red mark: the threshold.</figcaption>
</figure>

Two families of cycles emerge.

- **Locked cycles.** Ferrari wins 82% of the races of the Formula Two championship (1952-1953), Mercedes 69% of those of the hybrid power unit (2014-2021), Alfa Romeo 67% of the first two seasons. Red Bull wins 60% of the races of the return of ground effect (2022-2025) and half of those of the aerodynamic overhaul (2009-2013).
- **Open cycles.** From 1954 to 1960, Ferrari wins only 21% of the races, and ten teams win at least once. From 1966 to 1982, Lotus wins as many, and eighteen teams win. These are the two longest cycles: rules that last give the chasers time to catch the leader.

The 3-litre cycle also shows that a cycle can be decided elsewhere than between teams. No team dominates it, but Ford engines, including the [Cosworth DFV]({{ site.baseurl }}/en/timeline/#j-dfv) sold to all, win 66% of the races. Likewise, the Climax engine wins 53% of the races of the 1.5-litre formula (1961-1965).

## How fast the order settles

{% include domination.html quoi="cycles_dynamique" %}

- **In 5 cycles out of 11, the team leading the first season dominates the whole cycle**: Alfa Romeo in 1950, Ferrari in 1952, McLaren in 1989, Mercedes in 2014 and Red Bull in 2022.
- **Elsewhere, the dominant team takes the lead after one or two seasons**, after a first leader that fades: Mercedes-Benz in 1954, Ferrari in 1961, Brabham in 1966, Ferrari in 1983, Brawn in 2009. The extreme case is the 1994-2008 cycle: Benetton, Williams and McLaren lead in turn, and Ferrari only takes the lead in 2000, six seasons into the cycle.
- **Once ahead, the dominant team stays there a long time** in recent cycles: Mercedes leads seven seasons out of eight from 2014 to 2021, Red Bull four out of five from 2009 to 2013. In the 1966-1982 cycle, Lotus leads only seven seasons out of seventeen, alternating with seven other teams.

The "Concentration" column gives the Herfindahl index of the cycle's wins: the sum of the squares of each team's share of wins, out of 100. It is 100 if a single team wins everything, and the lower the more the wins are spread. It ranges from {{ CY | map: "hhi" | sort | first | times: 100 | round }}, for the 1966-1982 cycle, to {{ CY | map: "hhi" | sort | last | times: 100 | round }}, for the Formula Two championship.

## From one cycle to the next

Of the ten handovers from one cycle to the next, the team leading the last season stays ahead only twice:

- **McLaren from 1988 to 1989**, from the end of the restricted turbo to the 3.5-litre normally aspirated engine. It goes from 94% to 62% of wins, and stays ahead.
- **Red Bull from 2021 to 2022**, from the hybrid power unit to the return of ground effect. It goes from 50% to 77% of wins.

The other eight times, the leader is dethroned, often abruptly. Ferrari goes from 78% of wins in 1953 to 22% in 1954. Cooper, from 60% in 1960 to no wins in 1961. Lotus, from 60% in 1965 to 11% in 1966. Red Bull, from 68% in 2013 to 16% in 2014.

This is the finding of the fourth comparison in the [Dominance feature]({{ site.baseurl }}/en/features/domination/#regulations): new regulations reshuffle the pack. At the scale of the major cycles, the effect is clearer still. A reset almost always costs the outgoing leader its place; the only question is who will take advantage of it.

## Method and limits

- **The division is a choice.** Only major resets of the technical regulations are retained; a finer division would give shorter cycles and different results.
- **The leader of a season** is the team that wins the most Grands Prix; in case of a tie, the one with the highest composite index. This is the case in 1983, when Ferrari, Brabham and Renault win four races each.
- **Cycles are of unequal length.** A two-season cycle does not compare exactly with a seventeen-season one.
- **The Indianapolis 500 counts towards the championship from 1950 to 1960**, and therefore in the first two cycles and in the 2.5-litre one.

## Sources

The results are those of formula1.com, recorded and cross-checked with the Jolpica database as explained in the [Dominance feature]({{ site.baseurl }}/en/features/domination/#sources). Each regulation that opens a cycle is described and sourced on the [timeline]({{ site.baseurl }}/en/timeline/).
