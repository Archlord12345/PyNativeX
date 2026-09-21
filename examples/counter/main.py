import pynativex as pn


class CounterState(pn.State):
    count = pn.field(0)

    def increment(self) -> None:
        self.count += 1

    def build(self, context: pn.BuildContext) -> pn.Widget:
        return pn.Scaffold(
            app_bar=pn.AppBar(pn.Text("Compteur")),
            body=pn.Center(
                pn.Column(
                    [
                        pn.Text(f"Valeur : {self.count}", style=pn.TextStyle(size=28)),
                        pn.Button("Ajouter", on_press=self.increment),
                    ],
                    spacing=16,
                )
            ),
        )


state = CounterState()
app = pn.App(home=state.build(pn.BuildContext()), title="Counter")
