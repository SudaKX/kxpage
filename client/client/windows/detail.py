
from fasttk import *
from typing import Callable

from ..config import theme
from ..network import EventSpec as KXEvent


class EntryInput(Component):

    _tip: str
    _desc: str
    _readonly: bool
    _default: str

    et: Entry

    def setup(
        self,
        desc: str,
        tip: str,
        default: str = None,
        readonly: bool = False
    ):
        self._desc = desc
        self._tip = tip
        self._readonly = readonly
        self._default = default
    
    def on_mount(self):
        pass

    def struct(self):
        return Frame(
            style={
                "display": "grid",
                "border_style": "flat",
                "margin": 10,
                "row_weight": "0 0, 1 1",
                "column_weight": "0 0, 1 1"
            }
        ).add(
            Label(
                text=self._tip,
                style={
                    "font_size": 18,
                    "margin_left": 10,
                    "grid": "0, 0",
                    "stick": "horizontal",
                    "compound_position": "left",
                    "text_width": 10
                }
            ),
            Entry(
                disabled=self._readonly, text=self._default, ref="et",
                style={
                    "grid": "0, 1",
                    "font_size": 18,
                    "stick": "horizontal",
                    "text_align": "left"
                }
            ),
            Label(
                text=self._desc,
                style={
                    "font_size": 15,
                    "grid": "1, 0-1",
                    "stick": "all",
                    "compound_position": "top_left",
                    "padding": (5, 10)
                }
            )
        )

    def styles(self):
        return [
            theme.on(
                "button", "entry", "label", "scrollbar", "text", "frame"
            )
        ]

    def get_text(self) -> str:
        return self.et.text

class TextInput(Component):

    _grid: str
    _name: str
    _default: str

    text_input: Text

    def setup(self, grid: str, name: str, default: str):
        self._grid = grid
        self._name = name
        self._default = default
    
    def on_mount(self):
        self.text_input.text = self._default

    def struct(self):
        return Frame(
            style={
                "grid": self._grid,
                "stick": "all",
                "display": "grid",
                "column_weight": "0 1, 1 0",
                "row_weight": "0 0, 1 1",
                "margin": 15
            }
        ).add(
            Label(
                text=self._name,
                style={
                    "grid": "0, 0-1", "stick": "horizontal",
                    "compound_position": "left"
                }
            ),
            Text(
                style={
                    "grid": "1, 0", "stick": "all",
                    "text_wrap": "word"
                },
                ref="text_input", scrollbar_y="_sb"
            ),
            Scrollbar(ref="_sb", style={
                "grid": "1, 1", "stick": "vertical",
                "indicator_size": 15
            })
        )
    
    def styles(self):
        return [
            theme.on("label", "text", "frame", "scrollbar")
        ]
    
    def get_text(self) -> str:
        return self.text_input.text


class DetailWindow(Component):
    
    _main_cb: Callable[[bool, KXEvent], None]
    _create_mode: bool
    _event: KXEvent
    _instruction: str
    _uuid: str
    _confirm: bool

    confirm_button: Button
    cancel_button: Button

    title_input: EntryInput
    time_input: EntryInput
    hash_input: EntryInput
    href_input: TextInput
    desc_input: TextInput

    def setup(self, edit_mode = False, cb = None, data: KXEvent = {}):
        self._confirm = False
        self._main_cb = cb
        self._create_mode = not edit_mode
        self._event = data.copy() or {
            "time": "2024/5/1",
            "description": "",
            "href": "",
            "image": "",
            "title": "",
            "uuid": "114514-1919810-55558-777777"
        }
        self._uuid = self._event["uuid"]
        self._instruction = "新建事件" if self._create_mode else f"编辑事件：{self._uuid}"
    
    def _gather(self) -> None:
        self._event["href"] = self.href_input.get_text()
        self._event["description"] = self.desc_input.get_text()
        self._event["image"] = self.hash_input.get_text()
        self._event["title"] = self.title_input.get_text()
        self._event["time"] = self.time_input.get_text()

    def on_destroy(self):
        self._main_cb(self._confirm, self._event)

    def cancel(self) -> None:
        self.window.destroy()

    def confirm(self) -> None:
        self._gather()
        self._confirm = True
        self.window.destroy()

    def struct(self):
        return Frame(
            style={
                "display": "grid",
                "width": 1.0,
                "height": 1.0,
                "border_style": "flat",
                "column_weight": "0-1 1",
                "row_weight": "0 0, 1 2, 2 1, 3 0"
            }
        ).add(
            Label(
                text=self._instruction,
                style={
                    "grid": "0, 0-1", "compound_position": "left",
                    "stick": "all", "font_size": 30, "padding": 10
                }
            ),
            Frame(style={
                "grid": "1, 0",
                "border_style": "flat",
                "stick": "all",
                "display": "pack",
                "pack_direction": "column",
                "align_items": "stretch",
                "spread_items": True
            }).add(
                EntryInput(props=Props(
                    "事件的唯一标识符，自动生成，不可被更改。",
                    "事件UUID：", self._uuid, True
                )),
                EntryInput(props=Props(
                    "事件的标题，将会显示在前端列表中。", 
                    "标题：", self._event["title"]
                ), ref="title_input"),
                EntryInput(props=Props(
                    "事件的时间，将会显示在前端列表中。格式：yyyy/mm/dd", 
                    "时间：", self._event["time"]
                ), ref="time_input"),
                EntryInput(props=Props(
                    "事件的相关图片，请先在主界面上传，后将hash名黏贴到此处。", 
                    "图片Hash：", self._event["image"]
                ), ref="hash_input"),
            ),
            Frame(style={
                "grid": "1-2, 1",
                "stick": "all",
                "display": "grid",
                "row_weight": "0-1 1, 2 0",
                "column_weight": "0 1",
                "border_style": "flat",
                "padding_right": 10
            }).add(
                TextInput(
                    props=Props("0, 0", "外链：", self._event["href"]),
                    ref="href_input"
                ),
                TextInput(
                    props=Props("1, 0", "事件描述：", self._event["description"]),
                    ref="desc_input"
                )
            ),
            Frame(style={
                "grid": "2, 0",
                "display": "grid",
                "stick": "all",
                "column_weight": "0-1 1",
                "row_weight": "0 1",
                "border_style": "flat"
            }).add(
                Button(
                    text="确定",
                    style={
                        "grid": "0, 0", "stick": "right",
                        "font_size": 22,
                        "margin": 10
                    },
                    ref="confirm_button",
                    on_click=self.confirm
                ),
                Button(
                    text="取消",
                    style={
                        "grid": "0, 1", "stick": "left",
                        "font_size": 22,
                        "margin": 10
                    },
                    ref="cancel_button",
                    on_click=self.cancel
                )
            )
        )
    
    def styles(self):
        return [
            theme.on("frame", "label", "button")
        ]

