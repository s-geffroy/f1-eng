---
title: "Les cycles réglementaires : à chaque règlement, sa hiérarchie ?"
ordre: 7
resume: "Onze cycles de 1950 à 2025 : qui domine chaque nouveau règlement, à quelle vitesse la hiérarchie se fige, et si l'écurie qui mène à la fin d'un cycle garde sa place dans le suivant."
description: "Onze cycles de 1950 à 2025 : qui domine chaque nouveau règlement, à quelle vitesse la hiérarchie se fige, et si l'écurie qui mène à la fin d'un cycle garde sa place dans le suivant."
---
{%- assign CY = site.data.compteur.cycles -%}
{%- assign CP = site.data.compteur -%}
Le règlement technique de la Formule 1 change chaque année, mais certaines saisons le remettent presque entièrement à zéro : une nouvelle cylindrée, la fin du turbo, le groupe propulseur hybride. Ce dossier découpe soixante-seize saisons en {{ CY.size }} grands cycles, chacun ouvert par l'une de ces remises à zéro, et pose quatre questions :

1. Qui domine chaque cycle ?
2. À quel point le cycle est-il verrouillé ?
3. À quelle vitesse la hiérarchie se fige-t-elle ?
4. L'écurie qui mène à la fin d'un cycle garde-t-elle sa place dans le suivant ?

Les mesures sont celles du [dossier Domination]({{ site.baseurl }}/dossiers/domination/) : titres, victoires et indice composite, la moyenne des parts de victoires, de poles et de places sur le podium, sur 100.

## L'essentiel

- **Un nouveau règlement change presque toujours de meneur.** L'écurie qui gagne le plus lors de la dernière saison d'un cycle ne reste en tête au début du suivant que 2 fois sur 10 : McLaren en 1989 et Red Bull en 2022.
- **La première saison ne dit pas qui dominera.** Elle désigne l'écurie dominante du cycle 5 fois sur 11. Brawn en 2009, Benetton en 1994 et Mercedes-Benz en 1954 mènent la première saison, puis s'effacent.
- **Les cycles récents sont les plus verrouillés.** Depuis 2009, l'écurie dominante gagne au moins la moitié des courses de son cycle. Les deux cycles les plus longs, 1954-1960 et 1966-1982, sont les plus ouverts : leur écurie dominante n'en gagne qu'un cinquième.
- **Un cycle peut appartenir à un motoriste plutôt qu'à une écurie.** De 1966 à 1982, aucune écurie ne gagne plus de 21 % des courses, mais les moteurs Ford en gagnent 66 %.

Sommaire
{:.sommaire-titre}

* TOC
{:toc}

## Onze cycles

