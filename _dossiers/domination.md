---
title: "Domination : quand une écurie, un pilote ou un motoriste écrase la concurrence, et ce que les innovations y changent"
ordre: 6
resume: "Soixante-seize saisons de résultats officiels pour mesurer la domination des écuries, des pilotes et des motoristes, de la saison isolée à l'hégémonie, puis la confronter aux innovations, aux ingénieurs et aux règlements, sans confondre coïncidence et cause."
description: "Soixante-seize saisons de résultats officiels pour mesurer la domination des écuries, des pilotes et des motoristes, de la saison isolée à l'hégémonie, puis la confronter aux innovations, aux ingénieurs et aux règlements, sans confondre coïncidence et cause."
redirect_from: "/dossiers/hegemonies/"
---
{%- assign H = site.data.domination -%}
{%- assign P = H.parametres -%}
{%- assign EF = H.effectifs -%}
{%- assign CP = site.data.compteur -%}
{%- assign CR = site.data.croisement -%}
{%- assign TK = site.data.technologies.technologies -%}
{%- assign PNC = site.data.pneus.cas -%}
{%- assign CHC = site.data.chassis.cas -%}
{%- assign CHS = site.data.compteur.chassis -%}
{%- assign TJ = H.temoin_jalons -%}
{%- assign BI = H.bilan_ingenieurs -%}
{%- assign TR = H.temoin_reglement -%}
{%- assign EJ = H.etude_jalons -%}
{%- assign IA = H.ingenieurs_apparies -%}
{%- assign RB = H.rebat -%}
{%- assign AM = H.amont -%}
Le [classement]({{ site.baseurl }}/dossiers/methode/) des ingénieurs refuse de mesurer l'influence à l'aune du palmarès. Ce dossier pose la question inverse : **les innovations de la [chronologie]({{ site.baseurl }}/chronologie/) se voient-elles dans les résultats ?** Pour y répondre, il faut d'abord savoir quand une écurie, un pilote ou un motoriste a vraiment dominé, et à quel degré : une saison, quelques saisons, ou toute une époque. On confronte ensuite ces dominations à trois choses : les jalons techniques, les arrivées et les départs d'ingénieurs, et les changements de règlement.

Les chiffres viennent des résultats officiels de la Formule 1 : le vainqueur de chacun des {{ P.gp }} Grands Prix de championnat disputés de 1950 à 2025, et les classements finaux des pilotes et des constructeurs. Une victoire partagée entre deux pilotes (France 1951, Argentine 1956, Grande-Bretagne 1957) compte pour une seule course, créditée aux deux. Les chiffres sont recalculés par un programme, pas recopiés à la main. Les champions qu'on en tire concordent, saison par saison, avec ceux des [fiches des écuries]({{ site.baseurl }}/ecuries/).

## L'essentiel

- **Dominer est courant, durer est rare.** Chaque saison a ses champions, mais en soixante-seize saisons, l'hégémonie n'est atteinte que {{ EF.ecurie.hegemonie }} fois par une écurie, {{ EF.pilote.hegemonie }} fois par un pilote et {{ EF.motoriste.hegemonie }} fois par un motoriste.
- **Gagner n'est pas tout écraser.** Red Bull, de 2021 à 2023, gagne 74 % des Grands Prix mais ne part en pole qu'une fois sur deux ; Mercedes, de 2014 à 2021, réunit victoires, poles et doublés.
- **Une innovation rapporte, mais pas longtemps.** L'écurie qui innove passe en moyenne de {{ EJ.jalons[2] | times: 100 | round }} % à {{ EJ.jalons[4] | times: 100 | round }} % des victoires. Elle revient à son niveau de départ en quatre saisons.
- **Les innovations qui ouvrent une domination longue répondent presque toutes à un nouveau règlement** : {{ AM.ouvrants_regle }} sur {{ AM.ouvrants }}.
- **Interdire une innovation ne renverse pas l'écurie qui domine.**
- **L'arrivée d'un ingénieur du Tier A précède une hausse {{ IA[1].hausse }} fois sur {{ IA[1].n }}**, quand une écurie comparable n'en connaîtrait que {{ IA[1].hausse_attendue | replace: ".", "," }}. Un départ, lui, ne change rien.
- **Les nouveaux règlements bousculent la hiérarchie** : lors des saisons où un changement de règlement s'applique, l'écurie la plus victorieuse change dans {{ RB.avec.changements | times: 100.0 | divided_by: RB.avec.saisons | round }} % des cas, contre {{ RB.sans.changements | times: 100.0 | divided_by: RB.sans.saisons | round }} % les autres saisons. Le résultat est net, mais il dépend de la liste des règlements retenus. Ces changements ne créent pas pour autant plus souvent une domination longue.

Sommaire
{:.sommaire-titre}

* TOC
{:toc}

## Ce qu'on appelle domination

Un titre ne suffit pas : on peut le gagner de justesse. Le nombre de victoires seul ne suffit pas non plus : on peut gagner beaucoup sans être champion. On retient donc deux critères. Une saison est **dominante** pour une écurie, un pilote ou un motoriste qui remporte le titre, **ou** qui gagne au moins {{ P.seuil | times: 100 | round }} % des Grands Prix.

La domination se mesure ensuite à sa durée. Les saisons dominantes d'un même acteur, séparées au plus par une saison creuse, forment une période, qui a l'un de ces trois degrés :

1. **La saison dominante** : une seule saison, sans suite. [Tyrrell]({{ site.baseurl }}/ecuries/tyrrell/) en 1971, [Brawn]({{ site.baseurl }}/ecuries/brawn/) en 2009.
2. **La domination** : au moins {{ P.duo }} saisons dominantes. [McLaren]({{ site.baseurl }}/ecuries/mclaren/) en 1984 et 1985, par exemple.
3. **L'hégémonie** : au moins {{ P.min }} saisons dominantes, et un résultat qui résiste à toutes les variantes du seuil (voir plus bas). La Williams des années 1990 en est un exemple : battue en 1995, elle reste dominante avant et après cette saison.

