from datetime import date


class BankAccount:
    def __init__(self, owner, number, balance=0):
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self.owner = owner
        self.number = number
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True


class SavingsAccount(BankAccount):
    def __init__(self, owner, number, balance, rate):
        super().__init__(owner, number, balance)
        self.rate = rate

    def accrue(self):
        return self.deposit(self.balance * self.rate / 100)

    def withdraw(self, amount):
        if not super().withdraw(amount):
            return False
        fee = min(amount * 0.01, self.balance)
        if fee > 0:
            super().withdraw(fee)
        return True


class Pet:
    def __init__(self, name, age, energy=50):
        self.name = name
        self.age = age
        self.__energy = max(0, min(100, energy))

    @property
    def energy(self):
        return self.__energy

    def feed(self, portion):
        if portion <= 0:
            return False
        self.__energy = min(100, self.__energy + portion)
        return True

    def sleep(self, hours):
        if hours <= 0:
            return False
        self.__energy = min(100, self.__energy + hours * 10)
        return True

    def _spend_energy(self, amount):
        if amount <= 0 or amount > self.__energy:
            return False
        self.__energy -= amount
        return True


class Cat(Pet):
    def __init__(self, name, age, energy=50, lives=9):
        super().__init__(name, age, energy)
        self.lives = lives

    def climb(self):
        if not self._spend_energy(15):
            self.lives = max(0, self.lives - 1)
            return False
        return True


class Dog(Pet):
    def __init__(self, name, age, energy=50):
        super().__init__(name, age, energy)
        self.tricks = 0

    def do_trick(self):
        if not self._spend_energy(20):
            return False
        self.tricks += 1
        return True


class Person:
    def __init__(self, full_name, birth_year):
        self.__full_name = full_name
        self.birth_year = birth_year

    @property
    def full_name(self):
        return self.__full_name

    def age(self):
        return date.today().year - self.birth_year

    def rename(self, new_name):
        self.__full_name = new_name


class Employee(Person):
    def __init__(self, full_name, birth_year, job_title, salary):
        super().__init__(full_name, birth_year)
        self.job_title = job_title
        self.salary = salary

    def promote(self, new_title, raise_amount):
        if raise_amount <= 0:
            return False
        self.job_title = new_title
        self.salary += raise_amount
        return True


class Manager(Employee):
    def __init__(self, full_name, birth_year, job_title, salary):
        super().__init__(full_name, birth_year, job_title, salary)
        self.__team = []

    @property
    def team(self):
        return self.__team.copy()

    def hire(self, employee):
        self.__team.append(employee)

    def fire(self, full_name):
        for employee in self.__team:
            if employee.full_name == full_name:
                self.__team.remove(employee)
                return True
        return False

    def payroll(self):
        total = self.salary
        for employee in self.__team:
            total += employee.salary
        return total


class Parcel:
    def __init__(self, destination, weight, declared_value):
        self.destination = destination
        self.weight = weight
        self.declared_value = declared_value

    def cost(self):
        return self.weight * 10 + self.declared_value * 0.01


class FragileParcel(Parcel):
    def __init__(self, destination, weight, declared_value):
        super().__init__(destination, weight, declared_value)
        self.__insured = False

    @property
    def insured(self):
        return self.__insured

    def cost(self):
        return super().cost() + 200

    def pack(self):
        self.__insured = True


class ExpressParcel(Parcel):
    def __init__(self, destination, weight, declared_value, hours_left):
        super().__init__(destination, weight, declared_value)
        self.__hours_left = max(0, hours_left)

    @property
    def hours_left(self):
        return self.__hours_left

    def cost(self):
        return super().cost() * 1.5

    def deliver(self, hours):
        if hours <= 0:
            return False
        self.__hours_left = max(0, self.__hours_left - hours)
        return True


class Track:
    def __init__(self, name, duration):
        if duration <= 0:
            raise ValueError("Длительность должна быть больше нуля")
        self.name = name
        self.__duration = duration

    @property
    def duration(self):
        return self.__duration


class Playlist:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.__tracks = []

    @property
    def tracks(self):
        return self.__tracks.copy()

    def add(self, track):
        name = track.name.strip()
        if not name:
            return False
        for existing in self.__tracks:
            if existing.name.strip() == name:
                return False
        self.__tracks.append(track)
        return True

    def remove(self, name):
        name = name.strip()
        for track in self.__tracks:
            if track.name.strip() == name:
                self.__tracks.remove(track)
                return True
        return False

    def duration(self):
        total = 0
        for track in self.__tracks:
            total += track.duration
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, name, owner):
        super().__init__(name, owner)
        self.__editors = set()

    @property
    def editors(self):
        return self.__editors.copy()

    def invite(self, name):
        self.__editors.add(name)

    def exclude(self, name):
        self.__editors.discard(name)

    def add(self, track, editor):
        if editor not in self.__editors:
            return False
        return super().add(track)


class Order:
    def __init__(self, number, customer):
        self.number = number
        self.customer = customer
        self.__status = "создан"

    @property
    def status(self):
        return self.__status

    def _change_status(self, allowed, new_status):
        if self.__status not in allowed:
            return False
        self.__status = new_status
        return True

    def pay(self):
        return self._change_status(("создан",), "оплачен")

    def cancel(self):
        return self._change_status(("создан", "оплачен"), "отменён")


