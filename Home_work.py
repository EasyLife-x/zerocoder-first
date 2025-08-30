
def check_float_num():
    try:
        number = input(f"Введите число, или нажмите Enter для выхода\n- ").strip()
        if number == "":
            return "exit"
        number = float(number)
        return number
    except ValueError:
        print("Неправильное значение")
        return None

while True:
    result = check_float_num()
    if result == "exit":
        print("Пользователь завершил программу")
        break
    elif result is not None:
        print(result)


