# Échos du Cameroun

Application galerie Android construite avec PyNativeX.

L’interface est définie dans `gallery_app.py` avec les widgets Python `Scaffold`, `Column`, `Text`
et `PhotoGallery`. Avant chaque build Android, Gradle exécute `generate_ui.py`, qui compile cet arbre
en `gallery_ui.json`. L’hôte Kotlin lit le protocole et rend l’interface native.

Fonctionnalités :

- trois photographies disponibles hors ligne ;
- glissement horizontal, commandes précédente/suivante et indicateurs ;
- transition fondu/zoom ;
- lecture automatique toutes les quatre secondes, avec pause ;
- restauration de la photo courante après rotation ou recréation ;
- descriptions d’images pour l’accessibilité.

## Générer l’interface Python

```bash
python3 apps/photo_gallery/generate_ui.py \
  --output apps/photo_gallery/android/app/src/main/assets/gallery_ui.json
```

## Construire l’APK

```bash
cd apps/photo_gallery/android
./gradlew assembleDebug
```

APK produit :
`apps/photo_gallery/android/app/build/outputs/apk/debug/app-debug.apk`.
