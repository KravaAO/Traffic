from pygame import *
import random

init()

size = 600, 800
window = display.set_mode(size)
clock = time.Clock()


class Sprite:
    def __init__(self, img, x, y, width, height):
        self.img = transform.scale(image.load(f'img/{img}'), (width, height))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3, 6)

    def reset(self):
        window.blit(self.img, (self.rect.x, self.rect.y))


class Car(Sprite):
    def update(self):
        global score
        self.rect.y += self.speed
        if self.rect.y >= 900:
            self.rect.y = random.randint(-900, -100)
            self.rect.x = random.choice([80, 180, 280, 380, 470])
            score += 1


def update():
    keys = key.get_pressed()
    if keys[K_d] and player.rect.x <= 500:
        player.rect.x += 5
    if keys[K_a] and player.rect.x >= 80:
        player.rect.x -= 5


player = Sprite('player_car.png', 200, 600, 55, 100)
player_shadow = Sprite('player_shadow.png', 196, 600, 60, 105)

roads = list()
y = -95
for i in range(11):
    road = Sprite('road.png', 50, y, 500, 100)
    roads.append(road)
    y += 95

square_cars = ['grey_car.png', 'red_car.png', 'orange_car.png', 'green_car.png']
little_track = ['red_track.png', 'green_track.png']

car_list = ['grey_car.png', 'red_car.png', 'red_track.png', 'green_track.png', 'orange_car.png', 'green_car.png']


def spaw_car(count):
    cars = list()
    y_car = random.randint(-900, -100)
    for i in range(count):
        type_car = random.choice(car_list)
        if type_car in little_track:
            width = 60
            height = 120
        elif type_car in square_cars:
            width = 55
            height = 100
        car = Car(type_car, random.choice([80, 180, 280, 380]), y_car, width, height)
        cars.append(car)
        y_car = random.randint(-900, -100)
    return cars


trashs = list()
for i in range(random.randint(2, 7)):
    trash = Sprite('trash_botle.png', random.choice([10, 560]), random.randint(-100, 0), 30, 45)
    trashs.append(trash)

cars = spaw_car(8)

font1 = font.Font(None, 50)
high_score = 0
score = 0
speed = 12
finish = False
logo_fuel = Sprite('fuel.png', 565, 70, 20, 20)
fuel = 200
fuel_score = 0
bak_fuels = list()
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish:  # рестарт гри на пробіл
                score = 0
                cars = spaw_car(8)
                finish = False
                fuel = 200
    window.fill((0, 170, 0))

    if not finish:  # поки незакінчиться бензин або невріжиться у машину
        for trash in trashs:
            trash.rect.y += speed
            trash.reset()
            if trash.rect.y >= 900:
                trash.rect.y = random.randint(-2000, -900)

        for road in roads:
            road.reset()
            road.rect.y += speed
            if road.rect.y >= 900:
                road.rect.y = -95

        for f in bak_fuels:
            f.rect.y += speed
            f.reset()
            if player.rect.colliderect(f.rect):
                if fuel + 100 <= 200:
                    fuel += 100
                else:
                    fuel = 200
                bak_fuels.remove(f)

        # Логіка автомобілей
        for car in cars:
            car.update()
            car.reset()
            for other_car in cars:
                if car != other_car:
                    # Якщо машини зіштовхуються
                    if car.rect.colliderect(other_car.rect):
                        # Зниження швидкості при виявленні колізії
                        if car.speed > other_car.speed:
                            car.speed = max(other_car.speed - 1, 1)

                        # Спробувати змінити позицію для уникнення зіткнення
                        if car.rect.y < other_car.rect.y:
                            car.rect.y -= 10  # Плавно відсунути машину вверх
                        else:
                            car.rect.y += 10  # Плавно відсунути машину вниз
            if player.rect.colliderect(car.rect):
                finish = True
                if score > high_score:
                    high_score = score

        # складність у грі та відображення рахунку
        if score in [15, 20, 25, 30, 35]:
            car = Car('big_blue_track.png', random.choice([80, 180, 280, 380]), random.randint(-900, -100), 60, 200)
            for i in range(random.randint(1, 2)):
                img_fuel = Sprite('fuel.png', random.choice([80, 180, 280, 380]), random.randint(-200, -50), 50, 50)
                bak_fuels.append(img_fuel)
            cars.append(car)
            score += 1
        if fuel == 70:
            for i in range(random.randint(1, 3)):
                img_fuel = Sprite('fuel.png', random.choice([80, 180, 280, 380]), random.randint(-200, -50), 50, 50)
                bak_fuels.append(img_fuel)

        score_text = font1.render(f'{score}', True, (0, 0, 0))
        window.blit(score_text, (290, 20))

        # відображення палива та його логіка у грі
        rect_fuel = Rect(560, 100, 30, fuel)
        if fuel >= 150:
            color = (0, 255, 0)
        elif fuel >= 75:
            color = (255, 250, 0)
        else:
            color = (255, 0, 0)
        draw.rect(window, color, rect_fuel, width=0, border_radius=15)
        draw.rect(window, (0, 0, 0), Rect(560, 100, 30, 200), width=3, border_radius=15)
        fuel -= 0.1
        if fuel <= 5:
            finish = True
        logo_fuel.reset()

        # відображення гравця
        update()
        player_shadow.reset()
        player_shadow.rect.y = player.rect.y
        player_shadow.rect.x = player.rect.x
        player.reset()

    if finish:
        score_text = font1.render(f'Обігнали: {score}', True, (0, 0, 0))
        window.blit(score_text, (230, 300))
        high_score_text = font1.render(f'Рекорд: {high_score}', True, (0, 0, 0))
        window.blit(high_score_text, (235, 360))
        text = font1.render('тисни пробіл для початку', True, (0, 0, 0))
        window.blit(text, (100, 420))

    display.update()
    clock.tick(60)
