---
title: "Indicateurs : ce que soixante-seize saisons de résultats disent de la F1"
ordre: 8
resume: "Quatre mesures tirées des 1149 Grands Prix de 1950 à 2025 : combien d'écuries se partagent les victoires, ce que pèse un moteur maison, ce que vaut une pole et combien de temps dure une voiture gagnante."
description: "Quatre mesures tirées des 1149 Grands Prix de 1950 à 2025 : combien d'écuries se partagent les victoires, ce que pèse un moteur maison, ce que vaut une pole et combien de temps dure une voiture gagnante."
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
Le [dossier Domination]({{ site.baseurl }}/dossiers/domination/) cherche qui domine, et quand. Ce dossier part des mêmes résultats, les {{ I.client.gp }} Grands Prix du championnat de 1950 à 2025, et pose quatre autres questions :

1. La F1 est-elle plus fermée qu'avant ?
2. Faut-il construire son moteur pour gagner ?
3. Que vaut une pole position ?
4. Combien de temps une voiture gagnante dure-t-elle ?

Chaque mesure est calculée par décennie et par [cycle réglementaire]({{ site.baseurl }}/dossiers/cycles/).

## L'essentiel

- **La F1 la plus ouverte est celle des années 1970 et 1980.** En moyenne, {{ OD[2].effectif | replace: ".", "," }} écuries « effectives » se partagent les victoires dans les années 1970, contre {{ OD[6].effectif | replace: ".", "," }} depuis 2010. La saison la plus ouverte est {{ O0.annee }}, avec {{ RE.ecuries }} écuries et {{ RE.pilotes }} pilotes vainqueurs ; la plus fermée, {{ F0.annee }}.
- **Le moteur maison a disparu, puis il est revenu.** De 1960 à 1999, plus de trois victoires sur quatre reviennent à une écurie qui reçoit son moteur d'un motoriste. Dans les années 2000 et 2010, l'écurie qui construit aussi son moteur gagne environ six courses sur dix ({{ MD[5].part_maison | times: 100 | round }} % puis {{ MD[6].part_maison | times: 100 | round }} %).
- **La pole vaut plus qu'avant.** Le pilote parti en pole gagne {{ I.pole.taux | times: 100 | round }} % des Grands Prix. Ce taux tombe à {{ PD[3].taux | times: 100 | round }} % dans les années 1980 et monte à {{ PD[7].taux | times: 100 | round }} % depuis 2020.
- **Les voitures gagnent davantage, mais ne durent plus.** Une voiture gagnante remporte en moyenne {{ VD[0].victoires_par_modele | replace: ".", "," }} Grands Prix dans les années 1950, {{ VD[7].victoires_par_modele | replace: ".", "," }} depuis 2020. Jusqu'aux années 1980, près d'une victoire sur trois revient à une voiture déjà gagnante la saison précédente ; depuis 2004, cela n'arrive presque plus.

Sommaire
{:.sommaire-titre}

* TOC
{:toc}

## La F1 est-elle plus fermée qu'avant ?

Compter les écuries qui gagnent au moins une course ne suffit pas : une saison où une écurie gagne tout sauf une course compte deux écuries gagnantes, comme une saison partagée moitié-moitié. Le **nombre effectif d'écuries gagnantes** corrige ce biais. C'est l'inverse de l'indice de Herfindahl des parts de victoires : il vaut 1 si une seule écurie gagne tout, 2 si deux écuries se partagent les victoires à égalité, et ainsi de suite.

<figure class="figure">
{% include domination/indic-ouverture-fr.svg %}
<figcaption>Trait plein : le nombre effectif d'écuries gagnantes de chaque saison (survolez un point pour le détail). Tirets : le nombre d'écuries qui ont gagné au moins une course. Les bandes grises séparent les cycles réglementaires.</figcaption>
</figure>

