---
title: "Hégémonies : quand une écurie domine, et ce que les innovations y changent"
ordre: 6
resume: "Soixante-seize saisons de résultats officiels pour repérer les périodes de domination des écuries, des pilotes et des motoristes, puis les confronter aux innovations, aux ingénieurs et aux règlements, sans confondre coïncidence et cause."
description: "Soixante-seize saisons de résultats officiels pour repérer les périodes de domination des écuries, des pilotes et des motoristes, puis les confronter aux innovations, aux ingénieurs et aux règlements, sans confondre coïncidence et cause."
---
{%- assign H = site.data.hegemonies -%}
{%- assign P = H.parametres -%}
{%- assign TJ = H.temoin_jalons -%}
{%- assign BI = H.bilan_ingenieurs -%}
{%- assign TR = H.temoin_reglement -%}
Le [classement]({{ site.baseurl }}/dossiers/methode/) des ingénieurs refuse de mesurer l'influence au palmarès. Ce dossier pose la question inverse : **les innovations de la [chronologie]({{ site.baseurl }}/chronologie/) se voient-elles dans les résultats ?** Pour y répondre, il faut d'abord savoir quand une écurie, un pilote ou un motoriste a vraiment dominé. On confronte ensuite ces périodes à trois choses : les jalons techniques, les arrivées et les départs d'ingénieurs, et les changements de règlement.

Les chiffres viennent des résultats officiels de la Formule 1 : le vainqueur de chacun des {{ P.gp }} Grands Prix de championnat disputés de 1950 à 2025, et les classements finaux des pilotes et des constructeurs. Ils sont recalculés par un programme, pas recopiés à la main. Les champions qu'on en tire concordent, saison par saison, avec ceux des [fiches des écuries]({{ site.baseurl }}/ecuries/).

## Ce qu'on appelle une hégémonie

Un titre ne suffit pas : on peut le gagner de justesse. Le nombre de victoires seul ne suffit pas non plus : on peut gagner beaucoup sans être champion. On retient donc deux critères. Une saison est **dominante** pour une écurie, un pilote ou un motoriste s'il y est champion, **ou** s'il gagne au moins {{ P.seuil | times: 100 | round }} % des Grands Prix.

Une **hégémonie** compte au moins {{ P.min }} saisons dominantes, séparées au plus par {{ P.creux }} saison creuse. La Williams des années 1990 en est un exemple : battue en 1995, elle reste dominante avant et après cette saison.

Deux précisions :

- **Avant 1958, il n'y a pas de titre des constructeurs.** L'écurie du champion du monde en tient lieu.
- **Seuils arbitraires.** Tout seuil l'est. Le calcul est donc refait avec trois variantes : plus de 50 % des victoires, deux saisons suffisent, aucune saison creuse admise. Une hégémonie retrouvée dans les trois variantes est dite **robuste**, même si ses bornes bougent un peu.

On compte à quatre niveaux :

- le **nom d'écurie** ;
- la **lignée**, c'est-à-dire la même usine sous plusieurs noms, comme [Brackley]({{ site.baseurl }}/ecuries/), de Tyrrell à Mercedes ;
- le **pilote** ;
- le **motoriste**.

## Les écuries

{% include hegemonies.html quoi="tableau" unite="ecurie" %}

Neuf hégémonies en soixante-seize saisons. Trois traits ressortent.

- **Les plus écrasantes sont les plus récentes.** [Mercedes]({{ site.baseurl }}/ecuries/mercedes/) gagne 69 % des Grands Prix pendant huit saisons, de 2014 à 2021. [Red Bull]({{ site.baseurl }}/ecuries/red-bull/), de 2021 à 2023, en gagne 74 %. Les deux hégémonies des années 1960 et 1970, celles de Lotus et de Ferrari, n'en gagnent qu'environ un tiers.
- **La plus longue est celle de [Ferrari]({{ site.baseurl }}/ecuries/ferrari/), de 1999 à 2008** : huit titres en dix saisons, interrompus seulement par 2005.
- **[Lotus]({{ site.baseurl }}/ecuries/team-lotus/), de 1968 à 1973, n'est pas robuste.** Elle alterne titres et saisons creuses, et ne passe jamais 47 % des victoires.

