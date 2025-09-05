import json

class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        pass

class Bird(Animal):
    def __init__(self, name, age, voice):
        super().__init__(name, age)
        self.voice =voice

    def make_sound(self):
        print(f'Птица {self.name} издает звук - {self.voice}')

class Mammal(Animal):
    def __init__(self, name, age, voice):
        super().__init__(name, age)
        self.voice = voice

    def make_sound(self):
        print(f'Млекопитающее {self.name} издает звук - {self.voice}')

class Reptile(Animal):
    def __init__(self, name, age, voice):
        super().__init__(name, age)
        self.voice = voice

    def make_sound(self):
        print(f'Рептилия {self.name} издает звук - {self.voice}')

class Worker():
    def __init__(self, name, age):
        self.name = name
        self.age = age

class ZooKeeper(Worker):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.post = "Zoo keeper"

    def feed_animal(self):
        print(f'{self.name} кормит животного')

class Veterinarian(Worker):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.post = "Veterinarian"

    def heal_animal(self):
        print(f'{self.name} лечит животное')


class Zoo():
    def __init__(self, title):
        self.title = title
        self.workers = []
        self.animals = []

    def add_animal(self):
        try:
            type_animal = int(input(f'\nВыберите тип животного.\n'f'Введите 1, 2 или 3 для выбора\n'
                                    f'(1 - птица, 2 - млекопитающие, 3 - рептилия) - ').strip())
            if type_animal:
                if 0 < type_animal < 4:
                    name = input('Введите название животного - ').strip()
                    age = input('Введите возраст животного (например 2 мес.) - ').strip()
                    voice = input('Звук, который издает животное - ').strip()
                    if type_animal == 1:
                        bird = Bird(name, age, voice)
                        self.animals.append(bird)
                    elif type_animal == 2:
                        mammal = Mammal(name, age, voice)
                        self.animals.append(mammal)
                    elif type_animal == 3:
                        reptile = Reptile(name, age, voice)
                        self.animals.append(reptile)
                    else:
                        print('Ошибка создания животного')
                else:
                    print("Вы ввели не верное число. От 1 до 3!")
            else:
                print('Поле не может быть пустым')
        except Exception as e:
            print(f'Возникла ошибка - {e}')

    def add_zoo_keeper(self):
        print("\nДавайте добавим охраника")
        name = input('Как его зовут? - ')
        age = input('Сколько ему лет? -')
        zoo_keeper = ZooKeeper(name, age)
        self.workers.append(zoo_keeper)

    def add_veterinarian(self):
        print("\nДавайте добавим Ветеринара")
        name = input('Как его зовут? - ')
        age = input('Сколько ему лет? -')
        veterinarian = Veterinarian(name, age)
        self.workers.append(veterinarian)

    def get_workers(self):
        print(self.workers)

    def get_animals(self):
        print(self.animals)

    def save_to_file(self, filename="Zoo State.json"):
        data = {
            "zooTitle": self.title,
            "animals": [
                {
                    "type": animal.__class__.__name__,
                    "name": animal.name,
                    "age": animal.age,
                    "voice": getattr(animal, 'voice', '')
                }   for animal in self.animals
            ],
            "workers": [
                {
                    "type": worker.__class__.__name__,
                    "name": worker.name,
                    "age": worker.age
                }   for worker in self.workers
            ]
        }
        with open(filename, "w", encoding="utf8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f'Данные сохранены в {filename}')


def animal_sound(animals):
    for animal in animals:
        animal.make_sound()



animals = [Bird('Воробей', '5 Месяцев', 'чирик'), Mammal('Кит', '5 лет', 'Пение'),
           Reptile('Змея', '1 год', 'шипение') ]
animal_sound(animals)

zoo = Zoo("Зоопарк")
zoo.add_zoo_keeper()
zoo.add_animal()
zoo.add_veterinarian()
zoo.get_workers()
zoo.get_animals()
zoo.save_to_file()