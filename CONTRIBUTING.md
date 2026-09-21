# Contribuer à PyNativeX

Merci de contribuer. Avant une modification importante, ouvrez un ticket décrivant le problème,
les contraintes Android/iOS et l’impact sur les contrats publics.

## Environnement

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
ruff check .
cmake -S core -B build/core -DBUILD_TESTING=ON
cmake --build build/core
ctest --test-dir build/core --output-on-failure
```

## Règles de contribution

- Une pull request traite un problème cohérent.
- Toute API publique Python est typée et testée.
- Toute évolution du protocole incrémente sa version et documente la compatibilité.
- Le chemin critique du rendu ne rappelle jamais Python.
- Les fonctions JNI sont enregistrées explicitement ; aucun `JNIEnv*` n’est partagé entre threads.
- Une affirmation de performance inclut l’appareil, le build, la commande et les résultats bruts.
- Les textes destinés aux utilisateurs sont proposés en français et, si possible, en anglais.

## Commits et revue

Utilisez un sujet de commit impératif et précis. La revue vérifie d’abord la correction, la sécurité,
la compatibilité et les mesures ; les préférences stylistiques automatisables relèvent des outils.

En participant, vous acceptez le `CODE_OF_CONDUCT.md` et certifiez avoir le droit de placer votre
contribution sous Apache-2.0.
