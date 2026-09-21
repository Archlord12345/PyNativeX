# PyNativeX

[![CI](https://github.com/PyNativeX-Inc/PyNativeX/actions/workflows/ci.yml/badge.svg)](https://github.com/PyNativeX-Inc/PyNativeX/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

<p align="center">
  <img src="assets/0c51bfea-9b69-4621-8ef6-4200a0f92073.png" alt="PyNativeX — Build Native Mobile Apps with Python" width="440">
</p>

PyNativeX est un framework open source visant des applications mobiles natives écrites en Python :
Python pilote l’interface déclarative, un cœur C++ assure le rendu, et Kotlin/Swift donnent accès aux
plateformes. Android arm64 est prioritaire ; iOS reste expérimental.

> **État : pré-alpha (`0.1.0a1`).** Le SDK Python, le protocole d’opérations, la CLI, l’ABI C++
> et un hôte Android de galerie sont testables. Le rendu Skia et CPython embarqué ne sont pas
> encore livrés. `pynativex build android` refuse donc de prétendre produire un APK générique ;
> l’application **Échos du Cameroun** (`apps/photo_gallery`) est compilée nativement et publiée
> comme artefact GitHub Actions.
>
> Dépôt canonique : [github.com/PyNativeX-Inc/PyNativeX](https://github.com/PyNativeX-Inc/PyNativeX).

## Essai rapide

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pynativex inspect --pretty
pynativex create hello-mobile
cd hello-mobile
pynativex build android --dry-run
```

Exemple d’interface :

```python
import pynativex as pn

app = pn.App(
    title="Bonjour",
    home=pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("PyNativeX")),
        body=pn.Center(pn.Button("Continuer")),
    ),
)
```

## Architecture

| Plan | Langage | Responsabilité | État |
|---|---|---|---|
| Contrôle | Python 3.11+ | widgets immuables, état, reconcile, CLI | socle testable |
| Rendu | C++20 | ABI stable, lots d’opérations, futur Skia/Yoga | ABI et validation |
| Android | Kotlin | activité, `SurfaceView`, vsync, JNI | hôte minimal |
| iOS | Swift/ObjC++ | `CAMetalLayer`, plugins | planifié |

Le monorepo suit le cahier des charges :

- `sdk/python/pynativex` : API applicative et CLI ;
- `core` : cœur C++20 et ABI C stable ;
- `platform/android` : hôte Kotlin Android ;
- `examples` : Hello, Counter et Showcase ;
- `apps/pocket_tasks` : application mobile de démonstration avec état et interactions ;
- `apps/photo_gallery` : galerie Android dont l’interface est compilée depuis Python ;
- `docs` : architecture, roadmap et communauté ;
- `tests` : tests du SDK et de la CLI.

Inspecter l’application Pocket Tasks :

```bash
PYTHONPATH=apps/pocket_tasks pynativex inspect \
  --entry pocket_tasks.main:app \
  --pretty \
  --output build/pocket-tasks/ui-batch.json
```

## Intégration continue

Chaque push et chaque pull request sur `main` déclenche le workflow
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) :

- lint, typage et tests Python 3.11–3.13 ;
- compilation et tests C++ du cœur ;
- assemblage et vérification de l’APK debug de la galerie, puis dépôt de l’artefact
  `echos-cameroun-debug-apk`.

Le workflow peut aussi être lancé manuellement (*Actions → CI → Run workflow*).

## Développement

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
cmake -S core -B build/core -DBUILD_TESTING=ON
cmake --build build/core
ctest --test-dir build/core --output-on-failure
```

La documentation française est dans [`docs/index.md`](docs/index.md). La version anglaise et la
référence d’API générée sont prévues avant la bêta.

## Communauté

Lisez [`COMMUNITY.md`](COMMUNITY.md) pour rejoindre le projet, notamment le
[groupe WhatsApp PyNativeX](https://chat.whatsapp.com/CXSjNzxzH8J0LxtZqMCjKh).
Toute participation est soumise au [code de conduite](CODE_OF_CONDUCT.md).

## Licence

Apache-2.0. Ce choix suit la recommandation du cahier des charges et inclut une clause explicite de
brevets adaptée à un framework.
