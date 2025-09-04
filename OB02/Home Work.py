class User():
    __users = {}
    def __init__(self, id, name):
        self.__id = id
        self._name = name
        self._role = "user"
        User.__users[id] = self

    def get_users(self, role):
        if role == 'admin':
            return User.__users
        else:
            print('Данные не доступны')
            return {}

    def set_add_users(self, id, name):
        if id and name:
            User(id, name)
            print('Пользователь создан\n')
        else:
            print('Значения id или name пустые')

    def set_remove_user(self, id):
        if id in User.__users:
            del User.__users[id]
            print('Пользователь удален')
        else:
            print('Пользователь не найден\n')

    def __str__(self):
        return f"ID: {self.__id}, Имя: {self._name}, Уровень доступа: {self._role}"

class Admin(User):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.__private_role = "admin"

    def add_user(self):
        id = int(input('id - ').strip())
        name = input('Имя пользователя - ').strip()
        self.set_add_users(id, name)

    def remove_user(self):
        id = int(input("Введите id пользователя для удаления - ".strip()))
        User.set_remove_user(self, id)

    def get_users(self):
        users = User.get_users(self, 'admin')
        if users:
            for user_id, user in users.items():
                print(user)
        else:
            print('Пользователей не найдено')


user1 = User('123548151', 'Олег')
user2 = User('6548435184', 'Анна')
user3 = Admin('84358438484', 'Админ')

user3.get_users()

print('Давайте добавим пользователя:')
user3.add_user()
user3.get_users()

print('Давайте удалим пользователя: - ')
user3.remove_user()
user3.get_users()