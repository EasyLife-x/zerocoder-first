class Test():
    def __init__(self):
        self.public = "Публичный атрибут"
        self._protected = "Защищенный отрибут"
        self.__private = "Приватный атрибут"

    def get_private(self):
        return self.__private
    def set_private(self):
        self.__private = "Новый атрибут"
        print(self.__private)

test = Test()
print(test.get_private())
test.set_private()