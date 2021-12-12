import math
import random
import tkinter as tk
from tkinter import Canvas, ttk, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile
from tkinter.constants import CURRENT
from PIL import Image, ImageTk, ImageGrab

root = tk.Tk()


class Frames:
    def __init__(self):
        self.color_selected = "white"
        self.color_selected_outline = "black"
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.canvasOptions = {"bg": "white"}
        self.canvas = tk.Canvas(self.frame, self.canvasOptions)
        self.canvas.pack(fill="both", expand=True)


class Sketch1(Frames):
    def __init__(self):
        self.initials()
        self.group_stack = []
        super().__init__()

    def initials(self):
        self.x0 = None
        self.y0 = None
        self.lines = []
        self.layers = []
        self.lines2 = []
        self.polygon_points = []
        self.copyStack = None
        self.freeLine = None
        self.polycheck = None
        self.line = None
        self.rectangle = None
        self.circle = None
        self.polygon = None
        self.cut_object = False

    # drawing types
    def draw_free_hand(self):

        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.free_line)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_stright_line(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.stright_line)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_rectangle(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.create_rectangles)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_square(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.create_square)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_ellipse(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.creat_ellipse)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_circle(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.creat_circle)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    def draw_polygon(self):
        self.canvas.bind("<Button-1>", self.get_pos)
        self.canvas.bind("<Button-3>", self.get_pos_for_plolly)
        self.canvas.bind("<B1-Motion>", self.creat_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.saveline)

    # drawing methods
    def get_pos(self, event):
        self.x0 = event.x
        self.y0 = event.y

    def free_line(self, event):
        self.freeLine = self.canvas.create_line(
            self.x0,
            self.y0,
            event.x,
            event.y,
            fill=self.color_selected_outline,
            tags=["free_line", "event_binder"],
        )
        self.get_pos(event)

    def stright_line(self, event):
        # stright line
        if self.line:
            self.lines.append(self.line)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(self.line)
        self.line = self.canvas.create_line(
            self.x0,
            self.y0,
            event.x,
            event.y,
            fill=self.color_selected_outline,
            tags=["line", "event_binder"],
        )

    def create_rectangles(self, event):
        # rectangle
        if self.rectangle:
            self.lines.append(self.rectangle)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(id)
        self.rectangle = self.canvas.create_rectangle(
            self.x0,
            self.y0,
            event.x,
            event.y,
            fill=self.color_selected,
            outline=self.color_selected_outline,
            tags=["rectangle", "event_binder"],
        )

    def create_square(self, event):
        # rectangle
        if self.rectangle:
            self.lines.append(self.rectangle)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(id)
        d = math.sqrt(((self.x0 - event.x) ** 2) + ((self.y0 - event.y) ** 2))
        self.rectangle = self.canvas.create_rectangle(
            self.x0,
            self.y0,
            self.x0 + d,
            self.y0 + d,
            fill=self.color_selected,
            outline=self.color_selected_outline,
            tags=["square", "event_binder"],
        )

    def creat_ellipse(self, event):
        if self.circle:
            self.lines.append(self.circle)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(id)
        r = math.sqrt(((self.x0 - event.x) ** 2) + ((self.y0 - event.y) ** 2)) / 2
        self.circle = self.canvas.create_oval(
            (self.x0 - r),
            (self.y0 - r),
            (event.x + r),
            (event.y + r),
            fill=self.color_selected,
            outline=self.color_selected_outline,
            tags=["ellipse", "event_binder"],
        )

    def creat_circle(self, event):
        if self.circle:
            self.lines.append(self.circle)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(id)
        r = math.sqrt(((self.x0 - event.x) ** 2) + ((self.y0 - event.y) ** 2))
        self.circle = self.canvas.create_oval(
            (self.x0),
            (self.y0),
            (self.x0 + r),
            (self.y0 + r),
            fill=self.color_selected,
            outline=self.color_selected_outline,
            tags=["circle", "event_binder"],
        )

    def creat_polygon(self, event):
        if self.polygon:
            self.lines.append(self.polygon)
            for id in self.lines:
                if id in self.layers:
                    pass
                else:
                    self.canvas.delete(id)
        self.polygon = self.canvas.create_line(
            self.x0,
            self.y0,
            event.x,
            event.y,
            fill=self.color_selected_outline,
            width=1,
            tags=["dummy"],
        )

    def get_pos_for_plolly(self, event):

        if len(self.polygon_points) == 0:
            self.polygon_points.append(self.x0)
            self.polygon_points.append(self.y0)
        self.polygon_points.append(event.x)
        self.polygon_points.append(event.y)
        self.x0 = event.x
        self.y0 = event.y
        self.polygon = self.canvas.create_polygon(
            self.polygon_points,
            outline="black",
            fill=self.color_selected,
            width=1,
            tags=["polygon", "event_binder"],
        )

    def clear_screen(self):
        self.canvas.delete("all")
        self.initials()

    def saveline(self, event):
        if self.rectangle:
            self.layers.append(self.rectangle)

        if self.line:
            self.canvas.itemconfig(self.line, width=5)
            self.layers.append(self.line)

        if self.circle:
            self.layers.append(self.circle)

        if self.polygon:
            self.canvas.delete("dummy")
            self.polygon = self.canvas.create_polygon(
                self.polygon_points,
                outline=self.color_selected_outline,
                fill=self.color_selected,
                width=1,
                tags=["polygon", "event_binder"],
            )
            self.initials()
            self.layers.append(self.polygon)

        if self.freeLine:
            ids = self.canvas.find_withtag("free_line")
            unique_tag = f"tag_{self.x0}{self.y0}"
            for id in ids:
                if len(self.canvas.gettags(id)) == 2:
                    self.canvas.itemconfig(
                        id, tags=[unique_tag, "free_line", "event_binder"]
                    )
            self.layers.append(self.freeLine)

        self.lines = []

    def cutObject(self):
        self.unbindEvents()
        self.canvas.tag_bind("event_binder", "<Button-1>", self.cutting)

    def copyObject(self):
        self.unbindEvents()
        self.canvas.tag_bind("event_binder", "<Button-1>", self.copying)

    def pasteObject(self):
        self.unbindEvents()
        self.canvas.bind("<Button-1>", self.pasting)

    def groupObjects(self):
        self.unbindEvents()
        self.canvas.bind("<Button-1>", self.grouping)
        self.canvas.bind("<Button-3>", self.add_in_group)

    def ungroupObjects(self):
        self.unbindEvents()
        self.canvas.bind("<Button-1>", self.ungrouping)

    def copying(self, event):
        id = self.canvas.find_closest(event.x, event.y)
        self.copyStack = id
        print(self.copyStack)

    def pasting(self, event):
        tags = self.canvas.gettags(self.copyStack)
        if "group" in tags:
            self.paste_group(tags[3], event)
            return
        x0 = event.x
        y0 = event.y
        coordinates = self.canvas.coords(self.copyStack)
        type = self.canvas.type(self.copyStack)
        if type == "rectangle":
            fill = self.canvas.itemcget(self.copyStack, "fill")
            outline = self.canvas.itemcget(self.copyStack, "outline")
            x1 = x0 + abs(coordinates[0] - coordinates[2])
            y1 = y0 + abs(coordinates[1] - coordinates[3])
            if self.cut_object:
                fill = self.color_selected
                outline = self.color_selected_outline
            self.rectangle = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=fill, tags=["rectangle", "event_binder"]
            )

        if type == "line":
            tags = self.canvas.gettags(self.copyStack)
            fill = self.canvas.itemcget(self.copyStack, "fill")
            if self.cut_object:
                fill = self.color_selected_outline
            x1 = x0 + abs(coordinates[0] - coordinates[2])
            y1 = y0 + abs(coordinates[1] - coordinates[3])
            if "free_line" in tags:
                ids = self.canvas.find_withtag(tags[0])
                unique_tag = f"tag_{event.x}{event.y}"
                for id in ids:
                    f_line_part_coord = self.canvas.coords(id)
                    self.free_line = self.canvas.create_line(
                        f_line_part_coord[0],
                        f_line_part_coord[1],
                        f_line_part_coord[2],
                        f_line_part_coord[3],
                        fill=fill,
                        tags=[unique_tag, "free_line", "event_binder"],
                    )
                x = event.x - f_line_part_coord[0]
                y = event.y - f_line_part_coord[1]
                self.canvas.move(unique_tag, x, y)
            else:
                self.line = self.canvas.create_line(
                    x0, y0, x1, y1, fill=fill, tags=["line", "event_binder"]
                )

        if type == "oval":
            fill = self.canvas.itemcget(self.copyStack, "fill")
            outline = self.canvas.itemcget(self.copyStack, "outline")
            x1 = x0 + abs(coordinates[0] - coordinates[2])
            y1 = y0 + abs(coordinates[1] - coordinates[3])
            if self.cut_object:
                fill = self.color_selected
                outline = self.color_selected_outline
            self.circle = self.canvas.create_oval(
                x0,
                y0,
                x1,
                y1,
                fill=fill,
                outline=outline,
                tags=["circle", "event_binder"],
            )

        if type == "polygon":
            fill = self.canvas.itemcget(self.copyStack, "fill")
            width = self.canvas.itemcget(self.copyStack, "width")
            outline = self.canvas.itemcget(self.copyStack, "outline")
            if self.cut_object:
                fill = self.color_selected
                outline = self.color_selected_outline
            self.polygon = self.canvas.create_polygon(
                coordinates,
                outline=outline,
                fill=fill,
                width=width,
                tags=["polygon", "event_binder"],
            )
            x = event.x - coordinates[0]
            y = event.y - coordinates[1]
            self.canvas.move(self.polygon, x, y)

        self.saveline(event)

    def paste_group(self, group_id, event):
        ids = self.canvas.find_withtag(group_id)
        group_id = f"group{event.x}{event.y}"
        first_object_coordinates = self.canvas.coords(ids[0])
        for id in ids:
            coordinates = self.canvas.coords(id)
            x0 = event.x + abs(first_object_coordinates[0] - coordinates[0])
            y0 = event.y + abs(first_object_coordinates[1] - coordinates[1])
            type = self.canvas.type(id)
            if type == "rectangle":
                fill = self.canvas.itemcget(id, "fill")
                outline = self.canvas.itemcget(id, "outline")
                x1 = x0 + abs(coordinates[0] - coordinates[2])
                y1 = y0 + abs(coordinates[1] - coordinates[3])
                if self.cut_object:
                    fill = self.color_selected
                    outline = self.color_selected_outline
                self.rectangle = self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill=fill, tags=["rectangle", "event_binder"]
                )

            if type == "line":
                tags = self.canvas.gettags(id)
                fill = self.canvas.itemcget(id, "fill")
                if self.cut_object:
                    fill = self.color_selected_outline
                x1 = x0 + abs(coordinates[0] - coordinates[2])
                y1 = y0 + abs(coordinates[1] - coordinates[3])
                if "free_line" in tags:
                    ids = self.canvas.find_withtag(tags[0])
                    unique_tag = f"tag_{event.x}{event.y}"
                    for id in ids:
                        f_line_part_coord = self.canvas.coords(id)
                        self.free_line = self.canvas.create_line(
                            f_line_part_coord[0],
                            f_line_part_coord[1],
                            f_line_part_coord[2],
                            f_line_part_coord[3],
                            fill=fill,
                            tags=[unique_tag, "free_line", "event_binder"],
                        )
                    x = event.x - f_line_part_coord[0]
                    y = event.y - f_line_part_coord[1]
                    self.canvas.move(unique_tag, x, y)
                else:
                    self.line = self.canvas.create_line(
                        x0, y0, x1, y1, fill=fill, tags=["line", "event_binder"]
                    )

            if type == "oval":
                fill = self.canvas.itemcget(id, "fill")
                outline = self.canvas.itemcget(id, "outline")
                x1 = x0 + abs(coordinates[0] - coordinates[2])
                y1 = y0 + abs(coordinates[1] - coordinates[3])
                if self.cut_object:
                    fill = self.color_selected
                    outline = self.color_selected_outline
                self.circle = self.canvas.create_oval(
                    x0,
                    y0,
                    x1,
                    y1,
                    fill=fill,
                    outline=outline,
                    tags=["circle", "event_binder"],
                )

            if type == "polygon":
                fill = self.canvas.itemcget(id, "fill")
                width = self.canvas.itemcget(id, "width")
                outline = self.canvas.itemcget(id, "outline")
                if self.cut_object:
                    fill = self.color_selected
                    outline = self.color_selected_outline
                self.polygon = self.canvas.create_polygon(
                    coordinates,
                    outline=outline,
                    fill=fill,
                    width=width,
                    tags=["polygon", "event_binder"],
                )
                x = event.x - coordinates[0]
                y = event.y - coordinates[1]
                self.canvas.move(self.polygon, x, y)
            self.canvas.addtag_withtag("group", id)
            self.canvas.addtag_withtag(group_id, id)
            self.saveline(event)

    def cut_group(self, group_id, event):
        ids = self.canvas.find_withtag(group_id)
        group_id = f"group{event.x}{event.y}"
        for id in ids:
            self.copyStack = id
            print(id)
            tags = self.canvas.gettags(id)
            if "free_line" in tags:
                self.canvas.itemconfig(tags[0], fill="white")
            else:
                if "line" in tags:
                    self.canvas.itemconfig(id, fill="white")
                else:
                    self.canvas.itemconfig(id, fill="white")
                    self.canvas.itemconfig(id, outline="white")

    def cutting(self, event):
        self.cut_object = True
        id = self.canvas.find_closest(event.x, event.y)
        self.copyStack = id
        tags = self.canvas.gettags(self.copyStack)
        if "group" in tags:
            self.cut_group(tags[3], event)
            return
        tags = self.canvas.gettags(id)
        if "free_line" in tags:
            self.canvas.itemconfig(tags[0], fill="white")
        else:
            if "line" in tags:
                self.canvas.itemconfig(id, fill="white")
            else:
                self.canvas.itemconfig(id, fill="white")
                self.canvas.itemconfig(id, outline="white")

    def moveObject(self):
        self.unbindEvents()
        self.canvas.tag_bind("event_binder", "<Button-1>", self.add_tags)
        self.canvas.tag_bind("event_binder", "<B1-Motion>", self.moving)
        self.canvas.tag_bind("event_binder", "<ButtonRelease-1>", self.remove_tag)

    def moving(self, event):
        id = self.canvas.find_closest(event.x, event.y)
        cords = self.canvas.coords(id)
        x = event.x - cords[0]
        y = event.y - cords[1]
        tags = self.canvas.gettags(id)
        print(tags)
        if "group" in tags:
            self.canvas.move(tags[3], x, y)
        elif "free_line" in tags:
            self.canvas.move(tags[0], x, y)
        elif "polygon" in tags:
            self.canvas.move("move", x, y)
        else:
            self.canvas.move(id, x, y)

    def add_tags(self, event):
        id = self.canvas.find_withtag(CURRENT)[0]
        tags = self.canvas.gettags(id)
        if "free_line" in tags:
            ids = self.canvas.find_withtag(tags[0])
            for id in ids:
                self.canvas.addtag_withtag("move", id)
        else:
            self.canvas.addtag_withtag("move", id)

    def remove_tag(self, event):
        id = self.canvas.find_withtag(CURRENT)[0]
        self.canvas.dtag(id, "move")
        tags = self.canvas.gettags(id)
        if "free_line" in tags:
            ids = self.canvas.find_withtag(tags[0])
            for id in ids:
                self.canvas.dtag(id, "move")
        else:
            self.canvas.dtag(id, "move")
        print(tags)

    def grouping(self, event):
        id = self.canvas.find_closest(event.x, event.y)
        self.group_stack.append(id)
        print(self.group_stack)

    def ungrouping(self, event):
        id = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(id)
        ids = self.canvas.find_withtag(tags[3])
        for id in ids:
            self.canvas.dtag(id, "group")
            self.canvas.dtag(id, tags[3])

    def add_in_group(self, event):
        group_id = f"group{event.x}{event.y}"
        for id in self.group_stack:
            self.canvas.addtag_withtag("group", id)
            self.canvas.addtag_withtag(group_id, id)
        if event.num == 3:
            self.group_stack = []

    def unbindEvents(self):
        print("unbind")
        self.canvas.tag_unbind("event_binder", "<B1-Motion>")
        self.canvas.tag_unbind("event_binder", "<Button-1>")
        self.canvas.tag_unbind("event_binder", "<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.unbind("<ButtonRelease-1>")

    def save_file(self):
        file = asksaveasfilename(filetypes=[("Portable Network Graphics", "*.png")])
        x = root.winfo_rootx() + 120
        y = root.winfo_rooty()
        x1 = x + self.canvas.winfo_width() - 200
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save(file + ".png")

    def open_file(self):
        img_path = askopenfilename(
            title="Select A File",
            filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")),
        )
        if img_path:
            self.canvas.imageList = (
                []
            )  # To get rid of garbage collector, empty list is added
            img = Image.open(img_path)
            img = img.resize((750, 500), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(img)
            created_image_id = self.canvas.create_image(450, 250, image=image)
            self.canvas.imageList.append(image)


def make_free_line():
    start.draw_free_hand()


def make_line():
    start.draw_stright_line()


def make_rectangle():
    start.draw_rectangle()


def make_square():
    start.draw_square()


def make_ellipse():
    start.draw_ellipse()


def make_circle():
    start.draw_circle()


def make_polygon():
    start.draw_polygon()


def make_move():
    start.moveObject()


def clear_screen():
    start.clear_screen()


def make_cut():
    start.cutObject()


def make_copy():
    start.copyObject()


def make_paste():
    start.pasteObject()


def select_color():
    color = colorchooser.askcolor()[1]
    start.color_selected = color
    start.color_selected_outline = color


def make_group():
    start.groupObjects()


def make_ungroup():
    start.ungroupObjects()


def make_save():
    start.save_file()


def make_open():
    start.open_file()


top_frame = ttk.Frame(root)
top_frame.pack(side="left", fill="both", expand=False)

free_hand = ttk.Button(top_frame, text="Free Hand", command=make_free_line)
free_hand.pack(side="top")
line = ttk.Button(top_frame, text="Line", command=make_line)
line.pack(side="top")
rectangle = ttk.Button(top_frame, text="Rectangle", command=make_rectangle)
rectangle.pack(side="top")
square = ttk.Button(top_frame, text="Square", command=make_square)
square.pack(side="top")
ellipse = ttk.Button(top_frame, text="Ellipse", command=make_ellipse)
ellipse.pack(side="top")
circle = ttk.Button(top_frame, text="Circle", command=make_circle)
circle.pack(side="top")
polygon = ttk.Button(top_frame, text="Polygon", command=make_polygon)
polygon.pack(side="top")
move = ttk.Button(top_frame, text="Move", command=make_move)
move.pack(side="top")
cut = ttk.Button(top_frame, text="Cut", command=make_cut)
cut.pack(side="top")
copy = ttk.Button(top_frame, text="Copy", command=make_copy)
copy.pack(side="top")
paste = ttk.Button(top_frame, text="Paste", command=make_paste)
paste.pack(side="top")
color = ttk.Button(top_frame, text="Choose Color", command=select_color)
color.pack(side="top")
group = ttk.Button(top_frame, text="Group", command=make_group)
group.pack(side="top")
ungroup = ttk.Button(top_frame, text="Ungroup", command=make_ungroup)
ungroup.pack(side="top")
clear = ttk.Button(top_frame, text="Clear Screen", command=clear_screen)
clear.pack(side="top")
save = ttk.Button(top_frame, text="Save", command=make_save)
save.pack(side="top")
open = ttk.Button(top_frame, text="Open", command=make_open)
open.pack(side="top")
start = Sketch1()


root.mainloop()