Chaque saison a un champion du monde : chaque saison est donc dominante pour au moins un pilote, une écurie et un motoriste. Le premier degré est le plus courant. Ce qui est rare, c'est de durer.

Pour lire l'intensité d'une domination, chaque saison reçoit aussi une note sur 100, comme sur un compteur : l'**indice composite**, moyenne des parts de victoires, de poles et de places sur le podium ([détails plus bas](#mesures)). Le compteur ci-dessous suit, saison après saison, l'écurie la plus forte.

<figure class="figure">
{% include domination/compteur-f1-fr.svg %}
<figcaption>L'indice de l'écurie la plus forte de chaque saison (survolez un point pour la nommer). Bandes : les hégémonies d'écurie. Tirets rouges : le seuil de {{ CP.seuil | times: 100 | round }}, calculé plus bas.</figcaption>
</figure>

Le compteur ne descend jamais sous le seuil : chaque saison a une écurie nettement en tête. Il monte le plus haut avec Ferrari en 1952, sur huit courses seulement, puis avec McLaren en 1988 et Mercedes de 2014 à 2016. Il est au plus bas à la fin des années 1970 et au début des années 1980. En 1981, l'écurie la plus forte selon l'indice, Renault, doit sa place à ses poles et n'est même pas championne.

Trois précisions :

- **Avant 1958, il n'y a pas de titre des constructeurs.** L'écurie du champion du monde en tient lieu.
- **Les seuils sont arbitraires**, comme tout seuil. Le calcul est donc refait avec deux variantes plus exigeantes : au moins 50 % des victoires, puis aucune saison creuse admise. Une période d'au moins {{ P.min }} saisons dominantes retrouvée dans les deux variantes est dite **robuste**, même si ses bornes bougent un peu : c'est ce qui sépare l'hégémonie des autres dominations. (Une variante plus lâche, comme « deux saisons suffisent », retrouverait toujours tout : elle ne mettrait rien à l'épreuve.)
- **Les confrontations de la seconde partie portent sur les dominations longues** : au moins {{ P.min }} saisons dominantes, robustes ou non. Ce sont les hégémonies, plus quelques périodes fragiles, comme celle de Lotus de 1968 à 1973.

On compte à quatre niveaux :

- le **nom d'écurie** ;
- la **lignée**, c'est-à-dire la même usine sous plusieurs noms, comme [Brackley]({{ site.baseurl }}/ecuries/), de Tyrrell à Mercedes ;
- le **pilote** ;
- le **motoriste**.

## Les écuries

{% include domination.html quoi="tableau" unite="ecurie" %}

<figure class="figure">
{% include domination/tableau-ecurie-fr.svg %}
<figcaption>Le tableau de bord des dominations longues d'écurie. Aiguille : l'indice moyen de la période. Trait noir : sa meilleure saison. Repère rouge : le seuil. Arc en tirets : une domination qui n'est pas une hégémonie.</figcaption>
</figure>

En soixante-seize saisons, on compte {{ EF.ecurie.hegemonie }} hégémonies et {{ EF.ecurie.domination }} autres dominations. Quatre traits ressortent.

- **Les plus écrasantes sont les plus récentes.** [Mercedes]({{ site.baseurl }}/ecuries/mercedes/) gagne 69 % des Grands Prix pendant huit saisons, de 2014 à 2021. [Red Bull]({{ site.baseurl }}/ecuries/red-bull/), de 2021 à 2023, en gagne 74 %. La première hégémonie, celle de [Ferrari]({{ site.baseurl }}/ecuries/ferrari/) de 1975 à 1979, n'en gagne qu'environ un tiers.
- **La plus longue est celle de Ferrari, de 1999 à 2008** : huit titres en dix saisons, et une seule saison creuse, 2005.
- **Avant 1975, aucune écurie n'atteint l'hégémonie.** Les années 1950 et 1960 se jouent en dominations de deux saisons : Alfa Romeo, Ferrari, Mercedes-Benz, Cooper, Lotus, Brabham. Le titre change de mains trop souvent pour qu'une écurie s'installe.
- **Deux dominations longues ne sont pas des hégémonies.** [Lotus]({{ site.baseurl }}/ecuries/team-lotus/), de 1968 à 1973, alterne titres et saisons creuses, et ne dépasse jamais 47 % des victoires : elle ne survit pas à la variante sans saison creuse. McLaren, de 1998 à 2000, ne survit pas au seuil de 50 % : elle ne gagne que 44 % des Grands Prix en 1999 et 41 % en 2000.

On compte {{ EF.ecurie.saison }} saisons dominantes restées sans suite : {% include domination.html quoi="saisons" unite="ecurie" %}. Ce sont toutes des titres, parfois gagnés avec peu de victoires : McLaren en 1974 avec 27 % des Grands Prix, Ferrari en 1964 avec 30 %.

À l'échelle des **lignées**, le tableau est presque le même. Red Bull y devient Milton Keynes, Mercedes devient Brackley, et Enstone ne compte que deux dominations de deux saisons, sous les noms de Benetton (1994-1995) et de Renault (2005-2006). Aucune lignée n'atteint l'hégémonie en additionnant ses noms successifs. Brackley, par exemple, gagne avec Brawn en 2009 puis avec Mercedes à partir de 2014, mais les quatre saisons intermédiaires restent trop creuses.

{% include domination.html quoi="tableau" unite="lignee" %}

## Les pilotes

{% include domination.html quoi="tableau" unite="pilote" %}

<figure class="figure">
{% include domination/tableau-pilote-fr.svg %}
<figcaption>Le tableau de bord des dominations longues de pilote, avec la même lecture. Aucun pilote ne dépasse 50 de moyenne : il partage toujours le podium avec son coéquipier.</figcaption>
</figure>

