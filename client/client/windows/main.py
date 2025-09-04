
import io
from datetime import datetime
from uuid import uuid4 as random_uuid
from tkinter import filedialog, messagebox

from fasttk import *
from PIL import Image, ImageTk

from .detail import DetailWindow
from ..network import KXPageClient, StorageInfo, EventSpec as KXEvent, StateResponse
from ..config import theme, WINDOW_SIZE

IMAGE_FORMAT = ("JPEG", "PNG", "GIF", "BMP", "WEBP")

class Main(Component):

    _client: KXPageClient
    _events: dict[str, KXEvent]
    _table_items: dict[str, TreeviewItem]
    _current_time: str | None
    _storage_items: dict[str, TreeviewItem]
    _current_hash: str
    _current_image: bytes

    status_bar: Label
    st_display: Label
    refresh_button: Button
    time_label: Label
    event_fetch_button: Button
    table: Treeview

    image_display: Label
    desc_text: Text
    href_text: Text
    download_button: Button
    save_image_button: Button
    delete_image_button: Button
    find_image_button: Button
    event_refresh_button: Button
    image_select_display: Entry

    create_event_button: Button
    edit_event_button: Button
    remove_event_button: Button

    storage_list: Treeview

    def setup(
        self,
        client: KXPageClient = None,
        response: StorageInfo = None
    ):
        self._client = client or KXPageClient()
        self._init_storage = response or {"size": 0, "count": 0, "files": []}

    def update_storage(self) -> None:

        def cb(response: StorageInfo):
            self.status_bar.text = "储存信息更新完毕。"
            self.refresh_button.disabled = False
            self.delete_image_button.disabled = False
            self.st_display.text = \
