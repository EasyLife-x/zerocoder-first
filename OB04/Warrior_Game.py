from abc import ABC, abstractmethod

class Weapon(ABC):
  @abstractmethod
  def __init__(self, name):
    self.name = name
    
  @abstractmethod
  def attack(self):
    pass

class Sword(Weapon):
  def __init__(self, name):
    self.name = name
    
  def attack(self):
    return 'Наносит рубящий удар'

class Bow(Weapon):
  def __init__(self, name):
    self.name = name
  
  def attack(self):
    return 'Наносит колющий удар'

class Fighter():
  def __init__(self, name):
    self.name = name

  def take_weapon(self, weapon):
    self.weapon = weapon
    print(f'Воин {self.name} взял оружие {self.weapon.name}')

  def attack(self):
    print(f'Воин {self.weapon.attack()}')

class Monster():
  def __init__(self, name):
    self.name = name

  def monster_dead(self):
    print(f'Монстр {self.name} побежден')

sword = Sword('Меч')
bow = Bow('Лук')
fighter = Fighter('Иван')
monster = Monster('Зомби')

fighter.take_weapon(sword)
fighter.attack()
monster.monster_dead()

fighter.take_weapon(bow)
fighter.attack()
monster.monster_dead()


    