# Rejoindre la communauté PyNativeX

PyNativeX est porté par Kernel Forge et accueille les contributions sur Python, C++20, Android/Kotlin,
iOS/Swift, documentation, design et tests sur appareils d’entrée de gamme.

## Où échanger

- [Dépôt GitHub `PyNativeX-Inc/PyNativeX`](https://github.com/PyNativeX-Inc/PyNativeX)
- [Groupe WhatsApp PyNativeX](https://chat.whatsapp.com/CXSjNzxzH8J0LxtZqMCjKh)
- Discussions et tickets du dépôt pour les décisions durables
- Pull requests pour toute modification de code ou de documentation

Le groupe WhatsApp sert aux échanges rapides. Une décision technique prise dans le groupe doit être
reformulée dans un ticket, une RFC ou une ADR afin qu’elle reste publique et consultable.

## Première contribution

1. Lisez le `README`, la documentation et le code de conduite.
2. Choisissez un ticket marqué `good first issue` ou proposez un problème reproductible.
3. Pour une décision d’architecture, ouvrez d’abord une RFC.
4. Ajoutez des tests et indiquez les appareils/toolchains utilisés.
5. Ouvrez une pull request courte avec une description du comportement avant/après.

## Équipes de travail

- **SDK Python** : widgets, état, reconcile, navigation et ergonomie ;
- **Moteur C++** : protocole, scheduler, Yoga, Skia, texte et gestes ;
- **Android** : Kotlin, JNI, IME, accessibilité et plugins ;
- **iOS** : Swift, ObjC++, Metal et plugins ;
- **Qualité** : benchmarks, appareils bas de gamme, sécurité et documentation FR/EN.

## Règles essentielles

- aucune donnée de carte bancaire ne doit traverser le code Python ;
- aucune promesse de performance ne doit être publiée sans mesure reproductible ;
- les API publiques et protocoles sont versionnés ;
- Android passe avant iOS jusqu’au franchissement des jalons du MVP ;
- les contributions respectent le code de conduite.