f"""总大小：{response['size'] / 1048576:.2f} MB
图片数量：{response['count']} 张"""
            for item in self._storage_items.values():
                item.delete()
            self._storage_items.clear()
            for item in response["files"]:
                self._storage_items[item] = self.storage_list.insert(values=(item, ))

        def exception(e: Exception) -> None:
            self.refresh_button.disabled = False
            self.delete_image_button.disabled = False
            self.status_bar.text = f"更新储存信息时出错：{e.__class__.__name__}，详见控制台。"

        self.refresh_button.disabled = True
        self.delete_image_button.disabled = True
        self.status_bar.text = "正在更新储存信息..."
        ftk.promise(self._client.get_storage_info, cb, exception)

    def update_events(self) -> None:

        def cb(response: list[KXEvent]):
            self.event_fetch_button.disabled = False
            for event in response:
                uuid = event["uuid"]
                if uuid not in self._events:
                    self._table_items[uuid] = self.table.insert(
                        name=uuid, values=(event["time"], event["title"])
                    )
                    self._events[uuid] = event
            if response:
                self.time_label.text = f"截至 {response[-1]['time']}"
                self._current_time = response[-1]['time']
            self.status_bar.text = f"事件更新完毕，新增条数：{len(response)}。"

        def on_exception(e: Exception):
            self.event_fetch_button.disabled = False
            self.status_bar.text = f"获取事件时出错：{e.__class__.__name__}，详见控制台。"
            raise e

        self.event_fetch_button.disabled = True
        self.status_bar.text = "更新事件中..."
        ftk.promise(
            self._client.fetch_event, cb, on_exception,
            args=(self._current_time ,)
        )

    def clear_event_select(self) -> None:
        self.save_image_button.disabled = True
        self.find_image_button.disabled = True
        self.download_button.disabled = True
        self.image_display.text = ""
        self.href_text.text = ""
        self.desc_text.text = ""
        self.edit_event_button.disabled = True
        self.remove_event_button.disabled = True

    def update_selection(self, items: list[TreeviewItem]) -> None:
        if not items:
            self.clear_event_select()
            return None
        item = items[0]
        self.status_bar.text = f"当前选中：事件{item.name}。"
        event = self._events.get(item.name)
        self.href_text.text = event["href"] or "No href."
        self.desc_text.text = event["description"] or "No description."

        self.image_display.image = None
        self.save_image_button.disabled = True
        self.find_image_button.disabled = True
        self.download_button.disabled = True
        self.edit_event_button.disabled = False
        self.remove_event_button.disabled = False
        if image_hash := event["image"]:
            self.find_image_button.disabled = False
            self.download_button.disabled = False
            self.image_display.text = image_hash
            self._current_hash = image_hash
        else:
            self.image_display.text = "No image."

    def fetch_save_image(self) -> None:
        raw = self._client.fetch_image(self._current_hash)
        bio = io.BytesIO(raw)
        image = Image.open(bio, formats=IMAGE_FORMAT)
        height, width = (
            self.image_display.widget.winfo_height(),
            self.image_display.widget.winfo_width()
        )
        ratio = min(height / image.height, width / image.width)
        height = int(ratio * image.height)
        width = int(ratio * image.width)
        self._current_image = raw

        tk_image = ImageTk.PhotoImage(image.resize((width, height)))
        self.image_display.image = tk_image

    def download_image(self) -> None:

        def cb(_) -> None:
            self.save_image_button.disabled = False
            self.image_display.text = ""
            self.status_bar.text = f"图片{self._current_hash}下载完毕，已展示缩略图。"

        def exception(e: Exception):
            self.status_bar.text = f"下载图片出错：{e.__class__.__name__}，详见控制台。"
            self.download_button.disabled = False
            raise e

        self.status_bar.text = f"下载对应图片：{self._current_hash}。"
        self.download_button.disabled = True
        ftk.promise(self.fetch_save_image, cb, exception)

    def save_image(self) -> None:
        _, ext = self._current_hash.split('.')
        self.status_bar.text = "发起保存文件对话框..."
        writer = filedialog.asksaveasfile(
            "wb",
            defaultextension=ext, initialdir="./", title="保存图片",
            initialfile=self._current_hash,
            filetypes=((f"{ext.upper()}格式图片", f"*.{ext}"),)
        )
        if writer:
            writer.write(self._current_image)
            writer.close()
            self.status_bar.text = f"图片已保存至：{writer.name}。"
        else:
            self.status_bar.text = "保存已取消。"
    
    def update_image_selection(self, items: list[TreeviewItem]) -> None:
        if not items:
            self.delete_image_button.disabled = True
            return None
        self.delete_image_button.disabled = False
        item = items[0]
        self.status_bar.text = f"当前选中：图片{item['filename']}。"
        self.image_select_display.text = item["filename"]

    def storage_delete_current(self) -> None:
        name = self.storage_list.selection[0]["filename"]
        self.status_bar.text = "发起确认删除对话框..."
        confirm = messagebox.askokcancel(
            "确认删除",
            f"确认删除图片“{name}”吗？\n此操作不会检查事件对图片的依赖。",
            icon=messagebox.WARNING
        )
        if not confirm:
            self.status_bar.text = "删除操作已取消。"
            return None
        
        def task() -> None:
            return self._client.delete_image(name)
        
        def cp(success: StateResponse) -> None:
            if (message := success["message"]) == "success":
                self.status_bar.text = f"删除图片{name}成功。"
                self.update_storage()
            else:
                self.status_bar.text = f"删除图片{name}失败，{message}。"
                self.refresh_button.disabled = False

        def ex(e: Exception) -> None:
            self.status_bar.text = f"删除图片时出错：{e.__class__.__name__}，详见控制台。"
            self.delete_image_button.disabled = False
            raise e
        
        self.delete_image_button.disabled = True
        self.status_bar.text = f"正在删除图片：{name}..."
        ftk.promise(task, cp, ex)

    def find_current_image(self) -> None:
        target_item = self._storage_items.get(self._current_hash, None)
        if target_item:
            self.storage_list.selection = [target_item]
        else:
            self.status_bar.text = f"在储存中未找到{self._current_hash}，请检查储存列表是否更新或记录是否合法。"

    def refresh_all(self) -> None:
        
        def task() -> None:
            stop_before = int(
                datetime.strptime(self._current_time, "%Y/%m/%d").timestamp()
            )
            updated_events = []
            timestamp = 0
            time_before = None
            while timestamp < stop_before:
                events = self._client.fetch_event(time_before)
                updated_events.extend(events)
                if events:
                    time_before = events[-1]["time"]
                    timestamp = int(
                        datetime.strptime(time_before, "%Y/%m/%d").timestamp()
                    )
                else:
                    break
            return updated_events

        def cb(events: list[KXEvent]) -> None:
            self.event_refresh_button.disabled = False
            self.table.disabled = False
            self.status_bar.text = f"刷新事件成功。"
            new_map = {}
            for item in self._table_items.values():
                item.delete()
            self._table_items.clear()
            for event in events:
                uuid = event["uuid"]
                new_map[uuid] = event
                self._table_items[uuid] = self.table.insert(
                    name=uuid, values=(event["time"], event["title"])
                )
            self._events = new_map
            self.time_label.text = f"截至 {events[-1]['time']}"

        def ex(e: Exception) -> None:
            self.event_refresh_button.disabled = False
            self.table.disabled = False
            self.status_bar.text = f"刷新事件时出错：{e.__class__.__name__}，详情见控制台。"
            raise e

        if not len(self._events):
            self.update_events()
            return None

        self.event_refresh_button.disabled = True
        self.table.selection = []
        self.clear_event_select()
        self.table.disabled = True
        self.status_bar.text = f"刷新事件中..."
        ftk.promise(task, cb, ex)

    def upload_image(self) -> None:
        self.status_bar.text = "发起文件选择对话框..."
        path = filedialog.askopenfilename(title="选择文件", initialdir="./")
        if not path:
            self.status_bar.text = "上传操作已取消。"
            return None
        
        def cb(response: StateResponse) -> None:
            image_name = response["message"]
            self.status_bar.text = f"文件已上传，访问名称：{image_name}。"
            if not (item := self._storage_items.get(image_name, None)):
                item = self.storage_list.insert(name="_", values=(image_name, ))
                self._storage_items[image_name] = item
            self.storage_list.selection = [item]

        def ex(e: Exception) -> None:
            self.status_bar.text = f"上传图片时出错：{e.__class__.__name__}，详见控制台。"
            raise e

        self.status_bar.text = f"正在上传{path}..."
        ftk.promise(self._client.upload_image, cb, ex, args=(path, ))

    def copy_image_name(self) -> None:
        filename = self.image_select_display.text
        self.window.clipboard_clear()
        self.window.clipboard_append(filename)
        self.status_bar.text = f"已复制文件名：{filename}。"

    def detail_create_cb(self, action: bool, data: KXEvent) -> None:
        self.window.wm_deiconify()
        if not action:
            self.status_bar.text = "已取消创建事件。"
            return None
        
        def cb(response: StateResponse):
            self.create_event_button.disabled = False
            self.refresh_all()

        def ex(e: Exception):
            self.create_event_button.disabled = False
            self.status_bar.text = f"创建事件时出错：{e.__class__.__name__}，详见控制台。"
            raise e

        self.status_bar.text = "创建事件中..."
        self.create_event_button.disabled = True
        ftk.promise(self._client.append_event, cb, ex, args=([data], ))

    def detail_edit_cb(self, action: bool, data: KXEvent) -> None:
        self.window.wm_deiconify()
        if not action:
            self.status_bar.text = "已取消修改事件。"
            return None
        
        def cb(response: StateResponse):
            self.edit_event_button.disabled = False
            self.refresh_all()

        def ex(e: Exception):
            self.edit_event_button.disabled = False
            self.status_bar.text = f"修改事件时出错：{e.__class__.__name__}，详见控制台。"
            raise e

        self.status_bar.text = "修改事件中..."
        self.edit_event_button.disabled = True
        ftk.promise(
            self._client.update_event, cb, ex,
            args=(data["uuid"], ),
            kwargs={
                "event_time": datetime.strptime(data["time"], "%Y/%m/%d"),
                "event_title": data["title"],
                "event_href": data["href"],
                "event_description": data["description"],
                "image_hash": data["image"]
            }
        )

    def raise_detail_window(self, use_current: bool, cb) -> None:
        if use_current:
            data = self._events[self.table.selection[0].name]
        else:
            data: KXEvent = {
                "time": datetime.now().strftime("%Y/%m/%d"),
                "description": "",
                "href": "",
                "image": "",
                "title": "",
                "uuid": str(random_uuid())
            }
        ftk.create_window(
            DetailWindow,
            title="事件详情",
            size=WINDOW_SIZE,
            props=Props(use_current, cb, data)
        )
        self.window.wm_withdraw()

    def remove_event(self) -> None:
        
        uuid = self.table.selection[0].name
        title = self.table.selection[0]["title"]

        self.status_bar.text = "发起确认对话框..."
        confirm = messagebox.askokcancel(
            "确认删除",
            f"确认删除事件：\"{title}\"({uuid}) 吗？",
            icon=messagebox.WARNING
        )
        if not confirm:
            self.status_bar.text = "已取消删除事件。"
            return None

        def cb(response: StateResponse):
            self.status_bar.text = f"已删除事件：\"{title}\"({uuid})。"
            self.remove_event_button.disabled = False
            self.refresh_all()
    
        def ex(e: Exception):
            self.status_bar.text = f"删除事件时出错：{e.__class__.__name__}，详见控制台。"
            self.remove_event_button.disabled = False
            raise e

        self.status_bar.text = "正在删除事件..."
        self.remove_event_button.disabled = True
        ftk.promise(self._client.delete_event, cb, ex, args=(uuid, ))


    
    def on_mount(self):
        self._table_items = {}
        self._events = {}
        self._storage_items = {}
        self._current_time = None
        response = self._init_storage
        self.st_display.text = \
