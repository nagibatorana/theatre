class Actor:
    def __init__(self, actor_id, fio, staz, zvan=None, awards=None):
        self.__validate_actor_id(actor_id)
        self.__validate_fio(fio)
        self.__validate_staz(staz)

        self.__actor_id = actor_id
        self.__fio = fio
        self.__staz = staz

        self.__zvan = self.__validate_and_prepare_list(zvan, "звание")
        self.__awards = self.__validate_and_prepare_list(awards, "награда")

    @staticmethod
    def __validate_actor_id(actor_id):
        if not isinstance(actor_id, int) or actor_id <= 0:
            raise ValueError("ID актера должен быть положительным целым числом")

    @staticmethod
    def __validate_fio(fio):
        if not fio or not isinstance(fio, str):
            raise ValueError("ФИО должно быть непустой строкой")
        if len(fio.strip()) < 5:
            raise ValueError("ФИО должно содержать не менее 5 символов")
        if ' ' not in fio:
            raise ValueError("ФИО должно содержать имя и фамилию через пробел")

    @staticmethod
    def __validate_staz(staz):
        if not isinstance(staz, (int, float)):
            raise ValueError("Стаж должен быть числом")
        if staz < 0:
            raise ValueError("Стаж не может быть отрицательным")
        if staz > 100:
            raise ValueError("Стаж не может превышать 100 лет")

    @staticmethod
    def __validate_list_item(item, item_type):
        if not isinstance(item, str):
            raise ValueError(f"{item_type} должно быть строкой")
        if not item.strip():
            raise ValueError(f"{item_type} не может быть пустой строкой")
        return item.strip()

    @staticmethod
    def __validate_and_prepare_list(items, item_type):
        if items is None:
            return []

        if isinstance(items, str):
            validated_item = Actor.__validate_list_item(items, item_type)
            return [validated_item]

        if not isinstance(items, list):
            raise ValueError(f"{item_type} должны быть переданы как список или строка")

        validated_items = []
        for item in items:
            validated_item = Actor.__validate_list_item(item, item_type)
            validated_items.append(validated_item)

        return validated_items

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
        self.__validate_fio(value)
        self.__fio = value

    def set_staz(self, value):
        self.__validate_staz(value)
        self.__staz = value

    def add_zvan(self, title):
        validated_title = self.__validate_list_item(title, "звание")
        self.__zvan.append(validated_title)

    def remove_zvan(self, title):
        if title in self.__zvan:
            self.__zvan.remove(title)

    def add_award(self, award):
        validated_award = self.__validate_list_item(award, "награда")
        self.__awards.append(validated_award)

    def remove_award(self, award):
        if award in self.__awards:
            self.__awards.remove(award)

    def __str__(self):
        return f"ID актера: {self.__actor_id}, ФИО: {self.__fio}, Стаж: {self.__staz} лет, Звания: {self.__zvan}, Награды: {self.__awards}"


try:
    actor = Actor(1, "Круз Том Сергеевич", 20, ["Заслуженный артист РФ"], ["Оскар"])
    print(actor)
except ValueError as e:
    print(f"Ошибка создания объекта: {e}")

