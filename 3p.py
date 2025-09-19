import json


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

    def short_str(self):
        fam = self.__fio.split(' ')[0] 
        return f"ID: {self.__actor_id}, Фамилия: {fam}, Стаж (лет): {self.__staz}"

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return (self.__actor_id == other.__actor_id and
                self.__fio == other.__fio and
                self.__staz == other.__staz and
                self.__zvan == other.__zvan and
                self.__awards == other.__awards)

    @classmethod
    def from_json(cls, json_data):
        try:
            return cls(
                actor_id=json_data['ID'],
                fio=json_data['ФИО'],
                staz=json_data['Стаж'],
                zvan=json_data.get('Звание', []),
                awards=json_data.get('Награды', [])
            )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле в JSON: {e}")

    @classmethod
    def from_string(cls, csv_string):
        try:
            parts = csv_string.split(',')
            if len(parts) < 3:
                raise ValueError("Строка должна содержать минимум 3 поля: id,fio,staz")
            actor_id = int(parts[0])
            fio = parts[1]
            staz = float(parts[2])
            zvan = None
            if len(parts) > 3 and parts[3]:
                zvan = parts[3].split(';')
            awards = None
            if len(parts) > 4 and parts[4]:
                awards = parts[4].split(';')
            return cls(actor_id, fio, staz, zvan, awards)

        except ValueError as e:
            raise ValueError(f"Ошибка парсинга CSV строки: {e}")

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
        if items is None:
            return []
        if isinstance(items, str):
            if not items.strip():
                return []
            return [Actor.__validate_list_item(items, item_type)]
        if isinstance(items, list):
            validated_items = []
            for item in items:
                if isinstance(item, str) and item.strip():
                    validated_item = Actor.__validate_list_item(item, item_type)
                    validated_items.append(validated_item)
            return validated_items
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
        return f"ID: {self.__actor_id}, ФИО: {self.__fio}, Стаж (лет): {self.__staz} , Звания: {self.__zvan}, Награды: {self.__awards}"


try:
    actor1 = Actor(1, "Круз Том Сергеевич", 20, "Заслуженный артист РФ", [""])
    print("Полная форма:", actor1)
    print("Краткая форма:", actor1.short_str())

    json_data = {
        'ID': 2,
        'ФИО': 'Фокс Меган Александровна',
        'Стаж': 15,
        'Звание': [''],
        'Награды': ['Золотая пальмовая ветвь']
    }
    actor2 = Actor.from_json(json_data)
    print("Полная форма:",actor2)
    print("Краткая форма:", actor2.short_str())

    print("actor1 == actor2?", actor1 == actor2)
    csv_str = "3,Кавилл Генри Леонидович,7,,Премия MTV;BAFTA"
    actor3 = Actor.from_string(csv_str)
    print("Полная форма:",actor3)
    print("Краткая форма:", actor3.short_str())

except ValueError as e:
    print(f"Ошибка: {e}")