- **Le sommet est au tournant des années 1980.** {{ O0.annee }} est la saison la plus ouverte de l'histoire : {{ RE.ecuries }} écuries et {{ RE.pilotes }} pilotes différents gagnent l'une des {{ RE.gp }} courses, et le nombre effectif atteint {{ O0.effectif | replace: ".", "," }}. Les quatre saisons suivantes du classement datent de la même époque : {{ I.ouverture.plus_ouvertes[1].annee }}, {{ I.ouverture.plus_ouvertes[2].annee }}, {{ I.ouverture.plus_ouvertes[3].annee }} et {{ I.ouverture.plus_ouvertes[4].annee }}.
- **Deux des trois saisons les plus fermées sont récentes.** En {{ F0.annee }}, le nombre effectif tombe à {{ F0.effectif | replace: ".", "," }} ; viennent ensuite {{ F1.annee }} ({{ F1.effectif | replace: ".", "," }}) et {{ F2.annee }} ({{ F2.effectif | replace: ".", "," }}).
- **Depuis les années 1990, l'ouverture plafonne.** Le nombre effectif moyen ne dépasse plus {{ OD[4].effectif | replace: ".", "," }} par décennie, alors que le calendrier compte deux fois plus de courses qu'en 1970. Plus de courses ne disperse pas davantage les victoires.
- **Les titres se jouent rarement de près.** L'écart au titre constructeurs est la part des points du champion qui manque au deuxième. Il est en moyenne de {{ OD[2].ecart_titre | times: 100 | round }} % dans les années 1970, de {{ OD[3].ecart_titre | times: 100 | round }} % dans les années 1980 et de {{ OD[7].ecart_titre | times: 100 | round }} % depuis 2020.

Le constat rejoint celui du [dossier Cycles]({{ site.baseurl }}/dossiers/cycles/) : les deux cycles les plus longs, 1954-1960 et 1966-1982, sont aussi les plus ouverts.

## Faut-il construire son moteur pour gagner ?

Une victoire est comptée **avec moteur maison** quand l'écurie gagnante construit aussi son moteur : Ferrari, Mercedes, Renault, BRM ou Honda dans ses années d'écurie. Sinon, l'écurie reçoit son moteur d'un **motoriste** : acheté comme le Cosworth DFV, ou fourni dans un partenariat d'usine comme Williams-Honda ou McLaren-Mercedes.

<figure class="figure">
{% include domination/indic-moteur-fr.svg %}
<figcaption>Part des Grands Prix de la décennie gagnés avec un moteur maison (bleu) et avec le moteur d'un motoriste (gris). Survolez une barre pour le détail.</figcaption>
</figure>

- **Trois âges se succèdent.** Dans les années 1950, Alfa Romeo, Ferrari, Maserati, Mercedes-Benz et Vanwall gagnent {{ MD[0].part_maison | times: 100 | round }} % des courses avec leur propre moteur. De 1960 à 1999, les écuries britanniques qui achètent leur moteur prennent le dessus : le moteur maison tombe à {{ MD[4].part_maison | times: 100 | round }} % dans les années 1990. Il revient dans les années 2000 avec Ferrari et Renault, puis avec Mercedes : {{ MD[6].part_maison | times: 100 | round }} % des victoires des années 2010.
- **Les titres se partagent presque à égalité.** Sur {{ I.client.titres }} saisons, {{ I.client.titres_maison }} sont remportées par une écurie qui construit son moteur : un peu moins de la moitié.
- **Depuis 2020, le partenariat l'emporte à nouveau** : Red Bull avec Honda, puis McLaren avec Mercedes ne construisent pas leur moteur, et le moteur maison retombe à {{ MD[7].part_maison | times: 100 | round }} %.

{% include domination.html quoi="indic_couples" %}

Le couple le plus victorieux sans moteur maison est McLaren-Mercedes, de 1997 à 2025. La Lotus-Ford du DFV, de 1967 à 1982, reste le modèle de l'écurie qui achète son moteur au catalogue : la [fiche de Keith Duckworth]({{ site.baseurl }}{% link _ingenieurs/keith-duckworth.md %}) raconte comment ce moteur a ouvert la victoire aux petites écuries.

## Que vaut une pole position ?

On compte comme convertie une pole dont le pilote gagne la course ; pour une victoire partagée, il suffit que l'un des deux pilotes soit parti en pole. La grille de départ est publiée pour chacune des {{ I.pole.gp }} courses.

<figure class="figure">
{% include domination/indic-pole-fr.svg %}
<figcaption>Part des Grands Prix de la décennie gagnés par le pilote parti en pole position.</figcaption>
</figure>

- **La pole n'a jamais aussi peu pesé que dans les années 1980** : {{ PD[3].taux | times: 100 | round }} % de conversion. Le pire est {{ I.pole.saison_min.annee }}, où le poleman ne gagne que {{ I.pole.saison_min.convertis }} courses sur {{ I.pole.saison_min.gp }}. Les années turbo, où un moteur réglé pour un tour de qualification ne tenait pas toujours la distance, sont une explication possible ; ce dossier ne la teste pas.
- **Depuis les années 2000, la pole décide une course sur deux**, et plus encore depuis 2020 ({{ PD[7].taux | times: 100 | round }} %). Le record sur une saison est {{ I.pole.saison_max.annee }} : {{ I.pole.saison_max.convertis }} courses sur {{ I.pole.saison_max.gp }}.
- **Toutes les écuries ne convertissent pas de la même façon.** Red Bull transforme {{ RB.taux | times: 100 | round }} % de ses poles en victoire. La Renault des années turbo, à l'inverse, n'en convertit que {{ RT.taux | times: 100 | round }} % : {{ RT.poles }} poles, {{ RT.convertis }} victoires.

