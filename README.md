# TP Déploiement — CI/CD complète (ClientHub API)

API Flask conteneurisée, testée et déployée automatiquement sur une VM Azure
à chaque push sur `main`, via GitHub Actions.

## Application
Petite API Flask (`app.py`) qui écoute sur le port **8000** et expose :
- `GET /health` → `{"status": "ok"}` (vérification de disponibilité)
- `GET /hello` → un message + l'auteur (fonctionnalité de démonstration)

## Fonctionnement du pipeline
Le workflow `.github/workflows/deploy.yml` se déclenche à **chaque push sur `main`**
et enchaîne 4 jobs (chacun ne démarre que si le précédent réussit) :

1. **unit-tests** — installe les dépendances et lance les tests unitaires
   (`pytest tests/test_unit.py`), via le client de test Flask.
2. **e2e-tests** — build l'image, lance le conteneur, et teste l'API par de
   vraies requêtes HTTP (`tests/test_e2e.py`) : disponibilité (`/health`) + une
   fonctionnalité (`/hello`).
3. **build-and-push** — seulement si les tests passent. Build l'image Docker,
   la tague avec `latest` **et** le SHA du commit, puis la pousse sur Docker Hub
   (`melia15/myapp`).
4. **deploy** — se connecte en **SSH** à la VM Azure, `pull` la dernière image,
   relance le conteneur et vérifie `/health`.

## Comment le déploiement est déclenché
Aucune action manuelle : un simple `git push` sur `main` déclenche toute la
chaîne jusqu'au déploiement. L'application est accessible sur
**http://40.66.52.118:8006**.

## Idempotence
Le job de déploiement supprime l'ancien conteneur avant d'en relancer un
(`docker rm -f boukri_amelia || true` puis `docker run --name boukri_amelia`).
Relancer le workflow ou repousser le même commit ne crée donc pas de doublon
et ne casse pas le service.

## Sécurité — secrets
Aucun identifiant en clair dans le dépôt. Tout passe par **GitHub Secrets** :
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` — accès Docker Hub
- `VM_HOST`, `VM_USER`, `VM_PASSWORD` — accès SSH à la VM Azure

## Choix techniques
- **Flask** : framework léger, parfait pour une petite API.
- **pytest + requests** : tests unitaires simples, réutilisés en E2E via HTTP.
- **Docker** (image Python slim) : appli isolée et reproductible, port 8000 interne.
- **GitHub Actions** : CI/CD native au dépôt, jobs chaînés par `needs:`.
- **appleboy/ssh-action** : déploiement SSH depuis la pipeline.
- **Tags `latest` + SHA** : `latest` pour le déploiement courant, le SHA pour
  tracer précisément la version déployée.

## Lancer en local
\`\`\`
pip install -r requirements.txt pytest requests
python app.py                      # http://localhost:8000
python -m pytest tests/test_unit.py
\`\`\`