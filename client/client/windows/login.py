
from .main import Main

from ..network import KXPageClient, StorageInfo
from ..config import VERSION, theme
from fasttk import *

class Login(Component):

    status: Label
    token: Entry
    button: Button
    host: Entry

    def login(self, ev = None) -> None:
        if (token := self.token.text) and (host := self.host.text):
            self.status.text = "Connecting..."
            self.button.disabled = True
            client = KXPageClient(url=host, password=token)

            def check_response(response: StorageInfo):
                self.button.disabled = False
                if response["size"] < 0:
                    self.status.text = "Wrong token!"
                else:
                    ftk.mount_component(self.window, Main, Props(client, response))
                    self.destroy()
            
            def exception(e: Exception):
                self.button.disabled = False
                text = str(e)
                self.status.text = text[:200] + '...' if len(text) > 200 else text

            ftk.promise(client.get_storage_info, check_response, exception)
        else:
            self.status.text = "Empty token or host!"

    def on_mount(self):
        self._rt_bind_id = self.window.bind(
            EventSpec(event="KeyPress", key="Return"), self.login
        )

    def on_destroy(self):
        self.window.unbind(
            EventSpec(event="KeyPress", key="Return"), self._rt_bind_id
        )

    def struct(self):
        return Frame(tags="container").add(
            Label(tags="title", text="KXPage Console"),
            Label(tags="line"),
            Frame(tags="login").add(
                Frame(tags="input in").add(
                    Label(text=" Host: "),
                    Entry(tags="et", ref="host", text="http://localhost:8000/api/v1")
                ),
                Frame(tags="input in").add(
                    Label(text="Token: "),
                    Entry(tags="et", ref="token", style={"input_mask": "*"})
                ),
                Label(tags="status in", text="Waiting...", ref="status"),
                Button(tags="in", text="Login", on_click=self.login, ref="button", style={"font_size": 20})
            ),
            Label(tags="version", text=f"Version {VERSION}")
        )

    def styles(self) -> list[Style]:
        return [
            theme.on(
                "button", "checkbutton", "combobox", "entry", "label", "text",
                "frame"
            ),
            {
                "_selector": ".container",
            
                "left": 0.3,
                "top": 0.1,
                "width": 0.4,
                "height": 0.8,
            },
            {
                "_selector": ".line",
                "left": 0.005,
                "top": 0.25,
                "width": 0.99,
                "height": 0.005
            },
            {
                "_selector": ".title",

                "font_size": 40,
                "left": 0.05,
                "top": 0.1,
                "width": 0.9,
                "height": 0.1,

                "font_weight": "bold"
            },
            {
                "_selector": ".login",

                "left": 0.0,
                "width": 1.0,
                "top": 0.25,
                "height": 0.6,

                "display": "pack",

                "padding_top": 50,

                "pack_direction": "column",
                "spread_items": False
            },
            {
                "_selector": ".version",
                
                "left": 0.2,
                "width": 0.6,
                "height": 0.1,
                "top": 0.87,

                "font_size": 15
            },
            {
                "_selector": ".input",

                "display": "pack",
                "pack_direction": "row",
                "border_style": "flat"
            },
            {
                "_selector": ".in",
                "margin": (5, 10),
            },
            {
                "_selector": ".status",

                "font_size": 15,
                "text_wrap": 400,
            },
            {
                "_selector": ".et",

                "font_size": 20,
                "input_width": 25
            }
        ]