{% include domination.html quoi="indic_pole" %}

## Combien de temps une voiture gagnante dure-t-elle ? {#voitures}

Le [dossier Domination]({{ site.baseurl }}/dossiers/domination/#les-voitures) relève le modèle gagnant de chaque Grand Prix et nomme les voitures les plus écrasantes et les plus durables. On mesure ici le renouvellement : combien de victoires remporte une voiture, et quelle part des victoires revient à une voiture reconduite, c'est-à-dire déjà gagnante une saison précédente. Un modèle et ses évolutions désignées par une lettre (Lotus 72 à 72E, McLaren MP4/2 à MP4/2C) forment une seule voiture.

<figure class="figure">
{% include domination/indic-voitures-fr.svg %}
<figcaption>Nombre moyen de Grands Prix gagnés par chaque voiture gagnante de la décennie.</figcaption>
</figure>

- **Chaque voiture gagnante gagne de plus en plus.** {{ VD[0].victoires_par_modele | replace: ".", "," }} victoires en moyenne dans les années 1950, {{ VD[7].victoires_par_modele | replace: ".", "," }} depuis 2020. Les saisons plus longues y contribuent, mais pas seulement : il y a aussi moins de voitures gagnantes par saison ({{ VD[2].par_saison | replace: ".", "," }} en moyenne dans les années 1970, {{ VD[6].par_saison | replace: ".", "," }} dans les années 2010). Le record est {{ I.voitures.record_modeles.annee }}, avec {{ I.voitures.record_modeles.modeles }} voitures gagnantes différentes.
- **Une voiture ne passe plus l'hiver.** Jusqu'aux années 1980, environ trois victoires sur dix reviennent à une voiture reconduite. La part tombe à {{ VD[4].part_reconduites | times: 100 | round }} % dans les années 1990, puis à presque rien : après la Ferrari F2002 et la McLaren MP4-17D, en 2003, aucune voiture ne gagne plus deux saisons de suite jusqu'à la Red Bull RB16B de {{ I.voitures.derniere_reconduite.annee }}, évolution de la RB16 de 2020.

## Décennie par décennie, cycle par cycle

{% include domination.html quoi="indic_decennies" %}

{% include domination.html quoi="indic_cycles" %}

## Méthode et limites

- **Les victoires partagées comptent une fois**, comme dans tout le site : {{ I.client.gp }} Grands Prix de 1950 à 2025.
- **Les 500 miles d'Indianapolis comptent de 1950 à 1960**, comme au championnat. Leurs vainqueurs, tous à moteur Offenhauser, sont comptés sans moteur maison.
- **L'écart au titre constructeurs** n'existe que depuis 1958 : la moyenne des années 1950 ne porte que sur 1958 et 1959, et les deux premiers cycles n'en ont pas.
- **Moteur maison** : la liste des écuries qui construisent leur moteur est écrite dans `outils/domination.py`. Les moteurs badgés sont rendus à leur constructeur : le moteur RBPT de 2022 à 2025 est un Honda. BMW-Sauber (2006-2009, propriété de BMW) compte comme moteur maison. Un partenariat d'usine compte comme moteur d'un motoriste, même quand le motoriste est actionnaire de l'écurie : McLaren-Mercedes, par exemple.
- **Le nombre de victoires par voiture** dépend de la longueur des saisons : 7 à 9 Grands Prix dans les années 1950, plus de 20 aujourd'hui. Les deux autres mesures de voitures, voitures par saison et voitures reconduites, n'en dépendent pas.
- **Une évolution sans lettre finale** (Ferrari 312T2 après la 312T) compte comme une nouvelle voiture, comme dans le dossier Domination.

## Sources

Les résultats, les poles et les points sont ceux de formula1.com, relevés et croisés avec la base Jolpica comme l'explique le [dossier Domination]({{ site.baseurl }}/dossiers/domination/#sources), qui source aussi le modèle gagnant de chaque Grand Prix. Les cycles réglementaires sont décrits et sourcés dans la [chronologie]({{ site.baseurl }}/chronologie/). Les calculs sont faits par `outils/domination.py`.
