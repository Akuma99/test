from tkinter import Tk, Canvas
import random

# Globals
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


# Helper functions
def create_block():
    """ Создает блок в случайной позиции на карте """
    global BLOCK
    posx = SEG_SIZE * random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE)
    # блок это кружочек красного цвета
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")


def main():
    """ Handles game process """
    global IN_GAME
    if IN_GAME:

        # Двигаем змейку
        s.move()

        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords

        # Столкновение с границами экрана
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False

        # Поедание яблок
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()

        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].instance):
                    IN_GAME = False
        root.after(100, main)
    # Если не в игре выводим сообщение о проигрыше
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class Segment(object):
    # def - обращение к функции/методу
    # Метод - фукция вызываемая внутри класса. Других различий между ними нет.
    # __init__ - метод вызываемый единожды для каждого объекта. Выполняет роль конструктора класса. 
    def __init__(self, x, y):
        # создать сегмент змейки в виде прямоугольника по координатам х, у, х+SEG_SIZE, у+SEG_SIZE
        # x и y - координаты первого угла
        # х+SEG_SIZE и у+SEG_SIZE - координаты второго угла
        # fill - цвет которым заполняется область между двумя углами
        # instance = экземляр
        # self - атрибут позволяющий любым объектам ссылаться на самих себя.
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white")


class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # изначально змейка двигается вправо
        self.vector = self.mapping["Right"]

    def move(self):
        """ Двигает змейку в заданном направлении """
        # перебираем все сегменты кроме первого
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            # задаем каждому сегменту позицию сегмента стоящего после него
            c.coords(segment, x1, y1, x2, y2)

        # получаем координаты сегмента перед "головой"
        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        # помещаем "голову" в направлении указанном в векторе движения
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    s.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global s
    create_block()
    s = create_snake()
    # Reaction on keypress
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)


# Setting up window
root = Tk()
root.title("PythonicWay Snake")


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()
# catch keypressing
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
root.mainloop()