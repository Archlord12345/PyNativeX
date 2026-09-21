# Pocket Tasks

Pocket Tasks est la première application de démonstration construite avec PyNativeX. Elle présente :

- un tableau de bord mobile en français ;
- une liste de tâches avec catégories et statut ;
- les filtres Toutes, À faire et Terminées ;
- l’ajout rapide et le changement de statut ;
- un état vide ;
- des clés stables et des callbacks encodés dans le protocole natif.

Depuis la racine du dépôt :

```bash
python -m pip install -e ".[dev]"
PYTHONPATH=apps/pocket_tasks pynativex inspect \
  --entry pocket_tasks.main:app \
  --pretty \
  --output build/pocket-tasks/ui-batch.json

cd apps/pocket_tasks
pynativex build android --dry-run
```

La première commande exécute réellement le code Python de l’application et sérialise son arbre UI.
Le `--dry-run` valide la configuration Android. La production d’un APK restera désactivée tant que
le moteur PyNativeX Android (CPython embarqué, Yoga et Skia) n’est pas relié à cet arbre.
