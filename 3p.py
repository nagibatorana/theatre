import psycopg2
import json
import yaml

class Actor_rep_json:
    def __init__(self, filename="actors.json"):
        self.filename = filename
        self.data = []
        self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f) or []
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_by_id(self, actor_id):
        for actor in self.data:
            if actor.get('ID') == actor_id:
                return actor
        return None

    def get_k_n_short_list(self, k, n):
        start_index = (n - 1) * k
        end_index = start_index + k

        short_list = []
        for actor in self.data[start_index:end_index]:
            short_actor = {
                'ID': actor.get('ID'),
                'Фамилия': actor.get('Фамилия'),
                'Стаж': actor.get('Стаж')
            }
            short_list.append(short_actor)
        return short_list

    def sort_by_field(self, field, reverse=False):
        if not self.data:
            return

        if field not in self.data[0]:
            raise ValueError(f"Поле {field} не существует в данных")

        self.data.sort(key=lambda x: x.get(field, ''), reverse=reverse)
        self.save_data()

    def add_actor(self, actor_data):
        if self.data:
            new_id = max(actor.get('ID', 0) for actor in self.data) + 1
        else:
            new_id = 1

        actor_data['ID'] = new_id
        self.data.append(actor_data)
        self.save_data()
        return new_id

    def update_actor(self, actor_id, new_data):
        for i, actor in enumerate(self.data):
            if actor.get('ID') == actor_id:
                new_data['ID'] = actor_id
                self.data[i] = new_data
                self.save_data()
                return True
        return False

    def delete_actor(self, actor_id):
        for i, actor in enumerate(self.data):
            if actor.get('ID') == actor_id:
                del self.data[i]
                self.save_data()
                return True
        return False

    def get_count(self):
        return len(self.data)


class Actor_rep_yaml(Actor_rep_json):
    def __init__(self, filename="actors.yaml"):
        super().__init__(filename)

    def _load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f) or []
        except (FileNotFoundError, yaml.YAMLError):
            self.data = []

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f, allow_unicode=True,
                      default_flow_style=False, sort_keys=False)

class ActorShort:
    def __init__(self, actor_id, fam=None, staz=None):
        if isinstance(actor_id, str) and actor_id.strip().startswith('{'):
            data = self.__parse_json_string(actor_id)
            actor_id = data['ID']
            fam = data['Фамилия']
            staz = data['Стаж']

        self.__validate_actor_id(actor_id)
        self.__actor_id = actor_id
        self.__validate_fam(fam)
        self.__fam = fam
        self.__validate_staz(staz)
        self.__staz = staz

    def __parse_json_string(self, json_string):
        try:
            data = json.loads(json_string)
            required_fields = ['ID', 'Фамилия', 'Стаж']
            for field in required_fields:
                if field not in data:
                    raise ValueError("Отсутствуют необходимые поля")
            return data
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON формат")

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
    def __validate_fam(fam):
        if not fam or not isinstance(fam, str) or not fam.strip():
            raise ValueError("Фамилия должна быть непустой строкой")

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
    def __init__(self, short_actor, fio=None, zvan=None, awards=None):
        if isinstance(short_actor, str) and short_actor.strip().startswith('{'):
            data = self.__parse_full_json_string(short_actor)
            short_from_json = ActorShort(data['ID'], data['Фамилия'], data['Стаж'])
            short_actor = short_from_json
            fio = data['ФИО']
            zvan = data.get('Звание', [])
            awards = data.get('Награды', [])

        self.__validate_fam(short_actor.get_fam())
        super().__init__(short_actor.get_actor_id(), short_actor.get_fam(), short_actor.get_staz())
        self.__validate_fio(fio)
        self.__fio = fio
        self.__zvan = self.__prepare_list(zvan, "звание")
        self.__awards = self.__prepare_list(awards, "награда")

    def __parse_full_json_string(self, json_string):
        try:
            data = json.loads(json_string)
            required_fields = ['ID', 'Фамилия', 'Стаж', 'ФИО']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Отсутствует поле {field} в JSON")
            return data
        except json.JSONDecodeError:
            raise ValueError("Некорректный JSON формат")

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


