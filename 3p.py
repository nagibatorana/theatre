class Actor:
    def __init__(self, actor_id, fio, staz, zvan=None, awards=None):
        self.__actor_id = actor_id
        self.__fio = fio
        self.__staz = staz
        self.__zvan = zvan if zvan is not None else []
        self.__awards = awards if awards is not None else []

    def get_actor_id(self):
        return self.__actor_id

    def get_fio(self):
        return self.__fio

    def get_staz(self):
        return self.__staz

    def get_zvan(self):
        return self.__zvan.copy()

    def get_awards(self):
        return self.__awards.copy()

    def set_fio(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("ФИО должно быть непустой строкой")
        self.__fio = value

    def set_staz(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Стаж должен быть неотрицательным числом")
        self.__staz = value

    def add_zvan(self, title):
        if title and isinstance(title, str):
            self.__zvan.append(title)

    def remove_zvan(self, title):
        if title in self.__zvan:
            self.__zvan.remove(title)

    def add_award(self, award):
        if award and isinstance(award, str):
            self.__awards.append(award)

    def remove_award(self, award):
        if award in self.__awards:
            self.__awards.remove(award)

    def __str__(self):
        return f"ID актера: {self.__actor_id}, ФИО актера: {self.__fio}, Стаж (лет): {self.__staz}, Звания: {self.__zvan}, Награды: {self.__awards})"

actor = Actor(1, "Круз Том Сергеевич", 20, ["Заслуженный артист РФ"], ["Оскар"])
print(actor)

actor.set_fio("Кузнецов Том Сергеевич")
actor.set_staz(15)
actor.add_award("Золотой глобус")
print(actor)


