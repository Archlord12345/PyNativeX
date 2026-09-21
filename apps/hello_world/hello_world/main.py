import pynativex as pn

app = pn.App(
    title="Hello World",
    home=pn.Scaffold(
        app_bar=pn.AppBar(pn.Text("PyNativeX Hello")),
        body=pn.Center(pn.Text("Hello World!")),
    ),
)