Les hégémonies de pilotes se calquent sur celles de leur écurie : Schumacher sur Ferrari, Vettel et Verstappen sur Red Bull, Hamilton sur Mercedes. Seul **Fangio**, de 1954 à 1957, atteint l'hégémonie avec trois écuries : Mercedes-Benz, Ferrari et Maserati.

Trois dominations longues de pilotes ne sont pas des hégémonies :

- **Stewart**, de 1969 à 1973, domine avec Matra puis Tyrrell. Sa saison avec March, en 1970, est l'une de ses saisons creuses.
- **Prost** et **Senna** se partagent la même McLaren : leurs dominations se recouvrent, et aucune ne résiste aux variantes du seuil.

C'est chez les pilotes que la saison isolée est la plus fréquente : {{ EF.pilote.saison }} cas, {% include domination.html quoi="saisons" unite="pilote" %}. Un pilote peut être champion avec peu de victoires : Rosberg, en 1982, n'en remporte qu'une.

## Les motoristes

{% include domination.html quoi="tableau" unite="motoriste" %}

<figure class="figure">
{% include domination/tableau-motoriste-fr.svg %}
<figcaption>Le tableau de bord des dominations longues de motoriste, avec la même lecture.</figcaption>
</figure>

C'est à ce niveau que se trouve la plus longue domination : celle des moteurs **Ford**, dont le [Cosworth DFV]({{ site.baseurl }}/chronologie/#j-dfv). Ils dominent chacune des quinze saisons de 1968 à 1982 et gagnent 70 % des Grands Prix, pour Lotus, McLaren, Tyrrell et d'autres.

Le DFV est vendu à tous. Aucune hégémonie d'écurie ne lui correspond donc : on observe plutôt une succession d'écuries championnes avec le même moteur. Climax avant lui, Honda et Renault ensuite, dominent de la même façon à travers plusieurs écuries.

La domination du moteur Mercedes, de 2012 à 2021, commence avant celle de l'écurie Mercedes : il gagne d'abord avec McLaren, puis avec Mercedes et Racing Point. Avant elle, le moteur Mercedes avait déjà connu deux dominations longues sans atteindre l'hégémonie : de 1998 à 2000 avec McLaren, puis de 2005 à 2009 avec McLaren et enfin Brawn.

Le groupe propulseur de Red Bull, de 2021 à 2023, est compté sous le nom de **Honda**. Les résultats officiels l'appellent Honda en 2021, puis RBPT et Honda RBPT, mais c'est Honda qui le construit pendant toute cette période. C'est un choix de lecture : en séparant les trois noms, cette hégémonie disparaît.

Saisons dominantes isolées : {% include domination.html quoi="saisons" unite="motoriste" %}.

## Les ingénieurs

Un ingénieur ne gagne pas de course, mais on peut mesurer la domination de son écurie pendant qu'il y travaille. On suit chaque séjour daté des [fiches des écuries]({{ site.baseurl }}/ecuries/), saison par saison, avec les mêmes règles que pour une écurie : saisons dominantes, degrés et indice. Une suite de saisons dominantes peut passer d'une écurie à l'autre avec l'ingénieur. {{ CP.ingenieurs.non_dates }} séjours sans date de début ou de fin restent hors du compte.

<figure class="figure">
{% include domination/ingenieurs-compteur-fr.svg %}
<figcaption>Le compteur des douze ingénieurs dont l'écurie a dominé le plus de saisons. Aiguille : l'indice moyen de leurs écuries pendant leur présence. Trait noir : leur meilleure saison.</figcaption>
</figure>

**Adrian Newey** est en tête : seize saisons dominantes en trente-six saisons datées, chez Williams, McLaren et Red Bull. Sa plus longue suite, de 1991 à 2000, passe de Williams à McLaren. Paddy Lowe et Ross Brawn suivent, avec treize et douze saisons dominantes. Colin Chapman, lui, ne dépasse pas le degré de la domination : comme Lotus de 1968 à 1973, sa suite ne résiste pas à la variante sans saison creuse.

{% include domination.html quoi="ingenieurs_dom" %}

Ce compteur mesure une présence, pas une contribution : un ingénieur peut être là quand l'écurie gagne sans en être la cause. La troisième confrontation, plus bas, tente d'aller plus loin avec un témoin.

## Les voitures

Une écurie gagne avec une voiture précise, et elle en change parfois en cours de saison. On a relevé le modèle gagnant de chacun des {{ P.gp }} Grands Prix, course par course ({{ CHC.size }} écurie-saisons, chacune sourcée) : {{ CHS.modeles }} modèles différents ont gagné au moins une fois.

<figure class="figure">
{% include domination/chassis-fr.svg %}
<figcaption>Les douze voitures les plus écrasantes : chaque cadran donne la part des Grands Prix de la saison gagnés par ce modèle.</figcaption>
</figure>

{% include domination.html quoi="chassis" %}

- **La voiture la plus écrasante est récente** : la Red Bull RB19 gagne 21 des 22 Grands Prix de 2023, devant la McLaren MP4/4 (15 sur 16 en 1988) et la Mercedes W07 de 2016. Huit des douze cadrans datent de 2002 ou après.
- **Autrefois, une bonne voiture durait.** La Lotus 72 gagne de 1970 à 1974, en quatre évolutions ; la McLaren M23, de 1973 à 1976 ; la Lotus 25 et la Lotus 49 sur quatre saisons aussi. Après la McLaren MP4/2 (1984-1986), plus aucun modèle ne gagne sur trois saisons : chaque écurie construit désormais une nouvelle voiture chaque année.
- **Une voiture qui dure n'est pas forcément dominante** : la Lotus 72 et la M23 gagnent beaucoup, mais jamais plus de la moitié des courses d'une saison.

Les noms d'équipe de formula1.com sont presque toujours justes. La recherche a trouvé une exception : en 1957 et 1958, les voitures gagnantes des 500 miles d'Indianapolis, classées « Epperly Offenhauser », sont des Salih-Offenhauser.

## Les pneus

