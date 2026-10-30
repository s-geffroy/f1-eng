---
title: "Indicators: what seventy-six seasons of results say about F1"
ordre: 8
resume: "Four measures drawn from the 1,149 Grands Prix from 1950 to 2025: how many teams share the wins, what an in-house engine is worth, what a pole is worth and how long a winning car lasts."
description: "Four measures drawn from the 1,149 Grands Prix from 1950 to 2025: how many teams share the wins, what an in-house engine is worth, what a pole is worth and how long a winning car lasts."
---
{%- assign I = site.data.compteur.indicateurs -%}
{%- assign OD = I.ouverture.decennies -%}
{%- assign MD = I.client.decennies -%}
{%- assign PD = I.pole.decennies -%}
{%- assign VD = I.voitures.decennies -%}
{%- assign F0 = I.ouverture.plus_fermees[0] -%}
{%- assign F1 = I.ouverture.plus_fermees[1] -%}
{%- assign F2 = I.ouverture.plus_fermees[2] -%}
{%- assign O0 = I.ouverture.plus_ouvertes[0] -%}
{%- assign RE = I.ouverture.record_ecuries -%}
{%- assign RT = I.pole.ecuries | where: "id", "renault-1977" | first -%}
{%- assign RB = I.pole.ecuries | where: "id", "red-bull" | first -%}
The [Dominance feature]({{ site.baseurl }}/en/features/domination/) asks who dominates, and when. This feature starts from the same results, the {% include nombre.html n=I.client.gp %} championship Grands Prix from 1950 to 2025, and asks four other questions:

1. Is F1 more closed than it used to be?
2. Does a team need to build its own engine to win?
3. What is a pole position worth?
4. How long does a winning car last?

Each measure is computed by decade and by [regulation cycle]({{ site.baseurl }}/en/features/cycles/).

## The essentials

- **The most open F1 is that of the 1970s and 1980s.** On average, {{ OD[2].effectif }} "effective" teams share the wins in the 1970s, against {{ OD[6].effectif }} since 2010. The most open season is {{ O0.annee }}, with {{ RE.ecuries }} winning teams and {{ RE.pilotes }} winning drivers; the most closed, {{ F0.annee }}.
- **The in-house engine disappeared, then came back.** From 1960 to 1999, more than three wins in four go to a team supplied by an engine maker. In the 2000s and 2010s, the team that also builds its engine wins about six races in ten ({{ MD[5].part_maison | times: 100 | round }}% then {{ MD[6].part_maison | times: 100 | round }}%).
- **Pole is worth more than it used to be.** The driver starting from pole wins {{ I.pole.taux | times: 100 | round }}% of Grands Prix. The rate drops to {{ PD[3].taux | times: 100 | round }}% in the 1980s and rises to {{ PD[7].taux | times: 100 | round }}% since 2020.
- **Cars win more, but no longer last.** A winning car takes on average {{ VD[0].victoires_par_modele }} Grands Prix in the 1950s, {{ VD[7].victoires_par_modele }} since 2020. Up to the 1980s, nearly one win in three goes to a car that had already won in an earlier season; since 2004, this has almost stopped happening.

Contents
{:.sommaire-titre}

* TOC
{:toc}

## Is F1 more closed than it used to be?

Counting the teams that win at least one race is not enough: a season where one team wins every race but one counts two winning teams, just like a season split half and half. The **effective number of winning teams** corrects this bias. It is the inverse of the Herfindahl index of win shares: it equals 1 if a single team wins everything, 2 if two teams share the wins equally, and so on.

<figure class="figure">
{% include domination/indic-ouverture-en.svg %}
<figcaption>Solid line: the effective number of winning teams in each season (hover over a point for details). Dashes: the number of teams that won at least one race. Grey bands separate the regulation cycles.</figcaption>
</figure>

