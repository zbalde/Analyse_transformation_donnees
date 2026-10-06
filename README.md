# Trafic routier à Paris : avenue de Versailles, Sèvres, quai d'Orsay

## La question

Entre mars et août 2026, comment se comparent le débit, l'occupation et l'état du trafic sur l'avenue de Versailles, l'axe Sèvres et le quai d'Orsay ?

## Les données

Source : [Comptages routiers permanents](https://opendata.paris.fr/explore/dataset/comptages-routiers-permanents/), Ville de Paris.  
Axes (noms exacts) : `Av_de_Versailles`, `Sevres`, `Quai_d'Orsay`.  
Période : 1er mars 2026 → 31 août 2026, heure de fin de mesure.  
Volume : 178 924 lignes, 11 colonnes, 41 arcs (16, 10 et 15). Seuls le débit `q` (12,8 %) et le taux `k` (17,4 %) ont des valeurs manquantes.

Pièges rencontrés : l'apostrophe de `Quai_d'Orsay` casse le filtre ODSQL si elle n'est pas échappée par un antislash ; le CSV est en UTF-8 avec BOM et séparé par des points-virgules ; `etat_trafic` et `etat_barre` arrivent en libellés français, pas en codes entiers de la notice 2019 ; `t_1h` est en UTC.

Le détail des étapes est dans [METHODE.md](METHODE.md). L'exploration est dans `notebooks/01_m1_exploration.ipynb`.

## Résultats

- **Débit et occupation.** Sur chaque axe, le débit est plus souvent renseigné que le taux d'occupation. L'écart est le plus net avenue de Versailles (92,7 % de débit contre 84,1 % d'occupation, soit 8,6 points). Au quai d'Orsay : 89,3 % contre 86,4 %. Sur Sèvres : 75,3 % contre 74,3 %, l'écart le plus faible, mais aussi l'axe le moins bien mesuré dans l'ensemble. On peut donc souvent compter des voitures sans connaître le niveau d'encombrement.
- **Composition du trafic par état.** Sur les trois axes, le trafic est surtout fluide. Le quai d'Orsay et l'avenue de Versailles le sont 86 % et 83 % du temps ; Sèvres seulement 69 %, avec beaucoup plus d'heures « Inconnu » (25,7 %) et un peu plus de pré-saturation (4 %). « Inconnu » suit exactement l'absence de taux d'occupation (`k` manquant), pas un embouteillage : ce n'est donc pas une mesure de congestion.
- **Profil horaire.** Même rythme partout (creux à 5 h, journée chargée), mais pas les mêmes niveaux. Le quai d'Orsay reste le plus fréquenté à chaque heure et pointe à 19 h (486 véh/h), comme l'avenue de Versailles (393 véh/h). Sèvres plafonne dès midi (176 véh/h) et ne montre pas la même pointe du soir.

Figures : `figures/01_barres_tirets.png`, `figures/02_barres_etats.png`, `figures/03_debit_horaire.png`.

## Limites

Une ligne est une heure sur un arc, pas un résumé de toute la rue. Six mois de printemps-été ne disent rien de l'hiver. L'état « Inconnu » suit l'absence de taux d'occupation : ce n'est pas une mesure de congestion. Saturé et bloqué restent rares, donc ces données décrivent surtout un trafic fluide.

## Lancer le projet

```bash
pip install -r requirements.txt
python download_data.py
jupyter nbconvert --to notebook --execute --inplace notebooks/01_m1_exploration.ipynb
```

## Utilisation de l'IA

Cursor (Grok) a servi à corriger le téléchargement, choisir les types d'après la notice et l'export réel, écrire le notebook d'exploration et rédiger ce README. Les phrases sous les graphiques sont calculées dans le notebook à partir des tableaux, puis relues après exécution. Le filtre sur l'apostrophe a été vérifié par un appel API d'une ligne avant le téléchargement complet.

Les trois graphiques Altair du jalon initial ont ensuite été remplacés par des graphiques matplotlib plus simples à lire (barres pleines, barre empilée à 100 %, courbes à étiquettes directes), avec Claude, à partir des mêmes tableaux calculés dans le notebook — aucun chiffre n'a changé, seule leur mise en forme. Les textes d'explication et d'interprétation ont été réécrits à la main par la suite.