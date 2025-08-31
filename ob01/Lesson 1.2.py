# Определите класс 'Account' иммитирующий банковский счет. Класс должен включать
# атрибуты для хранения идентификатора владельца, баланс счета и методы для депозита (пополнения)
# и снятия средств, если на счету достаточно средств


class Account():

    def __init__(self, user_id, balance = 0):
        self.user_id = user_id
        self.balance = balance

    def replenishment(self, cash):
        if cash > 0:
            self.balance += cash
            print(f'Ваш баланс - {self.balance} рублей\n')
        else:
            print("Значение не может быть равным или меньше 0")

    def withdrawal_of_funds(self, cash):
        if cash <= self.balance:
            self.balance -= cash
            print(f'Ваш баланс - {self.balance} рублей\n')
        elif cash == 0:
            print("Операция не выполнена. Сумма не может быть равна 0")
        else:
            print("Недостаточно денег на счету")

    def my_balance(self):
        print(f"Ваш баланс {self.balance} рублей")

acc1 = Account("Олег", 1000)

acc1.replenishment(int(input("введите сумму для пополнения - ")))
acc1.withdrawal_of_funds(int(input("введите сумму для снятия наличных - ")))
acc1.my_balance()