- **The peak comes at the turn of the 1980s.** {{ O0.annee }} is the most open season in history: {{ RE.ecuries }} different teams and {{ RE.pilotes }} different drivers win one of the {{ RE.gp }} races, and the effective number reaches {{ O0.effectif }}. The next four seasons in the ranking come from the same era: {{ I.ouverture.plus_ouvertes[1].annee }}, {{ I.ouverture.plus_ouvertes[2].annee }}, {{ I.ouverture.plus_ouvertes[3].annee }} and {{ I.ouverture.plus_ouvertes[4].annee }}.
- **Two of the three most closed seasons are recent.** In {{ F0.annee }}, the effective number falls to {{ F0.effectif }}; next come {{ F1.annee }} ({{ F1.effectif }}) and {{ F2.annee }} ({{ F2.effectif }}).
- **Since the 1990s, openness has levelled off.** The average effective number no longer exceeds {{ OD[4].effectif }} per decade, although the calendar has twice as many races as in 1970. More races do not spread the wins further.
- **Titles are rarely close.** The constructors' title margin is the share of the champion's points that the runner-up lacks. It averages {{ OD[2].ecart_titre | times: 100 | round }}% in the 1970s, {{ OD[3].ecart_titre | times: 100 | round }}% in the 1980s and {{ OD[7].ecart_titre | times: 100 | round }}% since 2020.

This qualifies the finding of the [Cycles feature]({{ site.baseurl }}/en/features/cycles/): the two cycles in which the dominant team wins least, 1954-1960 and 1966-1982, are not both among the most open by the effective number: 1966-1982, the longest, is the most open of all, but 1954-1960 ranks only fifth out of eleven.

## Does a team need to build its own engine to win?

A win counts **with an in-house engine** when the winning team also builds its engine: Ferrari, Mercedes, Renault, BRM, or Honda in its years as a team. Otherwise, the team gets its engine from an **engine maker**: bought, like the Cosworth DFV, or supplied in a works partnership, like Williams-Honda or McLaren-Mercedes.

<figure class="figure">
{% include domination/indic-moteur-en.svg %}
<figcaption>Share of the decade's Grands Prix won with an in-house engine (blue) and with an engine maker's engine (grey). Hover over a bar for details.</figcaption>
</figure>

- **Three ages follow one another.** In the 1950s, Alfa Romeo, Ferrari, Maserati, Mercedes-Benz and Vanwall win {{ MD[0].part_maison | times: 100 | round }}% of races with their own engine. From 1960 to 1999, the British teams that buy their engines take over: the in-house engine falls to {{ MD[4].part_maison | times: 100 | round }}% in the 1990s. It returns in the 2000s with Ferrari and Renault, then with Mercedes: {{ MD[6].part_maison | times: 100 | round }}% of wins in the 2010s.
- **Titles are split almost evenly.** Of {{ I.client.titres }} seasons, {{ I.client.titres_maison }} are won by a team that builds its engine: a little under half.
- **Since 2020, the partnership has won out again**: Red Bull with Honda, then McLaren with Mercedes do not build their engines, and the in-house engine falls back to {{ MD[7].part_maison | times: 100 | round }}%.

{% include domination.html quoi="indic_couples" %}

