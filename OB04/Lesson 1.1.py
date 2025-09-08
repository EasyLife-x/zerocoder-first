class Bird():
    def __init__(self, name):
        self.name = name

    def fly(self):
        print("Птица летает")

class Penguin(Bird):
    pass

p = Penguin('Пингвин')

p.fly()
