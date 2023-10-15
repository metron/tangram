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
            "1 большой треугольник": ("green", [l1, 135, l2, 90, l2, 135]),
            "2 большой треугольник": ("blue", [l1, 135, l2, 90, l2, 135]),
            "3 средний треугольник": ("red", [l2, 135, l3, 90, l3, 135]),
            "4 маленький треугольник": ("yellow", [l3, 135, l4, 90, l4, 135]),
            "5 маленький треугольник": ("#e0e0e0", [l3, 135, l4, 90, l4, 135]),
            "6 квадрат": ("orange", [l4, 90, l4, 90, l4, 90, l4, 90]),
            "7 параллелограмм": ("purple", [l3, 135, l4, 45, l3, 135, l4, 45]),
        }

        # книжная
        # WIDTH = int(mm_to_px(210))
        # HEIGHT = int(mm_to_px(297))
        # альбомная
        self.WIDTH = int(mm_to_px(287))
        self.HEIGHT = int(mm_to_px(200))
        self.add_canvas()

    def add_canvas(self):
        # Screen
        screen = Tk()
        screen.geometry("{0}x{1}+10+10".format(self.WIDTH, self.HEIGHT))
        screen.title("Example Code")
        screen.tk.call('tk', 'scaling', 10.0)
        # screen.configure(bg="Gray")
        # Canvas
        self.canvas = canvas = Canvas(master=screen, width=str(self.WIDTH), height=str(self.HEIGHT))
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.tt = turtle.RawTurtle(canvas)
        self.tt.hideturtle()
        self.tt.speed(0)
        self.tt.penup()
        if self.silhouette:
            self.tt.color("#c0c0c0")

    def write_name(self, name):
        self.tt.goto(self.WIDTH / 2 - 3000, -self.HEIGHT / 2 + 500)
        self.tt.color("black")
        self.tt.write(name, font=("Arial", 400, "normal"))

    def follow_steps(self, operations, steps_num, start, reverse_path):
        for i in range(steps_num):
            indx = (i + start) % len(operations)
            if indx % 2:
                if reverse_path:
                    self.tt.left(operations[indx])
                else:
                    self.tt.right(operations[indx])
            else:
                self.tt.forward(operations[indx])

    def draw_simple(self, simple_name, start=0, add_path=0, reverse_path=False):
        color, operations = self.simples[simple_name]
        if not self.silhouette:
            self.tt.color(color)
        self.tt.begin_fill()
        self.tt.pendown(),
        self.follow_steps(operations, len(operations), start, reverse_path)
        self.tt.penup()
        self.tt.end_fill()
        self.follow_steps(operations, add_path, start, reverse_path)

    def pistolet(self):
        y0 = self.l1 / 2
        x0 = 215
        self.tt.goto(x0, y0)
        self.tt.right(135)
        self.draw_simple("1 большой треугольник", add_path=2)
        self.tt.forward(self.l4)
        self.tt.right(180)
        self.draw_simple("2 большой треугольник", start=2)

        self.tt.goto(x0, y0)
        self.draw_simple("3 средний треугольник", start=2)
        self.draw_simple("6 квадрат", reverse_path=True, add_path=4)
        self.draw_simple("4 маленький треугольник", start=2, add_path=3)
        self.draw_simple("7 параллелограмм", add_path=3)
        self.tt.right(180)
        self.draw_simple("5 маленький треугольник")

        self.write_name("Пистолет")

    def home(self):
        y0 = 0
        x0 = -2500
        self.tt.goto(x0, y0)
        self.draw_simple("1 большой треугольник", add_path=2, reverse_path=True)
        self.draw_simple("7 параллелограмм", add_path=2)
        self.draw_simple("6 квадрат", reverse_path=True)

        self.tt.goto(x0, y0)
        self.tt.forward((self.l1 + self.l4) / 2)
        self.draw_simple("3 средний треугольник", start=2)
        self.tt.right(45)
        self.draw_simple("2 большой треугольник", start=4)
        self.tt.right(90)
        self.draw_simple("4 маленький треугольник", start=2, add_path=1)
        self.draw_simple("5 маленький треугольник", start=4)

        self.write_name("Дом")

    def korablik(self):
        y0 = - self.l2 / 2
        x0 = - self.l2 / 2
        self.tt.goto(x0, y0)
        self.tt.left(45)
        self.draw_simple("1 большой треугольник", reverse_path=True)
        self.draw_simple("2 большой треугольник")
        self.tt.left(45)
        self.draw_simple("4 маленький треугольник", reverse_path=True, start=2)
        self.tt.left(90)
        self.draw_simple("7 параллелограмм", start=2)
        self.tt.left(180)
        self.tt.forward(self.l2)
        self.draw_simple("5 маленький треугольник", start=4, reverse_path=True, add_path=2)
        self.draw_simple("3 средний треугольник", start=4)
        self.tt.right(45)
        self.tt.goto(x0, y0)
        self.tt.forward(self.l2)
        self.tt.right(90)
        self.tt.forward((self.l2 - self.l4) / 2)
        self.draw_simple("6 квадрат", reverse_path=True)
        self.write_name("Кораблик")


tan = Tangram(silhouette=True)

# tan.pistolet()
# save_as_png(tan.canvas, "result_images/pistolet.png")
# save_as_eps(tt.getscreen().getcanvas(), "pistolet.eps")

# tan.add_canvas()
# tan.home()
# save_as_png(tan.canvas, "result_images/home.png")

tan.add_canvas()
tan.korablik()
save_as_png(tan.canvas, "result_images/korablik.png")
