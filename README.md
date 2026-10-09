# Trafic routier à Paris : avenue de Versailles, Sèvres, quai d'Orsay

## La question

Comment la congestion varie-t-elle selon l'heure, le jour et l'axe sur l'avenue de Versailles, l'axe Sèvres et le quai d'Orsay, et le débit suffit-il à la mesurer ?

## Les données

Source : [Comptages routiers permanents](https://opendata.paris.fr/explore/dataset/comptages-routiers-permanents/), Ville de Paris (opendata.paris.fr).
Axes (noms exacts) : `Av_de_Versailles`, `Sevres`, `Quai_d'Orsay`.
Période : du 1er mars 2026 au 1er septembre 2026 (exclu), une mesure par heure et par capteur, `t_1h` en UTC.

- **Données brutes** : 178 924 lignes, 11 colonnes, 41 capteurs (`data/raw/comptages.csv`). Le débit `q` manque dans 12,8 % des lignes et l'occupation `k` dans 17,4 %.
- **Nettoyage** (`jour_2`) : on retire les heures `Invalide` (14 183) et `Barré` (196), on comble les trous de 3 heures au maximum par interpolation (par capteur), puis on supprime les lignes où `q` ou `k` manque encore. Il reste **142 087 lignes, 10 colonnes, 36 capteurs** (14 à Versailles, 14 à Orsay, 8 à Sèvres), sans valeur manquante (`data/processed/comptages_propre.csv`).
- **Capteurs perdus (5)** : le 349 n'a jamais de débit, les 4400, 4649 et 4721 n'ont jamais d'occupation, le 348 est `Invalide` sur toute la période.
- **Transformation** (`jour_3`) : variables temporelles en heure de Paris, encodage de `etat_trafic` (ordinal) et `etat_barre` (one-hot), débits aberrants invalidés, statistiques par axe (`data/processed/comptages_apres_transformation_statistiques.csv`).

Pièges rencontrés : l'apostrophe de `Quai_d'Orsay` casse le filtre ODSQL si elle n'est pas échappée par un antislash ; `etat_trafic` et `etat_barre` arrivent en libellés français ; `t_1h` est en UTC.

## Résultats

Calculés sur les 142 087 lignes nettoyées. Le débit étant recopié sur plusieurs capteurs (29 séries distinctes pour 36 capteurs), il n'est compté qu'une fois par série.

- **La congestion se concentre sur Sèvres.** 7,4 % des heures y sont Pré-saturé, Saturé ou Bloqué, contre 1,1 % sur l'avenue de Versailles et 0,5 % sur le quai d'Orsay. Les heures Bloqué restent rares partout (0,24 % sur Sèvres).
- **Les pointes ne tombent pas aux mêmes heures.** En jours ouvrés, l'occupation médiane est maximale à 9 h sur l'avenue de Versailles (4,2 %), à 20 h sur le quai d'Orsay (5,2 %) et à 18 h sur Sèvres (8,6 %). Seule l'avenue de Versailles a une vraie pointe du matin, absente le week-end.
- **Le quai d'Orsay est l'axe le plus fréquenté.** Débit médian de 342 véh/h (236 pour Versailles, 164 pour Sèvres). En semaine à 19 h : environ 500 véh/h à Orsay, 440 à Versailles, 180 à Sèvres.
- **Le débit seul ne dit pas la congestion.** Sèvres a le plus faible débit mais l'occupation moyenne la plus élevée (5,5 %, contre 3,8 % et 2,9 %). Le diagramme fondamental montre le débit médian monter de 232 véh/h (occupation inférieure à 5 %) à 668 véh/h (30 à 35 %), puis plafonner entre 600 et 700 véh/h : au-delà, plus de véhicules sur le capteur ne veut pas dire plus de véhicules qui passent.
- **Qualité des mesures.** 13 capteurs sur 36 partagent leur série de débit avec au moins un autre capteur (29 séries distinctes), et 6 valeurs impossibles (5 193 à 5 484 véh/h sur les capteurs 4499 et 4505, le 24 juin) ont été invalidées. Le débit maximal plausible est de 1 497 véh/h.

Figures (`figures/`) : `01_barres_tirets.png`, `02_barres_etats.png`, `03_debit_horaire.png` (exploration brute, `jour_1`), puis `04_profil_horaire_semaine_weekend.png`, `05_heatmap_occupation.png` et `06_diagramme_fondamental.png` (analyse, `jour_4`).

## Limites

- Une ligne est une heure sur un capteur, pas un résumé de toute la rue ; six mois de printemps-été ne disent rien de l'hiver, et les pointes sont des médianes sur cette période.
- Cinq capteurs ont été exclus, dont deux sur les dix de Sèvres : la comparaison entre axes repose sur un nombre inégal de capteurs (14, 14 et 8).
- Au-delà de 30 % d'occupation il y a très peu de mesures. La médiane y est instable, et son maximum (825 véh/h pour 60 à 65 %) n'est pas un seuil de saturation. Le pic puis le creux autour de 5 à 15 % d'occupation viennent de la composition des capteurs dans chaque tranche, pas d'un phénomène de trafic.
- Le pic d'occupation du quai d'Orsay (73 %, dimanche 31 mai à minuit) est isolé et hors pointe : événement ponctuel ou défaillance du capteur, non vérifié.
- Les 885 heures `Inconnu` (état sans lien avec la congestion) sont laissées vides dans l'encodage ordinal.
- Le nombre de voies par axe est inconnu : les comparaisons de capacité restent indicatives.

## Lancer le projet

Une seule commande installe les dépendances, télécharge les données et exécute les 4 notebooks dans l'ordre :

```bash
python run_all.py
```

Ou étape par étape :

```bash
pip install -r requirements.txt
python download_data.py
```

puis exécuter les notebooks dans l'ordre :

1. `jour_1_analyse.ipynb` : chargement, types, valeurs manquantes, trois graphiques
2. `jour_2_types_nettoyage.ipynb` : types, doublons, nettoyage, export de `comptages_propre.csv`
3. `jour_3_transformation_statistiques.ipynb` : variables temporelles, encodage, aberrants, statistiques par axe
4. `jour_4_analyse.ipynb` : profil horaire, heatmap, diagramme fondamental

## Utilisation de l'IA

Cursor (Grok) a servi à corriger le téléchargement, choisir les types d'après la notice et l'export réel, écrire le notebook d'exploration (`jour_1`) et une première version de ce README. Claude a servi à remettre en forme les trois graphiques du jalon initial (aucun chiffre changé), à écrire le code des visualisations de `jour_4` et un premier jet des textes d'interprétation, et à recalculer et vérifier les chiffres de ce README à partir des notebooks. J'ai exécuté le code, relu et corrigé les textes, et vérifié que le projet se relance depuis les données brutes. Le filtre sur l'apostrophe avait été vérifié par un appel API d'une ligne avant le téléchargement complet.