Le manufacturier de pneus est un acteur à part : il équipe plusieurs écuries, comme un motoriste. On a relevé celui de chaque écurie qui a gagné un Grand Prix ou signé une pole, saison par saison ({{ PNC.size }} écurie-saisons, chacune sourcée). Une saison est dominante pour le manufacturier qui équipe l'écurie championne, ou qui gagne au moins {{ P.seuil | times: 100 | round }} % des courses. Les saisons de fournisseur unique sont hors concours : Goodyear seul de fait en 1987-1988 et de 1992 à 1996, puis Bridgestone en 1999-2000 et de 2007 à 2010, Pirelli depuis 2011.

<figure class="figure">
{% include domination/pneus-fr.svg %}
<figcaption>Part des Grands Prix gagnés sur chaque marque de pneus, saison par saison (survolez une barre pour le détail). « Autres » réunit Englebert, Continental et Avon. Hachures : les saisons de fournisseur unique.</figcaption>
</figure>

{% include domination.html quoi="pneus" %}

- **Dunlop, de 1958 à 1965, signe la domination la plus complète** : huit titres en huit saisons, 92 % des victoires. Elle accompagne la révolution du moteur arrière, de Cooper à Lotus.
- **Goodyear domine le plus longtemps**, de 1971 à 1986, avec douze titres, avant de rester seul en piste.
- **Les guerres de pneus désignent le plus souvent un camp gagnant**, plutôt qu'un équilibre : Michelin de 1979 à 1984, face à Goodyear, puis Bridgestone de 2001 à 2006, face à Michelin, avec les titres de Ferrari. Seule la lutte entre Firestone et Goodyear, de 1966 à 1972, reste partagée, en dominations courtes.
- **Depuis 2007, le pneu ne départage plus personne** : le fournisseur unique est devenu la règle.

Les vainqueurs et les polemen sont ceux de formula1.com. Pour la pole d'Argentine 1955, formula1.com indique Lancia, mais la recherche sur les pneus a montré que González l'a signée sur une Ferrari 625 chaussée d'Englebert : le manufacturier retenu est Englebert, et l'écart est signalé ici.

## Au-delà des victoires : poles, podiums et doublés {#mesures}

Les degrés reposent sur les titres et les victoires. Trois autres mesures décrivent la manière de dominer. Elles sont relevées course par course sur formula1.com :

- la **part des poles** : la première place de la grille de départ publiée, après d'éventuelles pénalités ;
- la **part des places sur le podium** : sur les trois places de chaque course ;
- la **part des doublés** : les deux premières places pour la même écurie ou le même motoriste. Pour un pilote, cette mesure n'a pas de sens : les tableaux donnent alors sa part des places sur le podium.

Ces mesures décrivent une domination, elles ne la définissent pas : une écurie ne change pas de degré selon ses poles. Elles figurent dans les tableaux ci-dessus, avec l'**indice composite** : la moyenne simple des parts de victoires, de poles et de places sur le podium, sur 100. Un indice de 100 voudrait dire tout gagner, partir en pole à chaque course et occuper tout le podium.

Elles nuancent le palmarès :

- **Mercedes, de 2014 à 2021, réunit tout** : 69 % des victoires, 74 % des poles et un doublé une course sur trois.
- **Red Bull, de 2021 à 2023, gagne plus (74 %), mais part en pole moins d'une fois sur deux, et ne signe un doublé qu'une course sur six.** Sa domination repose surtout sur un pilote et sur le rythme de course.
- **McLaren, de 1988 à 1991, part en pole 81 % du temps** : c'est la plus forte proportion parmi les hégémonies.
- **Ferrari, de 1975 à 1979, domine avec peu** : 35 % des victoires, 24 % des poles, 6 % de doublés. Elle doit son hégémonie à la régularité des titres plus qu'à l'écrasement.

### Les saisons les plus écrasantes

L'indice composite permet aussi de comparer les saisons entre elles, indépendamment des degrés.

{% include domination.html quoi="ecrasantes" unite="ecurie" %}

Les années 1950 figurent en bonne place, mais avec peu de courses : Ferrari gagne en 1952 sept des huit Grands Prix, dont les 500 miles d'Indianapolis où elle ne s'impose pas. Depuis, seules McLaren en 1988 et Mercedes en 2014-2016 approchent ce niveau sur une saison complète. Chez les pilotes, aucune saison n'atteint 60 : un pilote partage toujours le podium avec son coéquipier.

{% include domination.html quoi="ecrasantes" unite="pilote" %}

## Par cycle réglementaire

La domination se lit aussi à l'échelle des grands cycles réglementaires, ces remises à zéro du règlement technique qui reviennent tous les cinq à quinze ans. Le [dossier sur les cycles réglementaires]({{ site.baseurl }}/dossiers/cycles/) les examine un par un : qui domine chaque cycle, à quelle vitesse la hiérarchie se fige, et si le meneur d'un cycle survit au suivant.

<figure class="figure">
{% include domination/cycles-cadrans-fr.svg %}
<figcaption>Un cadran par cycle réglementaire : l'indice moyen de l'écurie qui y gagne le plus (aiguille), et sa meilleure saison du cycle (trait noir).</figcaption>
</figure>

L'écurie qui mène la dernière saison d'un cycle ne garde la tête au début du suivant que deux fois sur dix : McLaren en 1989 et Red Bull en 2022.

## Domination technique

Une écurie peut dominer, mais une technologie aussi. On suit neuf innovations de la [chronologie]({{ site.baseurl }}/chronologie/), du moteur arrière à la récupération d'énergie. Pour chaque Grand Prix, on note si la voiture gagnante l'utilise ; la part des victoires mesure alors la domination de la technologie, saison par saison. Hors des fenêtres de transition, tous les gagnants l'ont, ou aucun : le moteur arrière après 1961, l'effet de sol interdit de 1983 à 2021. Pendant ces fenêtres, chaque écurie gagnante est classée une à une, sources à l'appui ({{ TK.size }} technologies, {% assign n_tk = 0 %}{% for t in TK %}{% assign n_tk = n_tk | plus: t.cas.size %}{% endfor %}{{ n_tk }} classements).