Chaque cycle s'ouvre avec une remise à zéro du règlement technique, décrite et sourcée dans la [chronologie]({{ site.baseurl }}/chronologie/) : cliquez sur les dates du tableau pour la lire. Le premier cycle couvre les deux premières saisons du championnat ; en 1952 et 1953, le championnat se court selon le règlement de la Formule 2, ce qui forme un cycle à part. Le dernier cycle s'achève en 2025 : le [règlement de 2026]({{ site.baseurl }}/chronologie/#c-reglement-2026) en ouvre un nouveau.

<figure class="figure">
{% include domination/cycles-courbe-fr.svg %}
<figcaption>L'indice composite de l'écurie la plus forte de chaque saison (survolez un point pour la nommer). Les bandes séparent les cycles ; au-dessus, l'année d'ouverture du cycle et l'écurie qui y gagne le plus. Tirets rouges : le seuil de {{ CP.seuil | times: 100 | round }}, au-dessus duquel une saison est le plus souvent dominante.</figcaption>
</figure>

{% include domination.html quoi="cycles" %}

Les cycles sont de longueurs très inégales, de deux à dix-sept saisons. Les changements de règlement de moindre portée restent à l'intérieur d'un cycle : les ailerons sur supports interdits en 1969, la fin des jupes en 1981, le turbo bridé de 1987-1988 ou le passage aux V8 en 2006.

## Qui domine chaque cycle

<figure class="figure">
{% include domination/cycles-cadrans-fr.svg %}
<figcaption>Un cadran par cycle : l'indice moyen de l'écurie qui y gagne le plus (aiguille), et sa meilleure saison du cycle (trait noir). Repère rouge : le seuil.</figcaption>
</figure>

Deux familles de cycles se dessinent.

- **Les cycles verrouillés.** Ferrari gagne 82 % des courses du championnat en Formule 2 (1952-1953), Mercedes 69 % de celles du groupe propulseur hybride (2014-2021), Alfa Romeo 67 % des deux premières saisons. Red Bull gagne 60 % des courses du retour de l'effet de sol (2022-2025) et la moitié de celles de la refonte aérodynamique (2009-2013).
- **Les cycles ouverts.** De 1954 à 1960, Ferrari ne gagne que 21 % des courses, et dix écuries s'imposent au moins une fois. De 1966 à 1982, Lotus en gagne autant, et dix-huit écuries gagnent. Ce sont les deux cycles les plus longs : un règlement qui dure laisse aux poursuivants le temps de rattraper le meneur.

Le cycle de la formule 3 litres montre aussi qu'un cycle peut se jouer ailleurs qu'entre les écuries. Aucune n'y domine, mais les moteurs Ford, dont le [Cosworth DFV]({{ site.baseurl }}/chronologie/#j-dfv) vendu à tous, gagnent 66 % des courses. De même, le moteur Climax gagne 53 % des courses de la formule 1,5 litre (1961-1965).

## À quelle vitesse la hiérarchie se fige

{% include domination.html quoi="cycles_dynamique" %}

- **Dans 5 cycles sur 11, l'écurie qui mène la première saison domine tout le cycle** : Alfa Romeo en 1950, Ferrari en 1952, McLaren en 1989, Mercedes en 2014 et Red Bull en 2022.
- **Ailleurs, l'écurie dominante prend la tête au bout d'une ou deux saisons**, après un premier meneur qui s'efface : Mercedes-Benz en 1954, Ferrari en 1961, Brabham en 1966, Ferrari en 1983, Brawn en 2009. Le cas extrême est le cycle 1994-2008 : Benetton, Williams et McLaren mènent tour à tour, et Ferrari ne prend la tête qu'en 2000, six saisons après le début du cycle.
- **Une fois en tête, l'écurie dominante y reste longtemps** dans les cycles récents : Mercedes mène sept saisons sur huit de 2014 à 2021, Red Bull quatre sur cinq de 2009 à 2013. Dans le cycle 1966-1982, Lotus ne mène que sept saisons sur dix-sept, en alternance avec sept autres écuries.

La colonne « Concentration » donne l'indice de Herfindahl des victoires du cycle : la somme des carrés des parts de victoires de chaque écurie, sur 100. Il vaut 100 si une seule écurie gagne tout, et d'autant moins que les victoires se dispersent. Il va de {{ CY | map: "hhi" | sort | first | times: 100 | round }}, pour le cycle 1966-1982, à {{ CY | map: "hhi" | sort | last | times: 100 | round }}, pour le championnat en Formule 2.

## Le passage d'un cycle à l'autre

Sur les dix passages d'un cycle au suivant, l'écurie qui mène la dernière saison ne garde la tête que deux fois :

- **McLaren de 1988 à 1989**, de la fin du turbo bridé au moteur atmosphérique de 3,5 litres. Elle passe de 94 % à 62 % des victoires, et reste devant.
- **Red Bull de 2021 à 2022**, du groupe propulseur hybride au retour de l'effet de sol. Elle passe de 50 % à 77 % des victoires.

Les huit autres fois, le meneur est détrôné, souvent brutalement. Ferrari passe de 78 % des victoires en 1953 à 22 % en 1954. Cooper, de 60 % en 1960 à aucune victoire en 1961. Lotus, de 60 % en 1965 à 11 % en 1966. Red Bull, de 68 % en 2013 à 16 % en 2014.

C'est le constat de la quatrième confrontation du [dossier Domination]({{ site.baseurl }}/dossiers/domination/#reglements) : un nouveau règlement rebat les cartes. À l'échelle des grands cycles, l'effet est plus net encore. Une remise à zéro coûte presque toujours sa place au meneur sortant ; la seule question est de savoir qui saura en profiter.

## Méthode et limites

- **Le découpage est un choix.** On retient les remises à zéro majeures du règlement technique ; un autre découpage, plus fin, donnerait des cycles plus courts et des résultats différents.
- **Le meneur d'une saison** est l'écurie qui gagne le plus de Grands Prix ; en cas d'égalité, celle dont l'indice composite est le plus élevé. C'est le cas en 1983, où Ferrari, Brabham et Renault gagnent quatre courses chacune.
- **Les cycles sont de longueurs inégales.** Un cycle de deux saisons ne se compare pas tout à fait à un cycle de dix-sept.
- **Les 500 miles d'Indianapolis comptent au championnat de 1950 à 1960**, et donc dans les deux premiers cycles et dans celui de la formule 2,5 litres.

## Sources

Les résultats sont ceux de formula1.com, relevés et croisés avec la base Jolpica comme l'explique le [dossier Domination]({{ site.baseurl }}/dossiers/domination/#sources). Chaque règlement qui ouvre un cycle est décrit et sourcé dans la [chronologie]({{ site.baseurl }}/chronologie/).