Les dominations de deux saisons seulement ne sont pas comptées comme hégémonies : {% include hegemonies.html quoi="courtes" unite="ecurie" %}. Elles reparaissent dès qu'on abaisse le seuil à deux saisons, et ce sont elles qui rendent les hégémonies de Lotus et de McLaren 1998-2000 fragiles.

À l'échelle des **lignées**, le tableau est presque le même. Red Bull y devient Milton Keynes, Mercedes devient Brackley, et Enstone ne compte que deux dominations de deux saisons, sous les noms de Benetton (1994-1995) et de Renault (2005-2006). Aucune lignée ne forme une hégémonie en additionnant ses noms successifs. Brackley, par exemple, gagne avec Brawn en 2009 puis avec Mercedes à partir de 2014, mais les quatre saisons intermédiaires restent trop creuses.

{% include hegemonies.html quoi="tableau" unite="lignee" %}

## Les pilotes

{% include hegemonies.html quoi="tableau" unite="pilote" %}

Les hégémonies de pilotes se calquent presque toujours sur celles de leur écurie : Schumacher sur Ferrari, Vettel et Verstappen sur Red Bull, Hamilton sur Mercedes. Deux exceptions :

- **Fangio**, de 1954 à 1957, domine sur Mercedes-Benz, Ferrari et Maserati.
- **Stewart**, de 1969 à 1973, domine sur Matra, March et Tyrrell.

Leur hégémonie traverse plusieurs écuries : le pilote change de voiture et continue de gagner. Prost et Senna, eux, se partagent la même McLaren : leurs hégémonies se recouvrent, et aucune n'est robuste.

Dominations de deux saisons : {% include hegemonies.html quoi="courtes" unite="pilote" %}.

## Les motoristes

{% include hegemonies.html quoi="tableau" unite="motoriste" %}

C'est à ce niveau que se trouve la plus longue domination : celle des moteurs **Ford**, dont le [Cosworth DFV]({{ site.baseurl }}/chronologie/#j-dfv). Ils sont dominants quinze saisons sur quinze, de 1968 à 1982, et gagnent 70 % des Grands Prix, pour Lotus, McLaren, Tyrrell et d'autres.

Le DFV est vendu à tous. Il n'y a donc pas d'hégémonie d'écurie qui lui corresponde, mais une succession d'écuries championnes avec le même moteur. Climax avant lui, Honda et Renault ensuite dominent de la même façon à travers plusieurs écuries.

Le Mercedes de 2012-2021 commence avant l'écurie Mercedes. Il gagne d'abord avec McLaren, puis avec Mercedes et Racing Point.

## Innovations et résultats : trois confrontations

### Méthode

Le mot « corrélation » serait trompeur : la chronologie compte 43 jalons, beaucoup trop peu pour une statistique. On fait donc des comparaisons **avant / après**, et chacune est mesurée contre un **témoin**. Le témoin, c'est ce qu'on observerait à n'importe quelle saison, pour les mêmes écuries.

Le vocabulaire est celui du [dossier sur la causalité]({{ site.baseurl }}/dossiers/causalite/). Qu'une hégémonie suive un jalon est un recoupement **chronologique**, jamais une preuve. Un lien n'est plus que chronologique que si la chronologie l'établit déjà par une source.

### 1. Les jalons techniques

Chaque jalon est rattaché à l'écurie qui l'a porté, d'après les fiches des écuries. On compare sa part de victoires dans les deux saisons qui précèdent le jalon et dans les trois saisons qui commencent avec lui. On regarde aussi si une hégémonie commence dans les deux ans.

{% include hegemonies.html quoi="jalons" %}

Sur {{ TJ.n }} jalons portés par une écurie qui ne dominait pas encore, **{{ TJ.ouvre }} précèdent de peu une hégémonie** :

