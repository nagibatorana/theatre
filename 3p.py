class Actor:
    def __init__(self, actor_id, fio, staz, zvan=None, awards=None):
        self.__validate_actor_id(actor_id)
        self.__validate_fio(fio)
        self.__validate_staz(staz)
        self.__actor_id = actor_id
        self.__fio = fio
        self.__staz = staz
        self.__zvan = self.__prepare_list(zvan, "звание")
        self.__awards = self.__prepare_list(awards, "награда")

    @staticmethod
    def __validate(condition, error_message):
        if not condition:
            raise ValueError(error_message)

    @staticmethod
    def __validate_actor_id(actor_id):
        Actor.__validate(
            isinstance(actor_id, int) and actor_id > 0,
            "ID актера должен быть положительным целым числом"
        )

    @staticmethod
    def __validate_fio(fio):
        Actor.__validate(
            isinstance(fio, str) and fio.strip() and len(fio.strip()) >= 5 and ' ' in fio,
            "ФИО должно быть непустой строкой не менее 5 символов с пробелом"
        )

    @staticmethod
    def __validate_staz(staz):
        Actor.__validate(
            isinstance(staz, (int, float)) and 0 <= staz <= 100,
            "Стаж должен быть числом от 0 до 100 лет"
        )

    @staticmethod
    def __validate_list_item(item, item_type):
        Actor.__validate(
            isinstance(item, str) and item.strip(),
            f"{item_type} должно быть непустой строкой"
        )
        return item.strip()

    @staticmethod
    def __prepare_list(items, item_type):
        """Универсальная подготовка списка"""
        if items is None:
            return []
        if isinstance(items, str):
            return [Actor.__validate_list_item(items, item_type)]
        if isinstance(items, list):
            return [Actor.__validate_list_item(item, item_type) for item in items]
        raise ValueError(f"{item_type} должны быть списком или строкой")

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

    def __manage_list_item(self, item, list_name, action, item_type):
        if action == "add":
            validated = self.__validate_list_item(item, item_type)
            getattr(self, list_name).append(validated)
        elif action == "remove" and item in getattr(self, list_name):
            getattr(self, list_name).remove(item)

    def add_zvan(self, title):
        self.__manage_list_item(title, "_Actor__zvan", "add", "звание")

    def remove_zvan(self, title):
        self.__manage_list_item(title, "_Actor__zvan", "remove", "звание")

    def add_award(self, award):
        self.__manage_list_item(award, "_Actor__awards", "add", "награда")

    def remove_award(self, award):
        self.__manage_list_item(award, "_Actor__awards", "remove", "награда")

    def __str__(self):
        return f"ID: {self.__actor_id}, ФИО: {self.__fio}, Стаж: {self.__staz} лет, Звания: {self.__zvan}, Награды: {self.__awards}"

try:
    actor = Actor(1, "Круз Том Сергеевич", 20, "Заслуженный артист РФ", ["Оскар"])
    print(actor)
    actor.add_zvan("")
    actor.add_award("Золотой глобус")
    print(actor)
except ValueError as e:
    print(f"Ошибка: {e}")
