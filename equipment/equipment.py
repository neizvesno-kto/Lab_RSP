class Equipment:
    def __init__(self, name: str, price: float, weight: float):
        self._name = name
        self._price = price
        self._weight = weight
    #Инкапсуляция
    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def weight(self):
        return self._weight
    #Полиморфизм
    def __str__(self):
        return f"{self.name} (Цена: {self.price:.2f}$, Вес: {self.weight:.2f} кг)"
