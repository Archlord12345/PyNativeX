import pynativex as pn

app = pn.App(
    title="Hello PyNativeX",
    home=pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("PyNativeX")),
        body=pn.Center(
            pn.Text(
                "Python → protocole natif → C++",
                style=pn.TextStyle(size=22, weight=600, color=0xFF0284C7),
            )
        ),
    ),
)