The most successful pairing without an in-house engine is McLaren-Mercedes, from 1997 to 2025. The DFV-powered Lotus-Ford, from 1967 to 1982, remains the model of the team that buys its engine off the shelf: [Keith Duckworth's entry]({{ site.baseurl }}{% link _engineers/keith-duckworth.md %}) tells how this engine opened the way to victory for small teams.

## What is a pole position worth?

A pole counts as converted when its driver wins the race; for a shared win, one of the two drivers starting from pole is enough. The starting grid is published for all {{ I.pole.gp }} races.

<figure class="figure">
{% include domination/indic-pole-en.svg %}
<figcaption>Share of the decade's Grands Prix won by the driver who started from pole position.</figcaption>
</figure>

- **Pole has never counted for less than in the 1980s**: {{ PD[3].taux | times: 100 | round }}% conversion. The worst season is {{ I.pole.saison_min.annee }}, when the pole-sitter wins only {{ I.pole.saison_min.convertis }} races out of {{ I.pole.saison_min.gp }}. The turbo years, when an engine tuned for a qualifying lap did not always last the distance, are one possible explanation; this feature does not test it.
- **Since the 2000s, pole decides one race in two**, and even more since 2020 ({{ PD[7].taux | times: 100 | round }}%). The record over a season is {{ I.pole.saison_max.annee }}: {{ I.pole.saison_max.convertis }} races out of {{ I.pole.saison_max.gp }}.
- **Not every team converts in the same way.** Red Bull turns {{ RB.taux | times: 100 | round }}% of its poles into wins. The Renault of the turbo years, by contrast, converts only {{ RT.taux | times: 100 | round }}%: {{ RT.poles }} poles, {{ RT.convertis }} wins.

{% include domination.html quoi="indic_pole" %}

## How long does a winning car last? {#voitures}

The [Dominance feature]({{ site.baseurl }}/en/features/domination/#cars) records the winning model of every Grand Prix and names the most crushing and the most durable cars. Here we measure renewal: how many wins a car takes, and what share of wins goes to a carried-over car, meaning one that had already won in an earlier season. A model and its evolutions marked by a letter (Lotus 72 to 72E, McLaren MP4/2 to MP4/2C) count as a single car.

<figure class="figure">
{% include domination/indic-voitures-en.svg %}
<figcaption>Average number of Grands Prix won by each winning car of the decade.</figcaption>
</figure>

- **Each winning car wins more and more.** {{ VD[0].victoires_par_modele }} wins on average in the 1950s, {{ VD[7].victoires_par_modele }} since 2020. Longer seasons contribute, but not only: there are also fewer winning cars per season ({{ VD[2].par_saison }} on average in the 1970s, {{ VD[6].par_saison }} in the 2010s). The record is {{ I.voitures.record_modeles.annee }}, with {{ I.voitures.record_modeles.modeles }} different winning cars.
- **A car no longer survives the winter.** Up to the 1980s, about three wins in ten go to a carried-over car. The share falls to {{ VD[4].part_reconduites | times: 100 | round }}% in the 1990s, then to almost nothing: after the Ferrari F2002 and the McLaren MP4-17D, in 2003, no car wins in two consecutive seasons until the Red Bull RB16B of {{ I.voitures.derniere_reconduite.annee }}, an evolution of the 2020 RB16.

## Decade by decade, cycle by cycle

{% include domination.html quoi="indic_decennies" %}

{% include domination.html quoi="indic_cycles" %}

## Method and limits

- **Shared wins count once**, as throughout the site: {% include nombre.html n=I.client.gp %} Grands Prix from 1950 to 2025.
- **The Indianapolis 500 counts from 1950 to 1960**, as in the championship. Its winners, all Offenhauser-powered, count as without an in-house engine.
- **The constructors' title margin** only exists since 1958: the 1950s average covers only 1958 and 1959, and the first two cycles have none.
- **In-house engine**: the list of teams that build their engine is written in `outils/domination.py`. Badged engines are credited to their builder: the RBPT engine of 2022 to 2025 is a Honda. BMW Sauber (2006-2009, owned by BMW) counts as an in-house engine. A works partnership counts as an engine maker's engine, even when the engine maker is a shareholder in the team: McLaren-Mercedes, for instance.
- **The number of wins per car** depends on season length: 7 to 11 Grands Prix in the 1950s, more than 20 today. The two other car measures, cars per season and carried-over cars, do not.
- **An evolution without a final letter** (Ferrari 312T2 after the 312T) counts as a new car, as in the Dominance feature.

## Sources

Results, poles and points come from formula1.com, collected and cross-checked against the Jolpica database as explained in the [Dominance feature]({{ site.baseurl }}/en/features/domination/#sources), which also sources the winning model of every Grand Prix. Regulation cycles are described and sourced in the [timeline]({{ site.baseurl }}/en/timeline/). Calculations are made by `outils/domination.py`.
