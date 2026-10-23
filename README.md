# datapipelines
This repository is dedicated to a full ETL or ELT  project 

# Observatoire des offres d'emploi data 

Pipeline de données de bout en bout qui collecte, unifie et analyse les offres
d'emploi des métiers data (data analyst, analytics engineer, data engineer,
data scientist, BI) publiées en Europe et en remote.

Projet en cours de construction.

## Questions métier

- Combien d'offres data sont publiées, et comment ce volume évolue-t-il ?
- Où se trouvent-elles, et quelle part est ouverte au télétravail ?
- Quels outils sont les plus demandés (dbt, Airflow, Snowflake, Databricks, Python...) ?
- Quels salaires sont proposés, selon le métier et la séniorité ?
- Combien de temps une offre reste-t-elle en ligne ?

## Sources de données

| Source | Type | Accès |
|---|---|---|
| [Arbeitnow](https://www.arbeitnow.com) | Job board européen | API publique, sans clé |
| [Himalayas](https://himalayas.app) | Offres en remote | API publique, sans clé |
| [Jobicy](https://jobicy.com) | Offres en remote, avec salaires | API publique, sans clé |

Chaque source a son propre format : le pipeline les unifie dans un modèle commun,
dédoublonne les offres publiées sur plusieurs sites et normalise les salaires.
L'API Offres d'emploi de France Travail, actuellement suspendue, pourra être
ajoutée comme source supplémentaire lors de sa réouverture.

## Architecture

| Étape | Outil |
|---|---|
| Ingestion | Python, dlt |
| Stockage | Databricks (Free Edition) |
| Transformation | dbt |
| Orchestration | Airflow, GitHub Actions |
| Visualisation | Streamlit |

## Structure du repo

    ingestion/       scripts d'extraction et de chargement
    transform/       projet dbt (staging, intermediate, marts)
    orchestration/   DAGs Airflow
    dashboard/       application Streamlit
    docs/            schémas et documentation

## Installation

Prérequis : [uv](https://docs.astral.sh/uv/) et Git.

    git clone https://github.com/KUOQ/datapipelines.git
    cd datapipelines
    uv sync

## Avancement

- [x] Structure du projet et environnement Python
- [ ] Ingestion de la première source (Arbeitnow)
- [ ] Chargement dans Databricks
- [ ] Modèles dbt et tests
- [ ] Ajout des sources Himalayas et Jobicy
- [ ] Orchestration Airflow et GitHub Actions
- [ ] Dashboard Streamlit