<figure class="figure">
{% include domination/technologies-fr.svg %}
<figcaption>La diffusion des neuf technologies : part des Grands Prix gagnés par des voitures qui l'utilisent. Trait vertical : le jalon. Fond bleu : les saisons où le pionnier est seul à gagner avec elle.</figcaption>
</figure>

{% include domination.html quoi="technologies" %}

Quatre constats :

- **Le pionnier n'est jamais seul longtemps.** Au plus deux saisons, et souvent moins : les ailerons sont copiés dans la saison même, en 1968.
- **Une technologie gagnante conquiert la moitié des victoires en trois ans au plus**, sauf la suspension active, et presque toutes en un peu plus de trois ans en moyenne. Les ailerons vont le plus vite (un an), puis l'effet de sol et la récupération d'énergie (deux ans).
- **Les plus lentes sont les plus complexes** : six ans pour la suspension active, de la Lotus de 1987 à la Williams de 1993, et cinq pour le turbo, de la Renault de 1979 aux gagnants de 1984. Elles demandent un motoriste ou une électronique qu'on ne copie pas d'une course à l'autre.
- **Innover ne garantit pas de dominer.** Cooper, puis Lotus avec la monocoque et les ailerons, enchaînent des saisons dominantes juste après leur innovation. Mais Renault n'est jamais championne avec le turbo, Ferrari ne l'est pas avec la boîte semi-automatique, et McLaren ne domine qu'en 1984, trois ans après sa monocoque carbone, avec la MP4/2 et le moteur TAG-Porsche. Lotus tire de l'effet de sol un titre, en 1978, sans domination durable.