- le [DFV]({{ site.baseurl }}/chronologie/#j-dfv) chez Lotus en 1967 ;
- la [312T]({{ site.baseurl }}/chronologie/#j-ferrari-312t) chez Ferrari en 1975 ;
- la [MP4/4]({{ site.baseurl }}/chronologie/#j-mp4-4) chez McLaren en 1988 ;
- la [RB6]({{ site.baseurl }}/chronologie/#j-rb6) chez Red Bull en 2010 ;
- le [groupe propulseur hybride]({{ site.baseurl }}/chronologie/#j-hybride) chez Mercedes en 2014.

Le témoin prend les mêmes écuries à n'importe quelle saison où elles ne dominent pas. Il en attend environ {{ TJ.attendu | replace: ".", "," }}. **Les jalons précèdent donc une hégémonie à peu près deux fois plus souvent que le hasard, mais sur cinq cas.** C'est un indice, pas une démonstration.

Les contre-exemples sont plus nombreux que les exemples, et ils sont instructifs.

- **L'innovation sans hégémonie.** La [Lotus 78]({{ site.baseurl }}/chronologie/#j-lotus-78) fait passer Lotus de 3 % à 27 % des victoires, sans hégémonie à la suite. La [Benetton de 1993]({{ site.baseurl }}/chronologie/#j-cfd-benetton) fait passer son écurie de 6 % à 40 %, pour deux saisons de domination seulement. Le [double diffuseur]({{ site.baseurl }}/chronologie/#j-double-diffuseur) vaut à Brawn un titre en 2009, puis l'écurie change de nom. La [MP4/1]({{ site.baseurl }}/chronologie/#j-mp4-1) en carbone ne conduit McLaren qu'à deux titres, en 1984 et 1985.
- **L'innovation pendant une hégémonie.** La [FW14B]({{ site.baseurl }}/chronologie/#j-fw14b), la [Lotus 72]({{ site.baseurl }}/chronologie/#j-lotus-72) et la [RB18]({{ site.baseurl }}/chronologie/#j-rb18) arrivent alors que leur écurie domine déjà. Elles la prolongent ; elles ne l'ouvrent pas.
- **L'hégémonie sans jalon.** Aucun jalon de la chronologie n'accompagne celle de Ferrari en 1999-2008, ni celle de McLaren en 1998-2000. Les jalons retenus ne les expliquent pas : elles tiennent à autre chose, ou à des innovations que la chronologie ne retient pas.

### 2. Les ingénieurs

Les fiches des écuries datent l'arrivée et le départ de chaque ingénieur. Pour une **arrivée**, on compare la part de victoires de l'écurie dans les deux saisons qui précèdent et dans les trois qui commencent avec l'ingénieur. Pour un **départ**, on compare les deux dernières saisons avec lui et les trois suivantes. Un écart de plus de 5 points compte comme une hausse ou une baisse.

{% include hegemonies.html quoi="ingenieurs" %}

Deux constats :

- **Une écurie progresse après une arrivée plus souvent qu'à une saison quelconque** : {{ BI.arrivee.hausse | times: 100.0 | divided_by: BI.arrivee.n | round }} % des cas, contre {{ BI.temoin.hausse | times: 100.0 | divided_by: BI.temoin.n | round }} % pour le témoin.
- **Un départ ne change presque rien.** Les hausses et les baisses s'y équilibrent, à peu près comme dans le témoin.

La lecture la plus simple, « l'ingénieur fait gagner », n'est pas la seule. Une écurie en essor a aussi les moyens de recruter. L'arrivée peut donc accompagner l'essor autant que le provoquer. Le départ sans effet visible suggère qu'une organisation garde son élan quelques saisons après le départ d'un ingénieur.

La vue inverse est plus parlante : qui était là quand chaque hégémonie a commencé ? Un ingénieur est compté s'il est arrivé avant le début et parti au plus trois saisons avant. Quand sa date de départ n'est pas connue et qu'il est arrivé plus de trois saisons avant, sa présence est dite incertaine.

{% include hegemonies.html quoi="racines" %}

Deux ingénieurs sont présents au début de trois des neuf hégémonies d'écurie :

- [Adrian Newey]({{ site.baseurl }}/ingenieurs/adrian-newey/) : Williams 1991, McLaren 1998 et Red Bull 2010, plus Red Bull 2021, où sa présence est incertaine faute de date de départ connue chez Red Bull ;
- [Geoff Willis]({{ site.baseurl }}/ingenieurs/geoff-willis/) : Williams 1991, Red Bull 2010 et Mercedes 2014.

[Ross Brawn]({{ site.baseurl }}/ingenieurs/ross-brawn/) est présent au début de deux hégémonies, Ferrari 1999 et Mercedes 2014, et peut-être d'une troisième, Williams 1991. Cela ne mesure pas leur mérite, que le [classement]({{ site.baseurl }}/dossiers/methode/) évalue autrement : cela situe où ils se trouvaient.

### 3. Les règlements

Pour chaque début d'hégémonie, d'écurie, de pilote ou de motoriste, on cherche un changement de règlement de la chronologie dans l'année même ou l'année d'avant. Pour chaque fin, on en cherche un dans l'année de la dernière saison dominante ou l'année suivante.

**{{ TR.debuts_regle }} débuts sur {{ TR.debuts }}** coïncident avec un changement de règlement, et **{{ TR.fins_regle }} fins sur {{ TR.fins }}**. Mais ces changements sont si fréquents que {{ TR.avec_regle }} saisons sur {{ TR.annees }} en ont un dans la même fenêtre : à peu près la même proportion. **En moyenne, un changement de règlement n'ouvre ni ne ferme plus souvent une hégémonie qu'une saison ordinaire.**

Quelques coïncidences sont pourtant nettes :

- le [groupe propulseur hybride obligatoire]({{ site.baseurl }}/chronologie/#c-groupe-propulseur-2014) de 2014 précède de peu l'hégémonie de Mercedes et celle de Hamilton ;
- la [refonte aérodynamique de 2009]({{ site.baseurl }}/chronologie/#c-refonte-aero-2009) précède celle de Red Bull ;
- le [retour de l'effet de sol]({{ site.baseurl }}/chronologie/#c-retour-effet-de-sol), en 2022, suit de peu la fin de celle de Mercedes ;
- la [formule 3 litres]({{ site.baseurl }}/chronologie/#c-formule-3-litres), en 1966, suit de peu la fin de celle du Climax ;
- le [fond plat]({{ site.baseurl }}/chronologie/#c-fond-plat), en 1983, suit de peu la fin de celle du Ford.

Dans ces cinq cas, il s'agit d'une refonte d'ensemble des voitures ou des moteurs, et non d'un simple ajustement. Ces coïncidences restent chronologiques : la chronologie ne trace aucun lien sourcé entre ces règlements et les résultats.

## Limites

- **La victoire n'est pas la seule mesure.** Elle ignore les écuries qui progressent sans gagner, et elle reflète aussi le talent du pilote, la fiabilité et les budgets.
- **Les jalons sont une sélection.** La chronologie retient les innovations qui ont changé la conception des voitures, pas celles qui ont fait gagner. Une hégémonie sans jalon peut cacher une innovation non retenue.
- **Le rattachement d'un jalon à une écurie suit les fiches.** Quatre jalons n'y sont rattachés à aucune écurie, et ne sont donc pas comptés : le [prototype Cooper 500]({{ site.baseurl }}/chronologie/#j-cooper-500), le [FVA]({{ site.baseurl }}/chronologie/#j-dfv-fva), le [rappel pneumatique des soupapes]({{ site.baseurl }}/chronologie/#j-rappel-pneumatique) et le [V10 Renault]({{ site.baseurl }}/chronologie/#j-v10-renault).
- **Les dates des ingénieurs sont parfois incomplètes.** Une date de départ manquante rend une présence incertaine, et le tableau le signale.
- **Les 500 miles d'Indianapolis (1950-1960) comptent au championnat.** Elles figurent donc ici, gagnées par des constructeurs américains qui n'ont pas de fiche sur le site.
- **Les seuils restent des choix.** La colonne « Robuste » dit quelles hégémonies y résistent.

## Sources

Résultats consultés le 29 octobre 2026 sur formula1.com, pour chaque saison de 1950 à 2025 :

- les vainqueurs des Grands Prix : `https://www.formula1.com/en/results/<année>/races` ;
- le classement des constructeurs, depuis 1958 : `…/<année>/team` ;
- le classement des pilotes : `…/<année>/drivers`.

Le lien de chaque course est conservé dans les données du site. Les ingénieurs, les jalons et les règlements viennent des [fiches des écuries]({{ site.baseurl }}/ecuries/) et de la [chronologie]({{ site.baseurl }}/chronologie/), où chacun a ses propres sources.
