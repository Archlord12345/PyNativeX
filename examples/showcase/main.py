import pynativex as pn


def feature(title: str, description: str, color: int) -> pn.Widget:
    return pn.Box(
        pn.Column(
            [
                pn.Text(title, style=pn.TextStyle(size=18, weight=700, color=0xFFFFFFFF)),
                pn.Text(description, style=pn.TextStyle(size=14, color=0xFFE0F2FE)),
            ],
            spacing=6,
        ),
        color=color,
        padding=18,
        radius=16,
    )


app = pn.App(
    title="PyNativeX Showcase",
    home=pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("Tableau de bord")),
        body=pn.Column(
            [
                pn.Text("Prêt pour le mobile natif", style=pn.TextStyle(size=30, weight=700)),
                pn.Text("Une interface déclarative, pilotée en Python."),
                feature("Contrôle Python", "État, navigation et logique métier.", 0xFF0369A1),
                feature("Moteur C++", "Layout, rendu, gestes et animations.", 0xFF1D4ED8),
                feature("Plateforme Kotlin", "Cycle de vie, IME et plugins Android.", 0xFF4338CA),
                pn.Button("Commencer"),
            ],
            spacing=14,
        ),
    ),
)
