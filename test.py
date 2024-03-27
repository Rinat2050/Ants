class Engine:
    def __init__(self, type, horsepower):
        self.type = type
        self.horsepower = horsepower
        self.transmission = None
        self.wheels = [Wheel(i) for i in range(4)]

    def set_transmission(self, transmission):
        self.transmission = transmission
        print(f"The {self.type} engine is paired with a {transmission.type} transmission")

    def start(self):
        print(f"The {self.type} engine starts with {self.horsepower} horsepower")

    def accelerate(self, speed):
        if self.transmission is not None:
            gear = self.transmission.get_gear(speed)
            print(f"The {self.type} engine accelerates in {gear} gear to {speed} km/h")
        else:
            print("No transmission set")

    def power_wheels(self):
        print(f"The {self.type} engine powers all wheels")
        for wheel in self.wheels:
            wheel.rotate()


class Transmission:
    def __init__(self, type, gears):
        self.type = type
        self.gears = gears

    def get_gear(self, speed):
        if speed < 20:
            return self.gears[0]
        elif speed < 40:
            return self.gears[1]
        else:
            return self.gears[2]


class Wheel:
    def __init__(self, number):
        self.number = number

    def rotate(self):
        print(f"Wheel {self.number} is rotating")
class Car:
    def __init__(self, make, model, engine, transmission):
        self.make = make
        self.model = model
        self.engine = engine
        self.transmission = transmission

    def start(self):
        self.engine.start()

    def move(self, speed):
        self.engine.accelerate(speed)
        self.engine.power_wheels()


# Создаем объекты трансмиссии, двигателя и автомобиля
transmission = Transmission("Automatic", ["D", "N", "R"])
engine = Engine("V8", 500)
engine.set_transmission(transmission)
car = Car("Ford", "Mustang", engine, transmission)

# Запускаем автомобиль
car.start()

# Двигаемся
car.move(60)
