import json

import pygame as pg
import random

# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
FPS = 80

SIZE = (900, 550)

TOY_SIZE = 100

DOG_WIDTH = 310
DOG_HEIGHT = 500

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

DOG_Y = 100

ICON_SIZE = 80
PADDING = 5

MENU_NAV_XPAD = 90
MENU_NAV_YPAD = 130

FOOD_SIZE = 200

font = pg.font.Font(None, 40)
medium_font = pg.font.Font(None, 35)
mini_font = pg.font.Font(None, 15)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))

    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Food:
    def __init__(self, name, price, file, satiety, medecine_power=0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medecine_power = medecine_power
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)


class FoodMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [
            Food("лекарство", 175, "images/food/medicine.png", 0, medecine_power=25),
            Food("элитный корм", 125, "images/food/dog food elite.png", 25, medecine_power=5),
            Food("корм", 60, "images/food/dog food.png", 10, medecine_power=5),
            Food("мясо", 45, "images/food/meat.png", 20)
        ]

        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vpered_button = Button("Вперед", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH,
                                    SCREEN_HEIGHT - MENU_NAV_YPAD,
                                    width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                    func=self.to_back
                                    )
        self.buy_button = Button("Скормить", 350, 380,
                                 func=self.buy)

        self.nazad_button = Button("Назад",
                                   SCREEN_WIDTH - MENU_NAV_XPAD * 2 - BUTTON_WIDTH * 3,
                                   SCREEN_HEIGHT - MENU_NAV_YPAD,
                                   width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                   func=self.to_next_
                                   )

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100

            self.game.health += self.items[self.current_item].medecine_power
            if self.game.health > 100:
                self.game.health = 100

    def to_next_(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

    def to_back(self):
        if self.current_item != 0:
            self.current_item -= 1

    def update(self):
        self.vpered_button.update()
        self.nazad_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        if self.game.mode == "Food menu":
            self.vpered_button.is_clicked(event)
            self.nazad_button.is_clicked(event)
            self.buy_button.is_clicked(event)

    def draw(self, screen):

        screen.blit(text_render(self.items[self.current_item].name), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(self.menu_page, (0, 0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        screen.blit(text_render(self.items[self.current_item].price), (437, 164))

        self.vpered_button.draw(screen)
        self.nazad_button.draw(screen)
        self.buy_button.draw(screen)


class Item:
    def __init__(self, name, price, file, is_put_on, is_bought):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on
        self.file = file
        self.image = load_image(file, DOG_WIDTH // 1.7, DOG_HEIGHT // 1.7)
        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []

        for item in data:
            self.items.append(Item(*item.values()))

        self.current_item = 0

        # for i in self.items:
        #     if self.current_item % 2 != 0:
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button("Вперед", SCREEN_WIDTH - MENU_NAV_XPAD - BUTTON_WIDTH,
                                  550 - 130,
                                  width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                  func=self.to_next
                                  )
        self.clothes_button = Button("Купить", 350, 380,
                                     func=self.buy)
        self.put_on_button = Button(
            "надеть", SCREEN_WIDTH - MENU_NAV_XPAD * 2 - BUTTON_WIDTH * 3,
                      SCREEN_HEIGHT - MENU_NAV_YPAD - MENU_NAV_XPAD,
            width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
            func=self.put_on
        )

        self.backward_button = Button("Назад",
                                      SCREEN_WIDTH - MENU_NAV_XPAD * 2 - BUTTON_WIDTH * 3,
                                      SCREEN_HEIGHT - MENU_NAV_YPAD,
                                      width=int(BUTTON_WIDTH // 1.2), height=int(BUTTON_HEIGHT // 1.2),
                                      func=self.to_last
                                      )

    def buy(self):
        print(self.game.money, self.current_item, self.items[self.current_item].price,
              self.items[self.current_item].is_bought)

        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
            print(self.current_item)

    def to_last(self):
        if self.current_item != 0:
            self.current_item -= 1
            print(self.current_item)

    def put_on(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on

    def update(self):
        self.next_button.update()
        self.backward_button.update()
        self.clothes_button.update()
        self.put_on_button.update()

    def is_clicked(self, event):
        if self.game.mode == "Clothes menu":
            self.next_button.is_clicked(event)
            self.backward_button.is_clicked(event)
            self.clothes_button.is_clicked(event)
            self.put_on_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))

        if self.items[self.current_item].is_bought:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))

        screen.blit(text_render(self.items[self.current_item].price), (437, 164))

        if self.items[self.current_item].is_put_on == True:
            screen.blit(text_render("Надето"), (650, 116))

        else:
            screen.blit(text_render("Снято"), (658, 116))

        if self.items[self.current_item].is_bought == True:
            screen.blit(text_render("Куплено"), (640, 184))

        else:
            screen.blit(text_render("Отсутвует"), (638, 184))
            self.clothes_button.draw(screen)

        if self.items[self.current_item].is_put_on == True:
            self.put_on_button.draw(screen)

        else:
            self.put_on_button.draw(screen)

        self.next_button.draw(screen)
        self.backward_button.draw(screen)


class Button:
    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_font=font, func=None):
        self.idle_image = load_image("images/button.png", width, height)
        self.pressed_image = load_image("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.func = func

        self.text_font = text_font
        self.is_pressed = False
        self.text = self.text_font.render(str(text), True, "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image
            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.is_pressed = True
                    self.func()
                except:
                    pass


        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Toy(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image(image, TOY_SIZE, TOY_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(MENU_NAV_XPAD, SCREEN_WIDTH - MENU_NAV_XPAD - self.image.get_width())
        self.rect.y = 30

    # random.randint(MENU_NAV_YPAD, SCREEN_HEIGHT - MENU_NAV_YPAD - self.image.get_height())
    def update(self):
        self.rect.y += 3
        if self.rect.y >= SIZE[1]:
            self.kill()


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/dog.png", DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - MENU_NAV_YPAD - 10

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= 8

        if keys[pg.K_d]:
            self.rect.x += 8

        if keys[pg.K_w]:
            self.rect.y -= 8

        if keys[pg.K_s]:
            self.rect.y += 8


class MiniGame:
    def __init__(self, game):
        self.game = game
        self.image = load_image("images/dog.png", DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.dog_image = load_image("images/dog.png", DOG_WIDTH // 2, DOG_HEIGHT // 2)
        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect = self.image.get_rect()
        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def new_game(self):
        self.toys = pg.sprite.Group()
        self.dog = Dog()
        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def update(self):
        self.dog.update()
        self.toys.update()

        if random.randint(0, 100) >= 97:
            self.toys_image = "images/toys/ball.png"
            r = random.randint(0, 100)
            if r < 33:
                self.toys_image = "images/toys/ball.png"
                self.toy = Toy(self.toys_image)

            elif 33 <= r < 98:
                self.toys_image = "images/toys/blue bone.png"
                self.toy = Toy(self.toys_image)

            else:
                self.toys_image = "images/toys/red bone.png"
                self.toy = Toy(self.toys_image)

            self.toys.add(self.toy)
            self.toys.update()

        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score // 2)
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.dog.image, self.dog.rect)
        screen.blit(text_render(self.score), (MENU_NAV_XPAD + 20, 80))
        self.toys.draw(screen)


class Game:
    def __init__(self):
        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        with open("safe.json", encoding="utf-8") as f:
            data = json.load(f)

        self.happiness = data["happiness"]  # счастье питомца
        self.satiety = data["satiety"]  # сытость питомца
        self.health = data["health"]  # здоровье питомца
        self.money = data["money"]  # деньги
        self.coins_per_second = data["coins_per_second"]
        self.cost_of_upgrade = {}
        for key, value in data["cost_of_upgrade"].items():
            self.cost_of_upgrade[int(key)] = value

        self.DECREASE = pg.USEREVENT + 2
        self.DCREASE = pg.USEREVENT + 3
        self.DREASE = pg.USEREVENT + 4

        self.mode = "Main"

        self.pet = load_image("images/dog.png", 310, 500)

        self.back_ground = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)

        self.hunger_image = load_image("images/satiety.png", ICON_SIZE, ICON_SIZE)

        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)

        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDTH - BUTTON_WIDTH - PADDING

        self.eat_button = Button("еда", button_x, PADDING + ICON_SIZE + 5, func=self.food_menu_on)

        self.clothes_button = Button("одежда", button_x, PADDING + ICON_SIZE * 2,
                                     func=self.clothes_menu_on)

        self.games_button = Button("игры", button_x, PADDING + ICON_SIZE * 3 - 5, func=self.game_on)

        self.upgrade_button = Button("Улучшить", SCREEN_WIDTH - ICON_SIZE, 0, width=BUTTON_WIDTH // 3,
                                     height=BUTTON_HEIGHT // 3, text_font=mini_font, func=self.increase_money)

        self.death_screen = load_image("img_.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.buttons = [self.eat_button, self.clothes_button, self.games_button, self.upgrade_button]

        self.clothes_menu = ClothesMenu(self, data["clothes"])

        pg.time.set_timer(self.DECREASE, 5000)
        # ниже находится кликер, 1000 это 1 секунда можно поменять это число
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.food_menu = FoodMenu(self)

        self.mini_game = MiniGame(self)

        self.clock = pg.time.Clock()

        self.run()

    def increase_money(self):
        for cost, check in self.cost_of_upgrade.items():
            if not check and self.money >= cost:
                self.coins_per_second += 1
                self.money -= cost
                self.cost_of_upgrade[cost] = True
                break

    def clothes_menu_on(self):
        if self.mode == "Main":
            self.mode = "Clothes menu"


    def food_menu_on(self):
        if self.mode == "Main":
            self.mode = "Food menu"


    def game_on(self):
        self.mode = "Mini Game"
        self.mini_game.new_game()


    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)


    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "DEATH":
                    data = {

                        "happiness": 50,
                        "satiety": 40,
                        "health": 40,
                        "money": 25,
                        "coins_per_second": 1,
                        "cost_of_upgrade": {
                            "100": False,
                            "1000": False,
                            "5000": False,
                            "10000": False
                        },
                        "clothes": [
                            {
                                "name": "синяя футболка",
                                "price": 45,
                                "image": "images/items/blue t-shirt.png",
                                "is_put_on": False,
                                "is_bought": False
                            },
                            {
                                "name": "ботинки",
                                "price": 50,
                                "image": "images/items/boots.png",
                                "is_put_on": False,
                                "is_bought": False
                            },
                            {
                                "name": "шляпа",
                                "price": 35,
                                "image": "images/items/hat.png",
                                "is_put_on": False,
                                "is_bought": False
                            }
                        ]
                    }

                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_per_second": self.coins_per_second,
                        "cost_of_upgrade": {
                            "100": self.cost_of_upgrade[100],
                            "1000": self.cost_of_upgrade[1000],
                            "5000": self.cost_of_upgrade[5000],
                            "10000": self.cost_of_upgrade[10000]
                        },
                        "clothes": []

                    }
                    for item in self.clothes_menu.items:
                        data["clothes"].append({
                            "name": item.name,
                            "price": item.price,
                            "image": item.file,
                            "is_put_on": item.is_put_on,
                            "is_bought": item.is_bought})

                with open("safe.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)

                pg.quit()
                exit()

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)

                if chance <= 5:
                    self.satiety -= 1

                elif 5 < chance <= 9:
                    self.happiness -= 1

                else:
                    self.health -= 1

            if event.type == self.DCREASE:
                self.health -= 1
                self.happiness -= 1

            if event.type == self.DREASE:
                self.health -= 1

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second

            if event.type == pg.MOUSEBUTTONDOWN:
                self.money += 1

            for button in self.buttons:
                button.is_clicked(event)

            if self.mode != "Main":
                self.clothes_menu.is_clicked(event)
                self.food_menu.is_clicked(event)


    def update(self):
        if self.mode == "Clothes menu":
            self.clothes_menu.update()

        elif self.mode == "Food menu":
            self.food_menu.update()

        elif self.mode == "Mini Game":
            self.mini_game.update()

        else:
            for button in self.buttons:
                button.update()

        if self.satiety <= 30:
            pg.time.set_timer(self.DCREASE, 2500)

        if self.satiety <= 0:
            self.mode = "DEATH"

        if self.happiness <= 30:
            pg.time.set_timer(self.DREASE, 3000)

        if self.satiety < 1:
            self.mode = "HUNGER DEATH"

        if self.happiness < 1:
            self.mode = "DEPRESSION"

        if self.health < 1:
            self.mode = "DEATH"


    def draw(self):
        self.screen.blit(self.back_ground, (0, 0))

        self.screen.blit(self.happiness_image, (PADDING, PADDING))
        self.screen.blit(text_render(self.happiness), (PADDING + ICON_SIZE, PADDING * 6))
        self.screen.blit(text_render(self.satiety), (PADDING + ICON_SIZE, PADDING * 6 + 70))
        self.screen.blit(text_render(self.health), (PADDING + ICON_SIZE, PADDING * 6 + 135))
        self.screen.blit(text_render(self.money), (760, 48))

        self.screen.blit(self.pet, (310, 150))
        self.screen.blit(self.hunger_image, (PADDING, PADDING + 65))
        self.screen.blit(self.health_image, (PADDING, PADDING + 130))
        self.screen.blit(self.money_image, (800, 20))

        self.clothes_button.draw(self.screen)

        self.games_button.draw(self.screen)

        self.eat_button.draw(self.screen)

        self.upgrade_button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, (310, 150))

        if self.mode == "Clothes menu":
            self.clothes_menu.draw(self.screen)

        if self.mode == "Food menu":
            self.food_menu.draw(self.screen)

        if self.mode == "Mini Game":
            self.mini_game.draw(self.screen)

        if self.mode == "DEATH":
            self.screen.blit(self.death_screen, (0, 0))
            self.clock.tick(10)
        self.clock.tick(FPS)
        pg.display.flip()


if __name__ == "__main__":
    Game()

# {
#   "happiness": 50,
#   "satiety": 40,
#   "health": 40,
#   "money": 25,
#   "coins_per_second": 1,
#   "cost_of_upgrade": {
#     "100": false,
#     "1000": false,
#     "5000": false,
#     "10000": false
#   },
#   "clothes": [
#     {
#       "name": "синяя футболка",
#       "price": 45,
#       "image": "images/items/blue t-shirt.png",
#       "is_put_on": false,
#       "is_bought": false
#     },
#         {
#       "name": "ботинки",
#       "price": 50,
#       "image": "images/items/boots.png",
#       "is_put_on": false,
#       "is_bought": false
#     },
#         {
#       "name": "шляпа",
#       "price": 35,
#       "image": "images/items/hat.png",
#       "is_put_on": false,
#       "is_bought": false
#     }
#   ]
# }
# полные базовые настройки
