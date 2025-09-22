import json

class ActorShort:

    def __init__(self, actor_id, fam, staz):
        self.__validate_actor_id(actor_id)
        self.__actor_id = actor_id
        self.__validate_staz(staz)
        self.__fam = fam
        self.__staz = staz

    def __eq__(self, other):
        if not isinstance(other, ActorShort):
            return False
        return (self.__actor_id == other.__actor_id and
                self.__fam == other.__fam and
                self.__staz == other.__staz)

    @staticmethod
    def __validate_actor_id(actor_id):
        if not isinstance(actor_id, int) or actor_id <= 0:
            raise ValueError("ID актера должен быть положительным целым числом")

    @staticmethod
    def __validate_staz(staz):
        if not isinstance(staz, (int, float)) or staz < 0:
            raise ValueError("Стаж должен быть неотрицательным числом")
        if staz > 100:
            raise ValueError("Стаж не может превышать 100 лет")

    def get_actor_id(self):
        return self.__actor_id

    def get_fam(self):
        return self.__fam

    def get_staz(self):
        return self.__staz

    def set_staz(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Стаж должен быть неотрицательным числом")
        self.__staz = value

    def __str__(self):
        return f"ID: {self.__actor_id}, Фамилия: {self.__fam}, Стаж (лет): {self.__staz}"

    def to_full(self, fio, zvan=None, awards=None):
        return Actor(self, fio, zvan, awards)


class Actor(ActorShort):

    def __init__(self, short_actor, fio, zvan=None, awards=None):
        super().__init__(short_actor.get_actor_id(), short_actor.get_fam(), short_actor.get_staz())
        self.__validate_fio(fio)
        self.__fio = fio
        self.__zvan = self.__prepare_list(zvan, "звание")
        self.__awards = self.__prepare_list(awards, "награда")

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return (super().__eq__(other) and
                self.__fio == other.__fio and
                self.__zvan == other.__zvan and
                self.__awards == other.__awards)

    @staticmethod
    def __validate_fio(fio):
        if not fio or not isinstance(fio, str):
            raise ValueError("ФИО должно быть непустой строкой")
        if len(fio.strip()) < 5:
            raise ValueError("ФИО должно содержать не менее 5 символов")
        if ' ' not in fio:
            raise ValueError("ФИО должно содержать имя и фамилию через пробел")

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

    @staticmethod
    def __validate_list_item(item, item_type):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{item_type} должно быть непустой строкой")
        return item.strip()

    @classmethod
    def from_json(cls, json_data):
        try:
            short_actor = ActorShort(
                json_data['ID'],
                cls.__only_fam(json_data['ФИО']),
                json_data['Стаж']
            )
            return cls(
                short_actor,
                json_data['ФИО'],
                json_data.get('Звание', []),
                json_data.get('Награды', [])
            )
        except KeyError as e:
            raise ValueError(f"Отсутствует обязательное поле в JSON: {e}")

    @classmethod
    def from_string(cls, string_data):
        if string_data.strip().startswith('{'):
            try:
                json_data = json.loads(string_data)
                return cls.from_json(json_data)
            except json.JSONDecodeError:
                raise ValueError("Некорректный JSON формат")
        else:
            try:
                parts = string_data.split(',')
                if len(parts) < 3:
                    raise ValueError("Строка должна содержать минимум 3 поля: ID, ФИО, Стаж")

                actor_id = int(parts[0])
                fio = parts[1].strip()
                staz = float(parts[2])
                short_actor = ActorShort(actor_id, cls.__only_fam(fio), staz)
                zvan = None
                if len(parts) > 3 and parts[3].strip():
                    zvan = parts[3].split(';')
                awards = None
                if len(parts) > 4 and parts[4].strip():
                    awards = parts[4].split(';')
                return cls(short_actor, fio, zvan, awards)

            except ValueError as e:
                raise ValueError(f"Ошибка парсинга CSV строки: {e}")

    @staticmethod
    def __only_fam(fio):
        if not fio or not isinstance(fio, str):
            return ""
        parts = fio.split(' ')
        return parts[0] if parts else ""

    def get_fio(self):
        return self.__fio

    def get_zvan(self):
        return self.__zvan.copy()

    def get_awards(self):
        return self.__awards.copy()

    def set_fio(self, value):
        self.__validate_fio(value)
        self.__fio = value

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
        return f"ID: {self.get_actor_id()}, ФИО: {self.__fio}, Стаж (лет): {self.get_staz()}, Звания: {self.__zvan}, Награды: {self.__awards}"

try:
    short_actor1 = ActorShort(1, "Круз", 20)
    print(short_actor1)

    full_actor1 = short_actor1.to_full("Круз Том Сергеевич",["Заслуженный артист РФ"],["Оскар"])
    print(full_actor1)

    json_data = (
        '{"ID": 2,'
        '"ФИО": "Фокс Меган Александровна",'
        '"Стаж": 15,'
        '"Звание": ["Заслуженная артистка"],'
        '"Награды": ["Золотая пальмовая ветвь"]}'
    )
    actor2 = Actor.from_string(json_data)
    print(actor2)

    csv_str = "3,Кавилл Генри Леонидович,7, ,Премия MTV;BAFTA"
    actor3 = Actor.from_string(csv_str)
    print(actor3)

    print("full_actor является ActorShort?", isinstance(full_actor1, ActorShort))
    print("full_actor является Actor?", isinstance(full_actor1, Actor))
    print("short_actor является Actor?", isinstance(short_actor1, Actor))
    print("actor1 == actor2?", short_actor1 == actor2)

except ValueError as e:
    print(f"Ошибка: {e}")