Deux conventions de classement sont des choix : une semi-monocoque (treillis habillé de panneaux d'aluminium travaillants, chez Ferrari et BRM) compte comme une monocoque ; les ailerons comprennent les ailettes de nez. Les autres cas discutables sont détaillés dans les données du site, chacun avec sa source.

## Le compteur de domination

Chaque [fiche d'écurie]({{ site.baseurl }}/ecuries/) porte un compteur. Un cadran donne la meilleure saison de la lignée ; en dessous, une courbe suit l'indice composite saison par saison, l'usine sous tous ses noms. Les titres, les périodes de domination, les jalons de la chronologie et un seuil y figurent.

Ce seuil n'est pas choisi à la main. C'est la valeur d'indice qui sépare le mieux les saisons dominantes (titre ou au moins {{ P.seuil | times: 100 | round }} % des victoires) des autres, au sens de l'*indice de Youden*, qui additionne la part des saisons dominantes au-dessus du seuil et la part des autres en dessous. Il vaut **{{ CP.seuil | times: 100 | round }}**. Sur {{ CP.saisons }} saisons de lignée mesurées, les {{ CP.dominantes }} saisons dominantes le dépassent toutes ({{ CP.dominantes_au_dessus }}). {{ CP.au_dessus | minus: CP.dominantes_au_dessus }} autres le dépassent aussi : ce sont le plus souvent des écuries deuxièmes du championnat des constructeurs, battues pour le titre.

## Innovations et résultats : quatre confrontations


Les dominations disent qui a gagné. Reste à savoir ce que les innovations y changent. On pose ici quatre questions aux données :

1. Que rapporte une innovation à l'écurie qui la porte, et pendant combien de temps ?
2. Les chaînes de causes que trace la chronologie, du règlement à l'innovation, mènent-elles aux victoires ?
3. Une écurie gagne-t-elle davantage après l'arrivée d'un ingénieur ?
4. Un changement de règlement rebat-il les cartes ?

Les réponses sont résumées [en tête de page](#lessentiel).

### Méthode

Toutes les mesures portent sur la **part des Grands Prix gagnés** par l'écurie. Une **domination longue** compte au moins {{ P.min }} saisons dominantes, hégémonie ou non : chez les écuries, ce sont les {{ EF.ecurie.hegemonie }} hégémonies, plus Lotus de 1968 à 1973 et McLaren de 1998 à 2000. On compare deux fenêtres :

- **avant** : les deux saisons qui précèdent l'événement ;
- **après** : les trois saisons qui commencent avec lui.

Chaque écart est comparé à un **témoin**. Le témoin, c'est le même calcul fait pour la même écurie à n'importe quelle autre saison, une saison où il ne s'est rien passé de particulier.

Pour les ingénieurs, le témoin est **apparié sur le niveau de départ**. Une écurie qui ne gagnait rien ne peut que monter, et une écurie qui gagnait tout ne peut que baisser : c'est la *régression vers la moyenne*. Sans cette précaution, on prendrait ce mouvement naturel pour l'effet d'un ingénieur.

Quand les cas sont peu nombreux, on calcule la **probabilité d'obtenir un résultat au moins aussi net par le seul hasard**. En dessous de 5 %, l'écart est difficile à attribuer à la chance. Au-dessus, c'est un indice, pas une démonstration.

Enfin, le vocabulaire est celui du [dossier sur la causalité]({{ site.baseurl }}/dossiers/causalite/). Un écart mesuré reste un recoupement **chronologique**. Seuls les liens que la chronologie établit déjà par une source vont au-delà.

### 1. Ce que rapporte une innovation, et combien de temps

On prend les {{ EJ.n }} jalons rattachés à l'écurie qui les a portés. Pour chacun, on suit la part de victoires de l'écurie, de trois saisons avant le jalon à cinq saisons après.

<figure class="figure">
{% include domination/etude-jalons-fr.svg %}
<figcaption>Part moyenne des Grands Prix gagnés par l'écurie, saison par saison autour du jalon (trait plein), et par la même écurie à une saison quelconque (tirets). Les valeurs de chaque jalon sont dans le tableau détaillé plus bas.</figcaption>
</figure>

Trois saisons avant le jalon, rien ne distingue l'écurie de son niveau habituel.

- **L'année du jalon, la part de victoires de l'écurie bondit**, puis culmine la saison suivante.
- **L'écart moyen entre les deux fenêtres est de +{{ EJ.gain | times: 100 | round }} points**, contre {{ EJ.gain_temoin | times: 100 | round | replace: "-", "−" }} pour le témoin.
- **La hausse concerne environ la moitié des cas** : {{ EJ.hausses }} jalons sur {{ EJ.n }} sont suivis d'une progression de plus de 5 points. Deux jalons de la même écurie la même année (Benetton en 1993, McLaren en 2009) ne comptent qu'une fois.
- **L'avance s'efface ensuite** : quatre saisons après le jalon, l'écurie est revenue à son niveau. Une innovation donne une avance de deux à trois saisons. Les données ne disent pas pourquoi elle s'efface : copie par les rivaux, interdiction par le règlement (partie 2) ou simple usure.

**Toutes les voies techniques ne rapportent pas autant.** Les jalons d'**architecture** (le moteur arrière des Cooper, la monocoque de la Lotus 25, le carbone de la MP4/1, la MP4/4) sont les plus payants : cinq sur six sont suivis d'une hausse. L'**aérodynamique** fournit le plus de jalons, mais chacun d'eux rapporte moins, peut-être parce que ses idées se copient plus vite. Les effectifs sont trop faibles pour aller plus loin.

{% include domination.html quoi="voies" %}

**Une innovation suffit rarement à fonder une domination longue.** Sur {{ TJ.n }} jalons portés par une écurie qui ne dominait pas encore, **{{ TJ.ouvre }} précèdent de peu une domination longue** :

- le [DFV]({{ site.baseurl }}/chronologie/#j-dfv) chez Lotus en 1967 ;
- la [312T]({{ site.baseurl }}/chronologie/#j-ferrari-312t) chez Ferrari en 1975 ;
- la [MP4/4]({{ site.baseurl }}/chronologie/#j-mp4-4) chez McLaren en 1988 ;
- la [RB6]({{ site.baseurl }}/chronologie/#j-rb6) chez Red Bull en 2010 ;
- le [groupe propulseur hybride]({{ site.baseurl }}/chronologie/#j-hybride) chez Mercedes en 2014.

Le témoin en attend {{ TJ.attendu | replace: ".", "," }}. Le hasard seul en produirait au moins autant avec une probabilité de {{ H.p_hasard | times: 100 | round }} %. C'est un indice, pas une preuve.

Les contre-exemples sont instructifs :

- **L'innovation sans lendemain.** La [Lotus 78]({{ site.baseurl }}/chronologie/#j-lotus-78) fait passer Lotus de 3 % à 27 % des victoires, sans qu'une domination longue s'ensuive. La [Benetton de 1993]({{ site.baseurl }}/chronologie/#j-cfd-benetton) fait passer son écurie de 6 % à 40 %, mais pour deux saisons de domination seulement. Le [double diffuseur]({{ site.baseurl }}/chronologie/#j-double-diffuseur) vaut à Brawn un titre, puis l'écurie change de nom. La [MP4/1]({{ site.baseurl }}/chronologie/#j-mp4-1) en carbone ne rapporte à McLaren que 13 % des victoires de 1981 à 1983 : les titres de 1984 et 1985 viennent avec la [MP4/2]({{ site.baseurl }}/chronologie/#j-mp4-2) et son moteur TAG-Porsche.
- **L'innovation qui prolonge.** La [Lotus 72]({{ site.baseurl }}/chronologie/#j-lotus-72), la [FW14B]({{ site.baseurl }}/chronologie/#j-fw14b) et la [RB18]({{ site.baseurl }}/chronologie/#j-rb18) arrivent quand leur écurie domine déjà.
- **La domination sans jalon.** Aucun jalon n'accompagne Ferrari en 1999-2008, ni McLaren en 1998-2000. Les jalons retenus ne les expliquent pas.

<details>
<summary>Les {{ EJ.n }} jalons un par un</summary>
{% include domination.html quoi="jalons" %}
</details>

### 2. Du règlement aux victoires : les chaînes sourcées

La chronologie relie des événements de contexte (règlements, économie, techniques venues d'ailleurs) aux jalons qu'ils ont rendus possibles ou interdits. Chaque lien porte son mécanisme et son niveau de preuve. On peut donc suivre une chaîne complète : un règlement, l'innovation qu'il provoque, puis les victoires qui suivent.

**Les innovations qui fondent une domination longue répondent presque toutes à un nouveau règlement.** Sur les {{ AM.ouvrants }} jalons qui précèdent une domination longue, {{ AM.ouvrants_regle }} sont reliés par la chronologie à un changement de règlement :

- le DFV à la [formule 3 litres]({{ site.baseurl }}/chronologie/#c-formule-3-litres) (lien établi) ;
- la MP4/4 au [turbo bridé et à la dotation de 150 litres]({{ site.baseurl }}/chronologie/#c-turbo-bride) (attesté) ;
- la RB6 à la [refonte aérodynamique de 2009]({{ site.baseurl }}/chronologie/#c-refonte-aero-2009) (discuté) ;
- le moteur hybride au [groupe propulseur obligatoire]({{ site.baseurl }}/chronologie/#c-groupe-propulseur-2014) de 2014 (établi).

Sur l'ensemble des jalons, la proportion n'est que de {{ AM.avec_regle }} sur {{ AM.jalons }}.

Un nouveau règlement remet tout le monde à zéro. Celui qui y répond le mieux part avec une avance que les autres ne peuvent combler qu'au fil de plusieurs saisons. Mais sur {{ AM.ouvrants }} cas seulement, le hasard produirait un tel écart avec une probabilité de {{ AM.p | times: 100 | round }} % : c'est une tendance, pas une loi.

<details>
<summary>Les chaînes qui ouvrent ou transfèrent une innovation</summary>
{% include domination.html quoi="chaines" ferme="non" %}
</details>

**Interdire une innovation ne renverse pas l'écurie qui domine.** Quand le règlement ferme la porte à une innovation, l'effet sur l'écurie qui la portait varie : elle recule parfois, mais progresse tout aussi souvent. Deux fois, l'interdiction frappe une écurie au sommet, et celle-ci y reste :

- **Williams en 1994**, avec la [fin des aides électroniques]({{ site.baseurl }}/chronologie/#c-fin-aides-electroniques) : elle passe de 62 % à 49 % des victoires, mais son hégémonie dure jusqu'en 1997.
- **Red Bull en 2012**, avec l'[encadrement des échappements]({{ site.baseurl }}/chronologie/#c-echappements-2012) : elle passe de 55 % à 40 %, mais domine encore jusqu'en 2013.

Ce qui fait durer une domination ne tient donc pas à une seule pièce de la voiture.

{% include domination.html quoi="chaines" ferme="oui" %}

### 3. Les ingénieurs

Pour chaque arrivée, on compare la part de victoires de l'écurie dans les deux saisons qui précèdent et dans les trois qui commencent avec l'ingénieur. Pour chaque départ, on compare les deux dernières saisons avec lui et les trois suivantes. Une hausse ou une baisse de plus de 5 points est comptée comme telle. Les arrivées trop récentes pour avoir trois saisons de recul sont écartées.

<figure class="figure">
{% include domination/ingenieurs-fr.svg %}
<figcaption>Part des cas suivis d'une hausse de plus de 5 points (point plein), et part attendue d'après le témoin apparié sur le niveau de départ (cercle). Entre parenthèses, le nombre de cas.</figcaption>
</figure>

**Après une arrivée, l'écurie progresse nettement plus souvent que prévu** : {{ IA[0].hausse }} cas sur {{ IA[0].n }}, alors que le témoin apparié en attend {{ IA[0].hausse_attendue | replace: ".", "," }}. Le hasard seul produirait un tel écart avec une probabilité inférieure à 0,1 %.

**L'écart est le plus fort pour le Tier A** : {{ IA[1].hausse }} hausses sur {{ IA[1].n }} arrivées, pour {{ IA[1].hausse_attendue | replace: ".", "," }} attendues, et un gain moyen de +{{ IA[1].gain | times: 100 | round }} points ; le hasard seul produirait un tel écart avec une probabilité de {{ IA[1].p | times: 100 | round }} %. Ces arrivées sont celles d'[Adrian Newey]({{ site.baseurl }}/ingenieurs/adrian-newey/) et de [John Barnard]({{ site.baseurl }}/ingenieurs/john-barnard/). Les hausses suivent Newey chez Williams (1990) et chez McLaren (1997), Barnard chez McLaren (1972 et 1980) et chez Ferrari (1987). Les autres n'en sont pas suivies : Newey chez Fittipaldi (1980), March (1988) et Red Bull (2006), où la première victoire attend 2009, et Barnard à son retour chez Ferrari (1992). Neuf cas, c'est peu : l'écart est net, mais il repose sur deux hommes.

Pour les Tiers B à D, l'écart est moindre : le hasard seul le produirait avec une probabilité de {{ IA[2].p | times: 100 | round }} %. Pour les ingénieurs hors classement, l'écart est plus faible, mais il reste net sur {{ IA[3].n }} cas.

**Un départ, lui, ne change rien** : {{ IA[4].hausse }} hausses pour {{ IA[4].hausse_attendue | replace: ".", "," }} attendues. Une écurie garde son élan quelques saisons après le départ d'un ingénieur.

Cela ne prouve pas que l'ingénieur fasse gagner l'écurie. Le témoin neutralise le niveau de départ, pas la trajectoire ni le budget. Un grand ingénieur choisit aussi une écurie qui monte, et une écurie qui monte a les moyens de le recruter. Mais le classement n'a pas été établi d'après les résultats, et ce sont pourtant les ingénieurs du Tier A dont l'arrivée précède le plus nettement une hausse. Les deux mesures, l'une technique, l'autre sportive, vont dans le même sens.

**Qui était là quand chaque domination longue a commencé ?** Un ingénieur est compté s'il est arrivé avant le début de la domination et n'est pas parti plus de trois saisons avant ce début. Quand sa date de départ n'est pas connue et qu'il est arrivé plus de trois saisons avant, sa présence est dite incertaine.

{% include domination.html quoi="racines" %}

[Adrian Newey]({{ site.baseurl }}/ingenieurs/adrian-newey/) est présent au début de quatre des {{ EF.ecurie.longue }} dominations longues d'écurie : Williams 1991, McLaren 1998, Red Bull 2010 et Red Bull 2021. Deux ingénieurs le sont au début de trois :

- [Paddy Lowe]({{ site.baseurl }}/ingenieurs/paddy-lowe/) : Williams 1991, McLaren 1998 et Mercedes 2014 ;
- [Geoff Willis]({{ site.baseurl }}/ingenieurs/geoff-willis/) : Williams 1991, Red Bull 2010 et Mercedes 2014. Pour Red Bull, la règle des trois saisons le compte, mais il a quitté l'écurie en 2009, avant la saison 2010.

[Ross Brawn]({{ site.baseurl }}/ingenieurs/ross-brawn/) et [John Barnard]({{ site.baseurl }}/ingenieurs/john-barnard/) le sont au début de deux : Ferrari 1999 et Mercedes 2014 pour Brawn, McLaren 1988 et Ferrari 1999 pour Barnard, chaque fois parti peu avant.

<details>
<summary>Le bilan et les mouvements un par un</summary>
{% include domination.html quoi="ingenieurs" %}
</details>

### 4. Les règlements : rebattre les cartes sans créer de dynastie {#reglements}

D'une saison à l'autre, l'écurie qui gagne le plus de Grands Prix change souvent. Elle change **{{ RB.avec.changements }} fois sur {{ RB.avec.saisons }}** lors des saisons où un changement de règlement de la chronologie s'applique, contre **{{ RB.sans.changements }} fois sur {{ RB.sans.saisons }}** les autres saisons. Le hasard seul produirait un tel écart avec une probabilité de {{ RB.p | times: 100 | round }} %, sous le seuil habituel de 5 %. **Un nouveau règlement bouscule donc bien la hiérarchie.** Ce résultat reste fragile : il dépend de la liste des règlements retenus. Avant l'ajout à la chronologie du championnat couru en Formule 2 (1952) et de la formule 1,5 litre (1961), à l'occasion du [dossier sur les cycles réglementaires]({{ site.baseurl }}/dossiers/cycles/), la probabilité était de 8 %.

Il ne crée pas pour autant plus souvent une dynastie. {{ TR.debuts_regle }} débuts de domination longue sur {{ TR.debuts }}, et {{ TR.fins_regle }} fins sur {{ TR.fins }}, coïncident avec un changement de règlement. Ici, « coïncider » veut dire que le règlement s'applique la saison même ou la précédente ; avec cette fenêtre, {{ TR.avec_regle }} saisons sur {{ TR.annees }} sont dans ce cas : la proportion est à peu près la même.

Le règlement redistribue les cartes. Encore faut-il que quelqu'un sache jouer la nouvelle main, et c'est là que les parties 1 à 3 se rejoignent. Les coïncidences les plus nettes :

- le [groupe propulseur hybride obligatoire]({{ site.baseurl }}/chronologie/#c-groupe-propulseur-2014) de 2014 précède de peu les hégémonies de Mercedes et de Hamilton ;
- la [refonte aérodynamique de 2009]({{ site.baseurl }}/chronologie/#c-refonte-aero-2009) précède celle de Red Bull ;
- le [retour de l'effet de sol]({{ site.baseurl }}/chronologie/#c-retour-effet-de-sol), en 2022, suit de peu la fin de celle de Mercedes ;
- la [formule 3 litres]({{ site.baseurl }}/chronologie/#c-formule-3-litres), en 1966, suit de peu la fin de celle du Climax ;
- le [fond plat]({{ site.baseurl }}/chronologie/#c-fond-plat), en 1983, suit de peu la fin de celle du Ford.

### Ce qu'il faut retenir

Une domination durable se fait rarement sur une seule idée. Les données dessinent plutôt une séquence :

1. un **nouveau règlement** remet la hiérarchie à zéro ;
2. une écurie y répond par une **innovation** qui lui donne deux à trois saisons d'avance ;
3. elle garde cette avance si elle a su attirer, ou garder, les **ingénieurs** capables de renouveler l'idée avant qu'on la copie ;
4. l'**interdiction** de l'innovation ne suffit pas à mettre fin à sa domination : il faut attendre le règlement suivant.

Mercedes en 2014 et Red Bull en 2010 suivent ce schéma presque pas à pas. Ferrari en 1999-2008 y échappe, faute de jalon dans la chronologie.

## Limites

- **La victoire n'est pas la seule mesure.** Elle ignore les écuries qui progressent sans gagner, et elle reflète aussi le talent du pilote, la fiabilité et les budgets.
- **Les jalons sont une sélection.** La chronologie retient les innovations qui ont changé la conception des voitures, pas celles qui ont fait gagner. Une domination sans jalon peut cacher une innovation non retenue.
- **Le rattachement d'un jalon à une écurie suit les fiches des écuries.** Quatre jalons n'y sont rattachés à aucune écurie, et ne sont donc pas comptés : le [prototype Cooper 500]({{ site.baseurl }}/chronologie/#j-cooper-500), le [FVA]({{ site.baseurl }}/chronologie/#j-dfv-fva), le [rappel pneumatique des soupapes]({{ site.baseurl }}/chronologie/#j-rappel-pneumatique) et le [V10 Renault]({{ site.baseurl }}/chronologie/#j-v10-renault).
- **Les dates des ingénieurs sont parfois incomplètes.** Celles des ingénieurs cités dans ce dossier ont été vérifiées sur leurs fiches ; d'autres restent approximatives. Une date de départ manquante rend une présence incertaine, et le tableau le signale.
- **Les 500 miles d'Indianapolis (1950-1960) comptent au championnat.** Ils figurent donc ici, gagnés par des constructeurs américains : [Kurtis Kraft]({{ site.baseurl }}/ecuries/kurtis-kraft/) a une fiche, Kuzma, Watson et Epperly n'en ont pas.
- **Les seuils restent des choix.** La colonne « Degré » dit quelles dominations longues y résistent : ce sont les hégémonies.

## Sources

Résultats consultés le 29 octobre 2026 sur formula1.com, pour chaque saison de 1950 à 2025 :

- les vainqueurs des Grands Prix : `https://www.formula1.com/en/results/<année>/races` ;
- le classement des constructeurs, depuis 1958 : `…/<année>/team` ;
- le classement des pilotes : `…/<année>/drivers` ;
- pour chaque course, le podium et la grille de départ : `…/<année>/races/<course>/race-result` et `…/starting-grid`.

Le lien de chaque course est conservé dans les données du site.

Ces résultats ont été comparés course par course à une seconde source, la base ouverte [Jolpica]({{ CR.source }}) (successeur d'Ergast). Les vainqueurs concordent pour {{ CR.bilan.vainqueur.concordants }} courses sur {{ P.gp }}, les poles pour {{ CR.bilan.pole.concordants }}, les deuxièmes pour {{ CR.bilan.deuxieme.concordants }} et les troisièmes pour {{ CR.bilan.troisieme.concordants }}. Le seul désaccord porte sur le Grand Prix du Brésil 1983 : formula1.com laisse vacante la deuxième place de Keke Rosberg, disqualifié, et classe Niki Lauda troisième ; Jolpica fait remonter chacun d'un rang et classe Jacques Laffite troisième. Ce dossier suit formula1.com. Les ingénieurs, les jalons et les règlements viennent des [fiches des écuries]({{ site.baseurl }}/ecuries/) et de la [chronologie]({{ site.baseurl }}/chronologie/), où chacun a ses propres sources.