f"""总大小：{response['size'] / 1048576:.2f} MB
图片数量：{response['count']} 张"""
        for file in response["files"]:
            self._storage_items[file] = self.storage_list.insert(values=(file, ))
        del self._init_storage

    def struct(self):
        return Frame(tags="container").add(
            Frame(tags="main").add(
                Treeview(
                    tags="tv", ref="table", scrollbar_y="_tv_y_scb",
                    on_select=self.update_selection
                ).set_columns(
                    TreeviewColumn(),
                    TreeviewColumn(
                        "time", heading="日期", item_anchor="left", heading_anchor="left"
                    ),
                    TreeviewColumn(
                        "title", heading="标题", item_anchor="left", heading_anchor="left"
                    )
                ),
                Scrollbar(ref="_tv_y_scb", tags="tvb")
            ),
            Frame(tags="bottom").add(
                Frame(tags="sub_contain", style={"grid": "0, 0"}).add(
                    Label(text="外链:", style={"compound_position": "left"}),
                    Frame(tags="sub_text_wrap").add(
                        Text(
                            tags="sub_contain_text", scrollbar_y="_stw_1",
                            ref="href_text", disabled=True
                        ),
                        Scrollbar(tags="sub_contain_sb", ref="_stw_1")
                    )
                ),
                Frame(tags="sub_contain", style={"grid": "0, 1"}).add(
                    Label(text="简要描述:", style={"compound_position": "left"}),
                    Frame(tags="sub_text_wrap").add(
                        Text(
                            tags="sub_contain_text", scrollbar_y="_stw_2",
                            ref="desc_text", disabled=True
                        ),
                        Scrollbar(tags="sub_contain_sb", ref="_stw_2")
                    )
                ),
                Frame(tags="image_dl").add(
                    Label(text="图片:", style={
                        "compound_position": "left",
                        "grid": "0, 0-1",
                        "stick": "horizontal"
                    }),
                    Frame(style={
                        "grid": "1, 0-1", "stick": "all"
                    }).add(
                        Label(text="......", ref="image_display", style={
                            "width": 1.0,
                            "height": 1.0,
                            "font_size": 15,
                            "text_wrap": 200,
                            "compound_mode": "center"
                        }),
                    ),
                    Button(
                        text="Download",
                        style={
                            "grid": "2, 0", "font_size": 15, "stick": "right",
                            "margin_right": 10
                        },
                        ref="download_button", disabled=True, on_click=self.download_image
                    ),
                    Button(
                        text="Save",
                        style={
                            "grid": "2, 1", "font_size": 15,
                            "stick": "left", "margin_left": 10
                        },
                        ref="save_image_button", disabled=True, on_click=self.save_image
                    )
                )
            ),
            Frame(tags="right").add(
                Label(text="截至：--/--/--", ref="time_label"),
                Button(
                    text="获取更多事件", tags="in_right",
                    on_click=self.update_events, ref="event_fetch_button"
                ),
                Button(
                    text="刷新已有事件", tags="in_right",
                    on_click=self.refresh_all, ref="event_refresh_button"
                ),
                Label(text="事件操作"),
                Button(
                    tags="in_right", text="创建事件",
                    on_click=lambda: self.raise_detail_window(False, self.detail_create_cb),
                    ref="create_event_button"
                ),
                Button(
                    tags="in_right", text="修改事件", disabled=True,
                    on_click=lambda: self.raise_detail_window(True, self.detail_edit_cb),
                    ref="edit_event_button"
                ),
                Button(
                    tags="in_right", text="删除事件", disabled=True,
                    on_click=self.remove_event,
                    ref="remove_event_button"
                ),
                Button(
                    tags="in_right", text="同步左侧栏",
                    ref="find_image_button", on_click=self.find_current_image,
                    disabled=True
                )
            ),
            Frame(tags="storage").add(
                Label(
                    tags="st_status", text="储存信息",
                    style={"font_size": 20, "grid": "0, 0-1", "stick": "horizontal"}
                ),
                Label(ref="st_display", style={"grid": "1, 0-1", "stick": "all"}),
                Button(
                    text="刷新", on_click=self.update_storage,
                    style={
                        "font_size": 15, "grid": "5, 1",
                        "stick": "horizontal", "margin": 2
                    },
                    ref="refresh_button"
                ),
                Button(
                    text="删除选中",
                    style={
                        "font_size": 15, "grid": "5, 0",
                        "stick": "horizontal", "margin": 2
                    },
                    ref="delete_image_button", disabled=True,
                    on_click=self.storage_delete_current
                ),
                Frame(
                    style={
                        "grid": "2, 0-1",
                        "display": "grid",
                        "row_weight": "0 1",
                        "column_weight": "0 1, 1 1",
                        "stick": "all",
                        "margin": (5, 0)
                    }
                ).add(
                    Treeview(
                        scrollbar_y="_sb_st_tv_y",
                        style={
                            "stick": "all",
                            "treeview_show": "columns",
                            "heading_font_size": 18, "font_size": 15,
                            "treeview_row_height": 18
                        }, ref="storage_list", on_select=self.update_image_selection
                    ).set_columns(
                        TreeviewColumn(),
                        TreeviewColumn(
                            id="filename", heading="文件名",
                            heading_anchor="left", item_anchor="left"
                        ),
                    ),
                    Scrollbar(ref="_sb_st_tv_y", style={"grid": "0, 1", "stick": "vertical"})
                ),
                Entry(
                    ref="image_select_display", readonly=True,
                    style={
                        "grid": "3, 0-1", "margin": 2,
                        "font_size": 15, "stick": "horizontal"
                    }
                ),
                Button(
                    text="上传图片", ref="upload_image_button",
                    style={
                        "grid": "4, 0", "stick": "horizontal",
                        "font_size": 15, "margin": 2
                    },
                    on_click=self.upload_image
                ),
                Button(
                    text="复制文件名",
                    style={
                        "grid": "4, 1", "stick": "horizontal",
                        "font_size": 15, "margin": 2
                    },
                    on_click=self.copy_image_name
                )
            ),
            Frame(tags="status_bar").add(
                Label(text="空闲...", style={
                    "font_size": 15,
                    "width": 1.0,
                    "height": 1.0,
                    "compound_position": "left",
                    "padding": (0, 5),
                }, ref="status_bar", tags="status_label")
            )
        )
    
    def styles(self) -> list[Style]:
        return [
            theme.on(
                "button", "checkbutton", "combobox", "entry", "frame",
                "label", "text", "treeview", "scrollbar"
            ),
            {
                "_selector": ".container",

                "width": 1.0,
                "height": 1.0,
                "left": 0.0,
                "top": 0.0,

                "display": "grid",

                "column_weight": "0 0, 1 1, 2 0",
                "row_weight": "0 1, 1 0, 2 0",
                "column_minsize": "0 200, 2 200",
                "row_minsize": "1 200, 2 20"
            },
            {
                "_selector": ".bottom",
                
                "grid": "1, 1-2",
                "stick": "all",

                "display": "grid",
                "column_weight": "0-1 2, 2 1",
                "row_weight": "0 1"
            },
            {
                "_selector": ".right",
                
                "grid": "0, 2",
                "stick": "all",
                "display": "pack",
                "pack_direction": "column",

                "padding": (20, 0)
            },
            {
                "_selector": ".in_right",
                "margin": 10,
                "font_size": 15,
                "padding": (0, 10)
            },
            {
                "_selector": ".main",

                "grid": "0, 1",
                "stick": "all",
                "padding": 15,

                "display": "grid",
                "column_weight": "0 1, 1 0",
                "column_minsize": "1 15",
                "row_weight": "0 1"
            },
            {
                "_selector": ".tv",

                "grid": "0, 0",
                "stick": "all",
                "heading_font_size": 18,
                "font_size": 15,
                "treeview_row_height": 22,
                "treeview_show": "columns"
            },
            {
                "_selector": ".tvb",

                "grid": "0, 1",
                "stick": "vertical",
                "indicator_size": 15
            },
            {
                "_selector": ".storage",

                "grid": "0-1, 0",
                "stick": "all",

                "padding": 10,
                "display": "grid",
                "column_weight": "0 1, 1 1",
                "row_weight": "0-1 0, 2 1, 3-5 0"
            },
            {
                "_selector": ".st_status",

                "text_wrap": 200,

                "font_size": 15,
                "margin": 10
            },
            {
                "_selector": ".image_dl",

                "grid": "0, 2",
                "stick": "all",
                "padding": 10,

                "display": "grid",
                "column_weight": "0 1, 1 1",
                "row_weight": "0 0, 1 1, 2 0"
            },
            {
                "_selector": ".sub_contain",

                "display": "pack",
                "pack_direction": "column",
                "align_items": "stretch",
                "stick": "all",
                "padding": 10
            },
            {
                "_selector": ".sub_text_wrap",

                "display": "grid",
                "row_weight": "0 1",
                "column_weight": "0 1, 1 0",
                "column_minsize": "1 15"
            },
            {
                "_selector": ".sub_contain_text",
                
                "grid": "0, 0",
                "stick": "all",
                "font_size": 15,
                "text_width": 5
            },
            {
                "_selector": ".sub_contain_sb",

                "grid": "0, 1",
                "stick": "vertical",
                "indicator_size": 15,
                "text_wrap": "word"
            },
            {
                "_selector": ".status_bar",

                "grid": "2, 0-2",
                "stick": "all",
                "border_color": theme.hex_l1
            },
            {
                "_selector": ".status_label",
                
                "foreground": theme.hex_l1,
                "background": theme.hex_d0
            },
            {
                "_selector": ".st_frame",

                "row_weight": "0 0, 1 1, 2 0",
                "column_weight": "0 1"
            }
        ]
