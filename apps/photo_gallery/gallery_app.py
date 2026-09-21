from __future__ import annotations

import pynativex as pn

PHOTOS = (
    "mount_cameroon",
    "limbe_beach",
    "rainforest",
)

TITLES = (
    "Mont Cameroun",
    "Rivage de Limbé",
    "Forêt tropicale",
)

CAPTIONS = (
    "Là où la montagne rencontre les nuages.",
    "La lumière dorée sur le sable volcanique.",
    "Au cœur d’une nature vivante et préservée.",
)

app = pn.App(
    title="Échos du Cameroun",
    home=pn.Scaffold(
        app_bar=pn.AppBar(
            pn.Text(
                "Échos du Cameroun",
                style=pn.TextStyle(size=24, weight=700, color=0xFFFFFFFF),
            )
        ),
        body=pn.Column(
            [
                pn.Text(
                    "Carnet visuel",
                    style=pn.TextStyle(size=13, weight=700, color=0xFF38BDF8),
                ),
                pn.Text(
                    "Explorez trois paysages, glissez pour voyager.",
                    style=pn.TextStyle(size=18, color=0xFFE2E8F0),
                ),
                pn.PhotoGallery(
                    assets=PHOTOS,
                    titles=TITLES,
                    captions=CAPTIONS,
                    auto_play_seconds=4,
                    height=430,
                ),
            ],
            spacing=10,
        ),
    ),
)
