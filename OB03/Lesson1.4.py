# # Продемонстрировать принцип полиморфизма через реализацию разных классов,
# представляющих геометрические формы, и метод для расчёта площади каждой формы.
# Создать базовый класс Shape с методом area(), который просто возвращает 0.
# Создать несколько производных классов для разных форм (например, Circle, Rectangle, Square),
# каждый из которых переопределяет метод area().
# В каждом из этих классов метод area() должен возвращать площадь соответствующей фигуры.
# # Написать функцию, которая принимает объект класса Shape и выводит его площадь.

class Shape():
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        s = 3.14 * self.radius**2
        print(f'Площадь круга с радиусом {self.radius} = {s}')

class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def area(self):
        s = self.a * self.b
        print(f'Площадь прямоугольника со сторонами {self.a} и {self.b} = {s}')

class Square(Shape):
    def __init__(self, a):
        self.a = a

    def area(self):
        s = 2 * self.a
        print(f'Площадь квадрата со стороной {self.a} = {s}')

shapes = [Circle(19), Rectangle(14, 8), Square(8)]

for shape in shapes:
    shape.area()