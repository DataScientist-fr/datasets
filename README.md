# datasets
Some useful datasets for learning data science

## Analyse visuelle — ECE Data Visualisation (chapitre 4)

Fichiers utilisés par les notebooks du chapitre « Analyse visuelle : de la question métier au brief ». Les notebooks les téléchargent depuis `https://raw.githubusercontent.com/DataScientist-fr/datasets/main/` et vérifient leur empreinte SHA-256 complète : **ne modifiez pas ces fichiers sans mettre à jour les notebooks**.

| Fichier | Contenu | Taille | SHA-256 (début) |
|---|---|---|---|
| `olist_brut_1.zip` | Tables d'origine Olist : commandes, clients, paiements. | 5.2 Mo | `c8482ca564fb9a61…` |
| `olist_brut_2.zip` | Tables d'origine Olist : articles, avis, produits, vendeurs, traduction des catégories, et table dérivée des centroïdes de codes postaux. | 5.5 Mo | `d48270ee21ceb6f9…` |
| `olist_commandes.csv.gz` | Table préparée : une ligne par commande (99 441), jointures faites, aucun indicateur précalculé. | 6.0 Mo | `a4f180ca8d921df9…` |
| `olist_articles.csv.gz` | Table préparée : une ligne par article commandé (112 650). | 1.9 Mo | `57d65356adf92131…` |
| `so_2024_2025.csv.gz` | Extrait de 25 colonnes des éditions 2024 et 2025 du Stack Overflow Developer Survey (114 628 réponses), avec une colonne SurveyYear. | 4.6 Mo | `35e6c96be283b62e…` |

### Olist — Brazilian E-Commerce Public Dataset

- Source : Olist, *Brazilian E-Commerce Public Dataset by Olist* — https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- Licence : **CC BY-NC-SA 4.0** — attribution, usage non commercial, partage dans les mêmes conditions. Les fichiers ci-dessus, dérivés de ce jeu, sont redistribués sous la même licence.
- Transformations : identifiants hexadécimaux remplacés par des codes entiers (correspondance commune à toutes les tables) ; table `olist_centroides_cep.csv` dérivée de la table de géolocalisation d'origine (position médiane par préfixe de code postal, points hors du Brésil écartés) ; tables `olist_commandes` et `olist_articles` construites par jointure, distance client–vendeur à vol d'oiseau entre centroïdes.

### Stack Overflow Developer Survey 2024 et 2025

- Source : Stack Overflow — https://survey.stackoverflow.co/
- Licence : **Open Database License (ODbL)** — attribution et partage dans les mêmes conditions.
- Transformations : sélection de 25 colonnes communes aux deux éditions, ajout de `SurveyYear` ; aucune réponse modifiée. L'édition 2026 remplacera 2024 dès la publication de ses réponses brutes.