class PickupOrder(Order):
    def __init__(self, number, customer, shop_address):
        super().__init__(number, customer)
        self.shop_address = shop_address

    def assemble(self):
        return self._change_status(("оплачен",), "готов к выдаче")


class DeliveryOrder(Order):
    def __init__(self, number, customer, address):
        super().__init__(number, customer)
        self.address = address
        self.__courier = None

    @property
    def courier(self):
        return self.__courier

    def assign_courier(self, name):
        if self.status != "оплачен" or not name.strip():
            return False
        self.__courier = name
        return True

    def send(self):
        if self.__courier is None:
            return False
        return self._change_status(("оплачен",), "отправлен")


class Diploma:
    __next_number = 1

    def __init__(self, student, specialty, issue_date):
        self.__student = student
        self.__specialty = specialty
        self.__issue_date = issue_date
        self.__number = Diploma.__next_number
        Diploma.__next_number += 1

    @property
    def student(self):
        return self.__student

    @property
    def specialty(self):
        return self.__specialty

    @property
    def issue_date(self):
        return self.__issue_date

    def get_number(self):
        return self.__number

    def text(self):
        return (
            f"Диплом №{self.__number}: {self.__student}, "
            f"{self.__specialty}, {self.__issue_date}"
        )


class HonorsDiploma(Diploma):
    def __init__(self, student, specialty, issue_date, topic, grade):
        if not 4 <= grade <= 5:
            raise ValueError("Оценка должна быть от 4 до 5")
        super().__init__(student, specialty, issue_date)
        self.topic = topic
        self.grade = grade

    def text(self):
        return f"{super().text()}; тема: {self.topic}; оценка: {self.grade}"


class Device:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.__is_on = False

    @property
    def is_on(self):
        return self.__is_on

    def toggle(self):
        self.__is_on = not self.__is_on

    def consumption(self):
        return 0


class Lamp(Device):
    def __init__(self, brand, model, brightness):
        if brightness not in (1, 2, 3):
            raise ValueError("Яркость должна быть 1, 2 или 3")
        super().__init__(brand, model)
        self.__brightness = brightness

    @property
    def brightness(self):
        return self.__brightness

    def consumption(self):
        if not self.is_on:
            return 0
        return self.__brightness * 10


class Kettle(Device):
    def __init__(self, brand, model, water):
        super().__init__(brand, model)
        self.water = water
        self.__boils = 0

    @property
    def boils(self):
        return self.__boils

    def boil(self):
        if not self.is_on or self.water <= 0:
            return False
        self.__boils += 1
        return True

    def consumption(self):
        if not self.is_on:
            return 0
        return 1500


def total_consumption(devices):
    total = 0
    for device in devices:
        total += device.consumption()
    return total


class Hero:
    def __init__(self, name, health, gold):
        self.name = name
        self.__health = max(0, min(100, health))
        self.__gold = max(0, gold)

    @property
    def health(self):
        return self.__health

    @property
    def gold(self):
        return self.__gold

    def take_damage(self, amount):
        if amount > 0:
            self.__health = max(0, self.__health - amount)

    def heal(self, amount):
        if amount > 0 and self.__health > 0:
            self.__health = min(100, self.__health + amount)

    def spend(self, amount):
        if amount <= 0 or amount > self.__gold:
            return False
        self.__gold -= amount
        return True

    def earn(self, amount):
        if amount > 0:
            self.__gold += amount


class Merchant(Hero):
    def __init__(self, name, health, gold, prices):
        super().__init__(name, health, gold)
        self.__prices = prices.copy()
        self.__stock = {}

    @property
    def prices(self):
        return self.__prices.copy()

    @property
    def stock(self):
        return self.__stock.copy()

    def buy(self, item):
        if item not in self.__prices:
            return False
        if not self.spend(self.__prices[item]):
            return False
        self.__stock[item] = self.__stock.get(item, 0) + 1
        return True

    def sell(self, item):
        if self.__stock.get(item, 0) == 0:
            return False
        self.__stock[item] -= 1
        self.earn(self.__prices[item])
        return True

    def take_damage(self, amount):
        super().take_damage(amount * 0.7)


class Account:
    def __init__(self, login, email, password):
        self.login = login
        self.__email = email
        self.__password = password

    @property
    def email(self):
        return self.__email

    def change_email(self, new_email):
        if "@" not in new_email:
            return False
        self.__email = new_email
        return True

    def verify(self, password):
        return password == self.__password

    def change_password(self, old_password, new_password):
        if not self.verify(old_password) or len(new_password) < 8:
            return False
        self.__password = new_password
        return True


class Moderator(Account):
    def __init__(self, login, email, password):
        super().__init__(login, email, password)
        self.__warnings = {}
        self.__muted = set()
        self.__password_history = [password]

    @property
    def warnings(self):
        return self.__warnings.copy()

    @property
    def muted(self):
        return self.__muted.copy()

    def warn(self, user):
        self.__warnings[user] = self.__warnings.get(user, 0) + 1

    def mute(self, user):
        if self.__warnings.get(user, 0) < 3:
            return False
        self.__muted.add(user)
        return True

    def change_password(self, old_password, new_password):
        if new_password in self.__password_history:
            return False
        if not super().change_password(old_password, new_password):
            return False
        self.__password_history.append(new_password)
        self.__password_history = self.__password_history[-3:]
        return True