class Actor_rep_DB:
    _instance = None
    _connection = None

    def __new__(cls, db_config=None):
        if cls._instance is None:
            cls._instance = super(Actor_rep_DB, cls).__new__(cls)
            if db_config:
                cls._instance._initialize(db_config)
        return cls._instance

    def _initialize(self, db_config):
        self.db_config = db_config
        self._create_connection()

    def _create_connection(self):
        try:
            self._connection = psycopg2.connect(**self.db_config)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
            self._connection = None

    def _execute_query(self, query, params=None):
        try:
            if not self._connection:
                raise Exception("Нет подключения к БД")

            with self._connection.cursor() as cursor:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    self._connection.commit()
                    return cursor.rowcount
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None

    def _execute_insert_returning(self, query, params):
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.fetchone()[0]
                self._connection.commit()
                return new_id
        except Exception as e:
            print(f"Ошибка при выполнении INSERT: {e}")
            return -1

    def get_by_id(self, actor_id):
        query = """
        SELECT id, fam, staz, fio, zvan, awards 
        FROM actors 
        WHERE id = %s
        """
        result = self._execute_query(query, (actor_id,))  

        if result and len(result) > 0:
            row = result[0]
            return {
                'ID': row[0],
                'Фамилия': row[1],
                'Стаж': row[2],
                'ФИО': row[3],
                'Звание': row[4] or [],
                'Награды': row[5] or []
            }
        return None

    def get_k_n_short_list(self, k, n):
        offset = (n - 1) * k
        query = """
        SELECT id, fam, staz 
        FROM actors 
        ORDER BY id 
        LIMIT %s OFFSET %s
        """
        result = self._execute_query(query, (k, offset))  
        short_list = []
        if result:
            for row in result:
                short_actor = {
                    'ID': row[0],
                    'Фамилия': row[1],
                    'Стаж': row[2]
                }
                short_list.append(short_actor)

        return short_list

    def add_actor(self, actor_data):
        query = """
        INSERT INTO actors (fam, staz, fio, zvan, awards) 
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING id
        """
        new_id = self._execute_insert_returning(query, ( 
            actor_data['Фамилия'],
            actor_data['Стаж'],
            actor_data['ФИО'],
            actor_data.get('Звание', []),
            actor_data.get('Награды', [])
        ))
        return new_id

    def update_actor(self, actor_id, new_data):
        query = """
        UPDATE actors 
        SET fam = %s, staz = %s, fio = %s, zvan = %s, awards = %s 
        WHERE id = %s
        """
        rows_affected = self._execute_query(query, ( 
            new_data['Фамилия'],
            new_data['Стаж'],
            new_data['ФИО'],
            new_data.get('Звание', []),
            new_data.get('Награды', []),
            actor_id
        ))
        return rows_affected > 0 if rows_affected else False

    def delete_actor(self, actor_id):
        query = "DELETE FROM actors WHERE id = %s"
        rows_affected = self._execute_query(query, (actor_id,))
        return rows_affected > 0 if rows_affected else False

    def get_count(self):
        query = "SELECT COUNT(*) FROM actors"
        result = self._execute_query(query) 
        return result[0][0] if result else 0

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            self._instance = None

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'actors',
        'user': 'postgres',
        'password': 'postpass',
        'port': 5432
    }

    db_repo1 = Actor_rep_DB(db_config)
    db_repo2 = Actor_rep_DB()

    print(f"Это один и тот же объект: {db_repo1 is db_repo2}")

    test_actor = {
        'Фамилия': 'Круз',
        'Стаж': 20,
        'ФИО': 'Круз Том Сергеевич',
        'Звание': ['Заслуженный артист РФ'],
        'Награды': ['Оскар']
    }

    new_id = db_repo1.add_actor(test_actor)
    print(f"Добавлен актер с ID: {new_id}")
    actor = db_repo1.get_by_id(new_id)
    print(f"Актер с ID {new_id}: {actor['ФИО']}")
    short_list = db_repo1.get_k_n_short_list(4, 2)
    for actor in short_list:
        print(f"ID: {actor['ID']}, Фамилия: {actor['Фамилия']}, Стаж: {actor['Стаж']}")

    count = db_repo1.get_count()
    print(f"Общее количество актеров: {count}")
    updated_data = test_actor.copy()
    updated_data['Стаж'] = 21
    updated = db_repo1.update_actor(new_id, updated_data)
    print(f"Актер с ID {new_id} обновлен: {updated}")

    deleted = db_repo1.delete_actor(new_id)
    print(f"Актер с ID {new_id} удален: {deleted}")

    db_repo1.close_connection()
