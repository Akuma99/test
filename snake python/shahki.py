from tkinter import *
import random

# Создаем окно
root = Tk()
# Устанавливаем название окна
root.title("PythonicWay Snake")

# ширина экрана
WIDTH = 800
# высота экрана
HEIGHT = 600
# Размер сегмента змейки
SEG_SIZE = 20
# Переменная отвечающая за состояние игры
IN_GAME = True

# Создаем игровое поле класса Canvas (его мы еще будем использовать) и заливаем все зеленым цветом
c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()
# Наводим фокус на Canvas, чтобы мы могли ловить нажатия клавиш
c.focus_set()

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
		self.instance = c.create_oval(x, y,
						x+SEG_SIZE, y+SEG_SIZE,
						fill="white")
class Snake(object):
    def __init__(self, segments):
        self.segments = segments
         
        # список доступных направлений движения змейки
        self.mapping = {"Down": (0, 1), "Up": (0, -1),
                                "Left": (-1, 0), "Right": (1, 0) }
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
                       x1 + self.vector[0]*SEG_SIZE,
                       y1 + self.vector[1]*SEG_SIZE,
                       x2 + self.vector[0]*SEG_SIZE,
                       y2 + self.vector[1]*SEG_SIZE)
     
    def change_direction(self, event):
        """ Изменяет направление движения змейки """
 
        # event передаст нам символ нажатой клавиши
        # и если эта клавиша в доступных направлениях 
        # изменяем направление
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]
 
    def add_segment(self):
        """ Добавляет сегмент змейке """
 
        # определяем последний сегмент
        last_seg = c.coords(self.segments[0].instance)
         
        # определяем координаты куда поставить следующий сегмент
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
         
        # добавляем змейке еще один сегмент в заданных координатах
        self.segments.insert(0, Segment(x, y))  
def create_block():
    """ Создает блок в случайной позиции на карте """
    global BLOCK
    posx = SEG_SIZE * (random.randint(1, (WIDTH-SEG_SIZE) / SEG_SIZE))
    posy = SEG_SIZE * (random.randint(1, (HEIGHT-SEG_SIZE) / SEG_SIZE))
     
    # блок это кружочек красного цвета
    BLOCK = c.create_oval(posx, posy,
                          posx + SEG_SIZE,
                          posy + SEG_SIZE,
                          fill="red")

def main():
    global IN_GAME
     
    if IN_GAME:
        # Двигаем змейку
        s.move()
  
        # Определяем координаты головы
        head_coords = c.coords(s.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
     
        # Столкновение с границами экрана
        if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
     
        # Поедание яблок 
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            c.create_block()
 
        # Самоедство
        else:
            # Проходим по всем сегментам змеи
            for index in range(len(s.segments)-1):
                if c.coords(s.segments[index].instance) == head_coords:
                    IN_GAME = False
     
    # Если не в игре выводим сообщение о проигрыше
    else:
          c.create_text(WIDTH/2, HEIGHT/2,
                              text="GAME OVER!",
                              font="Arial 20",
                              fill="#ff0000")

c.bind("<KeyPress>", s.change_direction)


# Запускаем окно
root.mainloop()