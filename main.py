class Phone:
    __slots__ = (
        'id', 'last_name', 'first_name', 'patronymic',
        'address', 'credit_card_number', 'debit', 'credit',
        '_local_call_time', '_long_distance_call_time'
    )

    def __init__(self, id, last_name, first_name, patronymic="",
                 address="", credit_card_number="", debit=0, credit=0,
                 local_call_time=0, long_distance_call_time=0):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.address = address
        self.credit_card_number = credit_card_number
        self.debit = debit
        self.credit = credit
        self._local_call_time = local_call_time
        self._long_distance_call_time = long_distance_call_time

    def __getattr__(self, item: str):
        if item.startswith('get_'):
            priv = item[4:]
            if hasattr(self, f'_{priv}'):
                return lambda: getattr(self, f'_{priv}')
        if item.startswith('set_'):
            priv = item[4:]
            if hasattr(self, f'_{priv}'):
                return lambda val: setattr(self, f'_{priv}', val)
        raise AttributeError(f'{self.__class__.__name__} has no attribute {item!r}')

    def __str__(self):
        return (
            f"Phone(id={self.id}, ФИО={self.last_name} {self.first_name} {self.patronymic}, "
            f"Адрес={self.address}, Карта={self.credit_card_number}, "
            f"Дебет={self.debit}, Кредит={self.credit}, "
            f"Время городских={self._local_call_time}, "
            f"Время междугородных={self._long_distance_call_time})"
        )

    def __hash__(self):
        return hash((self.id, self.last_name, self.first_name, self.patronymic))


phones = [
    Phone(1, "Иванов", "Иван", "Иванович", "Москва", "12345", 1000, 500, 120, 0),
    Phone(2, "Петров", "Петр", "Петрович", "СПб", "54321", 500, 300, 50, 20),
    Phone(3, "Сидоров", "Алексей", "Алексеевич", "Казань", "98765", 200, 100, 200, 10),
    Phone(4, "Андреев", "Сергей", "Сергеевич", "Самара", "67890", 800, 400, 30, 0)
]

threshold = 100
print(f"a) Абоненты с временем городских разговоров > {threshold}:")
for p in phones:
    if p.get_local_call_time() > threshold:
        print(p)

print("\nb) Абоненты, пользовавшиеся междугородной связью:")
for p in phones:
    if p.get_long_distance_call_time() > 0:
        print(p)

print("\nc) Абоненты в алфавитном порядке:")
phones_sorted = sorted(phones, key=lambda x: (x.last_name, x.first_name, x.patronymic))
for p in phones_sorted:
    print(p)
