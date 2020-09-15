class Player:
    money = int

    def __init__(self):
        self.money = 100

    def add_money(self, amount):
        self.money += amount

    def substract_money(self, amount):
        self.money -= amount
