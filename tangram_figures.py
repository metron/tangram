import io
import turtle
from math import sqrt
from tkinter import *

from PIL import Image


def get_leg_length(hypotenuse_length):
    return sqrt((hypotenuse_length * hypotenuse_length) / 2)

def mm_to_px(mm_length):
    return mm_length * 3000 / 70

def save_as_png(canvas, file_name):
    ps = canvas.postscript(colormode='color')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save(file_name, 'png')

def save_as_eps(canvas, file_name):
    canvas.postscript(file=file_name, colormode='color')


class Tangram:
    def __init__(self, l1=103, silhouette=False):
        self.l1 = l1 = mm_to_px(l1)  # l1 - гипотенуза большого треугольника
        self.l2 = l2 = get_leg_length(l1)  # катет большого треугольника = гипотенуза среднего треугольника
        self.l3 = l3 = get_leg_length(l2)  # катет среднего треугольника = гипотенуза маленького треугольника
        self.l4 = l4 = get_leg_length(l3)  # катет маленького треугольника = сторона квадрата
        self.silhouette = silhouette

        self.simples = {
            "Большой треугольник 1-го цвета": ("green", [l1, 135, l2, 90, l2, 135]),
            "Большой треугольник 2-го цвета": ("blue", [l1, 135, l2, 90, l2, 135]),
            "Средний треугольник 3-го цвета": ("red", [l2, 135, l3, 90, l3, 135]),
            "Маленький треугольник 4-го цвета": ("yellow", [l3, 135, l4, 90, l4, 135]),
            "Маленький треугольник 5-го цвета": ("#e0e0e0", [l3, 135, l4, 90, l4, 135]),
            "Квадрат 6-го цвета": ("orange", [l4, 90, l4, 90, l4, 90, l4, 90]),
            "Параллелограмм 7-го цвета": ("purple", [l3, 135, l4, 45, l3, 135, l4, 45]),
        }

        # книжная
        # WIDTH = int(mm_to_px(210))
        # HEIGHT = int(mm_to_px(297))
        # альбомная
        self.WIDTH = WIDTH = int(mm_to_px(287))
        self.HEIGHT = HEIGHT = int(mm_to_px(200))

        # Screen
        screen = Tk()
        screen.geometry("{0}x{1}+10+10".format(WIDTH, HEIGHT))
        screen.title("Example Code")
        screen.tk.call('tk', 'scaling', 10.0)
        # screen.configure(bg="Gray")
        # Canvas
        self.canvas = canvas = Canvas(master=screen, width=str(WIDTH), height=str(HEIGHT))
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.tt = turtle.RawTurtle(canvas)
        self.tt.penup()
        if silhouette:
            self.tt.color("#c0c0c0")

    def draw_simple(self, simple_name, start=0):
        color, operations = self.simples[simple_name]
        if not self.silhouette:
            self.tt.color(color)
        self.tt.begin_fill()
        self.tt.pendown(),
        operation_pairs = len(operations) // 2
        for i in range(operation_pairs):
            indx = 2 * ((i + start) % operation_pairs)
            self.tt.forward(operations[indx])
            self.tt.right(operations[indx + 1])
        self.tt.penup()
        self.tt.end_fill()

    def pistolet(self):
        y0 = self.l1 / 2
        x0 = 215
        self.tt.goto(x0, y0)
        self.tt.right(135)
        self.draw_simple("Большой треугольник 1-го цвета")

        self.tt.forward(self.l1 * 2)
        self.tt.right(135)
        self.tt.forward(self.l2 / 2)
        self.tt.right(45)
        self.draw_simple("Большой треугольник 2-го цвета")

        self.tt.goto(x0, y0)
        self.tt.right(180)
        self.tt.forward(self.l2)
        self.tt.right(180)
        self.draw_simple("Средний треугольник 3-го цвета")

        self.tt.goto(x0, y0)
        self.tt.right(45)
        self.draw_simple("Квадрат 6-го цвета")

        self.tt.forward(self.l4)
        self.draw_simple("Маленький треугольник 4-го цвета", start=2)

        self.tt.forward(self.l4)
        self.draw_simple("Параллелограмм 7-го цвета")

        self.tt.forward(self.l3)
        self.tt.right(135)
        self.tt.forward(self.l4)
        self.tt.right(180)
        self.draw_simple("Маленький треугольник 5-го цвета")

        self.tt.goto(self.WIDTH / 2 - 3000, -self.HEIGHT / 2 + 500)
        self.tt.color("black")
        self.tt.write("Пистолет", font=("Arial", 400, "normal"))


tan = Tangram(silhouette=True)
tan.tt.hideturtle()
tan.tt.speed(0)
tan.pistolet()

save_as_png(tan.canvas, "pistolet.png")
# save_as_eps(tt.getscreen().getcanvas(), "pistolet.eps")

