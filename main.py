from pygame import *
import random

init()

size = 600, 800
window = display.set_mode(size)
clock = time.Clock()


class Sprite:
    def __init__(self, img, x, y, width, height):
        self.img = transform.scale(image.load(img), (width, height))
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
    if keys[K_d]:
        player.rect.x += 5
    if keys[K_a]:
        player.rect.x -= 5


player = Sprite('player_car.png', 200, 600, 55, 100)

roads = list()
y = -95
for i in range(11):
    road = Sprite('road.png', 50, y, 500, 100)
    roads.append(road)
    y += 95

square_cars = ['grey_car.png', 'red_car.png', 'orange_car.png', 'green_car.png']
little_track = ['red_track.png', 'green_track.png']

car_list = ['grey_car.png', 'red_car.png', 'red_track.png', 'green_track.png', 'orange_car.png', 'green_car.png']


def spaw_car():
    cars = list()
    y_car = random.randint(-900, -100)
    for i in range(20):
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


cars = spaw_car()

font1 = font.Font(None, 40)
high_score = 0
score = 0
speed = 12
finish = False
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish:
                score = 0
                cars = spaw_car()
                finish = False
    window.fill((0, 200, 200))

    if not finish:
        for road in roads:
            road.reset()
            road.rect.y += speed
            if road.rect.y >= 900:
                road.rect.y = -95

        for car in cars:
            car.update()
            car.reset()
            for other_car in cars:
                if car != other_car and car.rect.colliderect(other_car.rect):
                    car.rect.y -= car.speed * 2
                    car.speed = other_car.speed

            if player.rect.colliderect(car.rect):
                finish = True
                if score > high_score:
                    high_score = score
        if score == 20:
            car = Car('big_blue_track.png', random.choice([80, 180, 280, 380]), random.randint(-900, -100), 60, 200)
            cars.append(car)
            score += 1

        score_text = font1.render(f'Обігнали: {score}', True, (0, 0, 0))
        window.blit(score_text, (10, 20))

        update()
        player.reset()

    if finish:
        score_text = font1.render(f'Обігнали: {score}', True, (0, 0, 0))
        window.blit(score_text, (230, 300))
        high_score_text = font1.render(f'Рекорд: {high_score}', True, (0, 0, 0))
        window.blit(high_score_text, (235, 360))
        text = font1.render('тисни пробіл для початку', True, (0, 0, 0))
        window.blit(text, (150, 420))

    display.update()
    clock.tick(60)
