class Warrior():
    def __init__(self, name, power, endurance, hair_color):
        self.name = name
        self.power = power
        self.endurance = endurance
        self.hair_color = hair_color

    def sleep (self):
        print(f"{self.name} лег спать")
        self.endurance += 2

    def walk(self):
        print(f"Воин {self.name} идет...")
        self.endurance -= 1

    def eat(self):
        print(f"Воин {self.name} ест")
        self.power += 1

    def hit(self):
        print(f"Воин {self.name} наносит удар")
        self.endurance -= 6

    def info(self):
        print(f"Имя воина - {self.name}\nСила - {self.power}\nВыносливость - {self.endurance}\nЦвет волос - {self.hair_color}")

war1 = Warrior("Олег", 50, 60, "Черный")
war2 = Warrior("Егор", 80, 60, "Рыжий")

war1.info()
war1.sleep()
war1.info()