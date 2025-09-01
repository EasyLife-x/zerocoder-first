tasks = []
def add_task():
    description = input("Введите описание задачи - ").strip()
    deadline = input("Срок выполнения DD/MM/YYYY - ").strip()
    status = False
    if description != '' and deadline != '':
        tasks.append(Task(description, deadline, status))
    else:
        print('Введите описание задачи и срок выполнения')

def current_tasks():
    current = []
    print(f'\n Текущие задачи:')
    for task in tasks:
        if task.status == False:
            current.append(task)
            print(f'{task.description} - {task.deadline}')

def complete(description):
    task_to_complete = ''
    for task in tasks:
        if task.description == description: 
            task.status = True
            print(f'\n Задача {description} выполнена')
            task_to_complete = task
    if task_to_complete == '':
        print('Задача не найдена')


class Task():
    def __init__(self, description, deadline, status):
        self.description = description
        self.deadline = deadline
        self.status = status

    def __str__(self):
        return f'{self.description} - {self.deadline}'


add_task()
add_task()
add_task()

current_tasks()

complete(input('Введите описание задачи, которую хотите выполнить - '))
current_tasks()