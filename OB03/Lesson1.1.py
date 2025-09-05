class Engine():
    def start(self):
        print('Двигатель запущен')
    def stop(self):
        print('Двигатель остановлен')

class Car():
    def __init__(self):
        self.engine = Engine()

    def start(self):
        self.engine.start()
    def stop(self):
        self.engine.stop()

car = Car()
car.start()
car.stop()