from random import randint

class Store:
  def __init__(self, name, adress, items):
    self.name = name
    self.adress = adress
    self.items = {}

  def add_item(self, item, price):
    product = {item: price}
    if item not in self.items:
      self.items.update(product)
      print(f'\nПродукт {item} Добавлен в асортимент магазина {self.name}')

  def remove_item(self, item):
    if item in self.items:
      self.items.pop(item)
      print(f'\nПродукт {item} Удален из асортимента магазина {self.name}')
    else:
      print("Продукт не найден\n")
      
  def get_price(self, item):
    if item in self.items:
      print(f"\nПродукт {item} - {self.items.get(item)} рублей")
    else:
      return None

  def update_price(self, item, price):
    product = {item: price}
    if item in self.items:
      self.items.update(product)
      print(f'\nЦена продукта {item} изменена на {price} рублей')
    else:
      print("Продукт не найден\n")

# Функции создания магазинов и добавления товаров
def create_stores():
  store1 = Store('Магазин 1', 'Адрес 1', {})
  store2 = Store('Магазин 2', 'Адрес 2', {})
  store3 = Store('Магазин 3', 'Адрес 3', {})
  return store1, store2, store3

def add_items(store1, store2, store3):
  for i in range(3):
    store1.add_item(f"Товар{i}", randint(1, 1000))
    store2.add_item(f"Товар{i}", randint(1, 1000))
    store3.add_item(f"Товар{i}", randint(1, 1000))

store1, store2, store3 = create_stores()
add_items(store1, store2, store3)

print(f"Товары магазина {store2.items}\n")
store2.remove_item('Товар2')
print(f"Товары магазина {store2.items}\n")

store2.get_price('Товар0')
print(f"Товары магазина {store2.items}\n")

store2.update_price('Товар1', 658)
print(f"Товары магазина {store2.items}\n")