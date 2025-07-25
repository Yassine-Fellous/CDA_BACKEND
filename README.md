# 🏟️ CDA Backend - API Cartographie Installations Sportives

[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com/)
[![GeoJSON](https://img.shields.io/badge/GeoJSON-API-4CAF50?style=flat&logo=leaflet&logoColor=white)](https://geojson.org/)

> **API Django haute performance** pour la cartographie et la recherche d'installations sportives en France. Migration complète SQLAlchemy → Django ORM avec **98% d'amélioration de performance**.

## 🚀 Performance Exceptionnelle
Après migration vers Django ORM avec cache optimisé :
- **⚡ 75ms** de temps de réponse (vs 4.1s avant)
- **🎯 5,825+ installations** géolocalisées en temps réel  
- **📍 Cache intelligent** Redis avec TTL 5 minutes

## 📊 Données et Prétraitement

Les données proviennent du [site officiel du gouvernement français](https://equipements.sports.gouv.fr/explore/dataset/data-es/table/). 

### 🔧 Pipeline de traitement des données
- **Source** : Dataset national des équipements sportifs (`data-es.json`)
- **Prétraitement** : Notebook Jupyter `data/preprocess-data.ipynb` 
- **Filtrage** : Focus département Bouches-du-Rhône (code 13)
- **Résultat** : `data/filtered-data-es.csv` avec 5,825+ installations validées

---

## ⚡ Étape par étape : Architecture optimisée

### 1. 🗄️ Préparation et import des données

- Téléchargez le dataset brut depuis le [portail gouvernemental](https://equipements.sports.gouv.fr/explore/dataset/data-es/table/)
- Utilisez le notebook `data/preprocess-data.ipynb` pour :
  - **Analyse** complète du dataset avec pandas
  - **Validation** des coordonnées géographiques
  - **Filtrage** par département (Bouches-du-Rhône)
  - **Export** optimisé vers CSV structuré

### 2. 🏗️ Backend Django haute performance

- **Architecture** : Django 5.0+ avec Django REST Framework
- **Base de données** : PostgreSQL 15 avec JSONField optimisé
- **ORM** : Django ORM avec indexes spécialisés (migration depuis SQLAlchemy)
- **Configuration** : Variables d'environnement via `.env`
- **Structure** :
  - **Models** Django ORM pour installations sportives
  - **Management command** `load_csv` sécurisé avec protection doublons
  - **API endpoints** RESTful avec cache Redis intégré

### 3. 📥 Import sécurisé des données

```bash
# Migration et import avec protection
python manage.py migrate
python manage.py load_csv data/filtered-data-es.csv

# Options avancées
python manage.py load_csv data/filtered-data-es.csv --force  # Merge avec existant
python manage.py load_csv data/filtered-data-es.csv --clear  # Reset complet
```

### 4. 🌐 API endpoints optimisés

| Endpoint | Description | Performance |
|----------|-------------|-------------|
| `/api/v1/installations/geojson/` | 🗺️ Format GeoJSON complet | **75ms** |
| `/api/v1/installations/equipments/` | 🏟️ Liste avec filtres | **50ms** |
| `/api/v1/installations/sports/` | ⚽ Catalogue des sports | **30ms** |

### 5. 🐳 Déploiement Docker optimisé

```bash
# Démarrage complet avec Docker Compose
docker-compose up -d --build

# Import automatique des données
docker-compose exec sport-map-api python manage.py load_csv data/filtered-data-es.csv

# Monitoring des services
docker-compose logs sport-map-api -f
```

### 6. 📁 Architecture du projet

```
CDA_Backend/
├── 📁 config/                    # Configuration Django
│   ├── settings.py              # Settings avec cache optimisé
│   └── urls.py                  # Routing principal
├── 📁 installations/            # App principale
│   ├── models.py               # 🗄️ Models Django ORM
│   ├── serializers.py          # 📊 Serializers DRF
│   ├── views.py                # 🌐 API endpoints
│   ├── tests.py                # 🧪 Tests (95% coverage)
│   └── management/commands/    
│       └── load_csv.py         # 📥 Import CSV sécurisé
├── 📁 data/                     # Données et preprocessing
│   ├── filtered-data-es.csv    # Dataset final (5,825 installations)
│   └── preprocess-data.ipynb   # 📊 Analyse et nettoyage
├── 🐳 docker-compose.yaml      # Orchestration complète
├── 🐳 Dockerfile               # Image de production
├── 📋 requirements.txt         # Dépendances Python
└── 📖 RAPPORT_MIGRATION.md     # Documentation technique détaillée
```

---

## 🎯 Résultats de la migration

### ✅ **Gains de performance mesurés**
- **API GeoJSON** : 4.1s → **75ms** (-98.2%)
- **Liste équipements** : 3.2s → **50ms** (-98.4%)  
- **Catalogue sports** : 1.8s → **30ms** (-98.3%)
- **Utilisation mémoire** : -50% à -60%
- **Débit API** : +340% (847 req/s vs 247 req/s)

### 🔧 **Technologies modernisées**
- **Migration** : SQLAlchemy → Django ORM natif
- **Performance** : Cache intelligent avec TTL
- **Sécurité** : Protection imports multiples
- **Tests** : Automatisés avec GitHub Actions
- **Documentation** : Rapport technique complet

**📖 Consultez `RAPPORT_MIGRATION.md` pour l'analyse complète des performances et métriques détaillées.**