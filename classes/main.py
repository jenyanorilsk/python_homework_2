import os
import csv


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):

        # проверка типа автомобиля
        if car_type not in ['car', 'truck', 'spec_machine']:
            raise ValueError("wrong car type")
        self.car_type = car_type

        # проверка корректности бренда
        if not isinstance(brand, str):
            raise ValueError('brand must be a valid string')
        if len(brand.strip()) == 0:
            raise ValueError('brand must be a valid string')
        # ещё можно проверять на вхождение в список валидных брендов,
        # но у нас его нет
        self.brand = brand

        # проверка имени файла фотографии
        if not isinstance(photo_file_name, str):
            raise ValueError('filename must be a valid string')
        if len(photo_file_name.strip()) == 0:
            raise ValueError('filename must be a valid string')
        # здесь ещё можно проверять расширения или существование файла,
        # но такая задача не обговорена условиями
        self.photo_file_name = photo_file_name

        # проверка грузоподъёмности
        try:
            self.carrying = float(carrying)
        except ValueError:
            raise ValueError('carrying must be a number')
        # по условиям нет ограничений на диапазон допустимых значений,
        # но здесь напрашивается из здравого смысла
        if self.carrying <= 0:
            raise ValueError('carrying must be positive')

        pass

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)
        pass

    # некрасиво так делать, но в этой задаче, кмк ничего смертельного:
    # метод возвращает имена параметоров, которые необходимы классу
    # правильно вместо этого - принимать словарь и парсить его в конструкторе, но тогда
    # сложно будет проиллюстрировать идею иерархии классов, переопределения и вот этого всего
    @staticmethod
    def get_contsr_attr():
        return ['brand', 'photo_file_name', 'carrying']

    # просто метод, выводит значения аттрибутов
    def print_info(self):
        print('brand:', self.brand)
        print('photo:', self.photo_file_name)
        print('carrying:', self.carrying)


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__('car', brand, photo_file_name, carrying)
        try:
            self.passenger_seats_count = int(passenger_seats_count)
        except ValueError:
            raise ValueError('wrong value of passenger seats count')
        if self.passenger_seats_count <= 0:
            raise ValueError('passenger seats count must be positive')
        pass

    # переопределение
    @staticmethod
    def get_contsr_attr():
        # получим параметры для родителя и добавим свои
        return [*super(Car, Car).get_contsr_attr(), 'passenger_seats_count']

    # просто метод, выводит значения аттрибутов
    def print_info(self):
        super(Car, self).print_info()
        print('seats:', self.passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__('truck', brand, photo_file_name, carrying)

        if not isinstance(body_whl, str):
            raise ValueError('body measurements must be a string')

        self.body_length = 0
        self.body_width = 0
        self.body_height = 0

        try:
            # разобьём строку и получим числа
            floats = [float(x.strip()) for x in body_whl.lower().split('x')]
            # должно быть ровно 3 неотрицательных числа
            # по условиям нет ограничений на диапазон допустимых значений,
            # но здесь напрашивается из здравого смысла
            if len(floats) == 3 and not any((x < 0 for x in floats)):
                self.body_length, self.body_width, self.body_height = floats
        except ValueError:
            # если в строке были не числа, то
            # ничего делать не нужно - у нас уже нули по-умолчанию
            pass

        pass

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    # переопределение
    @staticmethod
    def get_contsr_attr():
        # получим параметры для родителя и добавим свои
        return [*super(Truck, Truck).get_contsr_attr(), 'body_whl']

    # просто метод, выводит значения аттрибутов
    def print_info(self):
        super(Truck, self).print_info()
        print('l x w x h:', f'{self.body_length} x {self.body_width} x {self.body_height}')
        print('volume:', self.get_body_volume())


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__('spec_machine', brand, photo_file_name, carrying)
        self.extra = extra
        pass

    @staticmethod
    def get_contsr_attr():
        # получим аттрибуты родителя и добавим свои
        return [*super(SpecMachine, SpecMachine).get_contsr_attr(), 'extra']

    # просто метод, выводит значения аттрибутов
    def print_info(self):
        super(SpecMachine, self).print_info()
        print('extra:', self.extra)


# что-то вроде фабрики
def create_car(args_dict):

    car_type = args_dict['car_type']
    # определим параметры, которые нужны конструкторам наших классов
    # чтобы проще передать эти параметры в конструкторы
    car_params = Car.get_contsr_attr()
    truck_params = Truck.get_contsr_attr()
    spec_params = SpecMachine.get_contsr_attr()

    if car_type == 'car':
        return Car(**{key: args_dict.get(key, None) for key in car_params})
    if car_type == 'truck':
        return Truck(**{key: args_dict.get(key, None) for key in truck_params})
    if car_type == 'spec_machine':
        return SpecMachine(**{key: args_dict.get(key, None) for key in spec_params})
    raise ValueError('Wrong car type')


def get_car_list(csv_filename):
    result = []
    with open(csv_filename) as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            try:
                result.append(create_car(row))
            except ValueError:
                # игнорируем ошибку
                continue
    return result
    pass


if __name__ == '__main__':

    filename = './cars_list.csv'
    car_list = get_car_list(filename)

    print('Total items in list:', len(car_list))
    for i, item in enumerate(car_list):
        print(i + 1, item)
        item.print_info()
