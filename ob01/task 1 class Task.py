tasks = []

def add_task():
    description = input("Введите описание задачи - ").strip()
    deadline = input("Срок выполнения DD/MM/YYYY - ").strip()
    status = False
    if description != '' and deadline != '':
        tasks.append(Task(description, deadline, status))



class Task():
    def __init__(self, description, deadline, status):
        self.description = description
        self.deadline = deadline
        self.status = status

    def complete(self):
        self.status = True


add_task()
print(f'\n Список задач: {tasks}')