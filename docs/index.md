# Documentation PyNativeX

PyNativeX veut offrir une expérience proche des frameworks déclaratifs modernes sans imposer Dart
ou JavaScript aux auteurs d’applications. Le code produit aujourd’hui constitue le **jalon zéro** :
les API et frontières d’architecture nécessaires pour mesurer les hypothèses du cahier des charges.

## Démarrer

1. Installez Python 3.11 ou plus récent.
2. Exécutez `python -m pip install -e ".[dev]"`.
3. Vérifiez la CLI avec `pynativex --version`.
4. Affichez un lot d’opérations avec `pynativex inspect --pretty`.
5. Créez un projet avec `pynativex create mon-app`.

## Modèle d’interface

Les widgets sont des objets immuables à slots. `Widget.children()` décrit l’arbre et
`Reconciler.mount()` produit un lot atomique `CREATE`/`INSERT`/`COMMIT`. Le format JSON utilisé par
le prototype rend le contrat observable ; FlatBuffers le remplacera lorsque le schéma sera figé.

Un champ `pn.field()` marque son `State` comme sale à l’affectation. Plusieurs affectations avant
la prochaine frame restent coalescées en un seul état sale.

## Contrat natif

`core/include/pynativex/pynativex_core.h` est la frontière C stable. Elle versionne l’ABI, crée le
moteur et n’accepte que des séquences strictement croissantes. Sur Android, les méthodes JNI sont
enregistrées explicitement dans `JNI_OnLoad` conformément au cahier des charges.

Le prototype **ne dessine pas encore de pixels**. Les prochains critères techniques sont :

- intégrer Yoga puis Skia GLES ;
- embarquer CPython Android sur un thread dédié ;
- relier les lots Python à l’ABI sans copie inutile ;
- mesurer taille, première frame, RSS et fluidité sur appareils Android Go ;
- publier les artefacts moteur seulement après validation de ces mesures.

## CLI

- `pynativex create NAME` crée un projet minimal sans question interactive ;
- `pynativex doctor` retourne un code non nul si la toolchain Android manque ;
- `pynativex inspect` rend le protocole observable ;
- `pynativex build android --dry-run` valide une demande ;
- `pynativex build android` échoue explicitement tant que le moteur Android n’est pas publié.

Ajoutez `--json` avant la sous-commande pour une sortie exploitable par les outils.

## Exemples

1. `examples/hello` : texte et structure minimale ;
2. `examples/counter` : état réactif et callback ;
3. `examples/showcase` : composition d’un écran plus riche.

## Limites connues

La navigation, l’IME, le réseau natif, la caméra, le stockage sécurisé, Skia et le packaging APK/AAB
restent à implémenter. Les budgets de 15 Mo et 60 fps sont des objectifs à mesurer, pas des résultats
acquis.
