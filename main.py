import random
from pygame import mixer
import pygame


def create_obstacles(dif):
    obstacles = []
    y = 50
    if dif == "easy":
        for i in range(2):
            x = 5
            for j in range(10):
                obstacles.append(Obstacle(0, x, y, obstacle_width, obstacle_height))
                x += obstacle_width + 5
            y += obstacle_height + 10
    elif dif == "medium":
        for i in range(3):
            x = 5
            for j in range(10):
                obstacles.append(Obstacle(2 - i, x, y, obstacle_width, obstacle_height))
                x += obstacle_width + 5
            y += obstacle_height + 10
    elif dif == "hard":
        for i in range(5):
            x = 5
            for j in range(10):
                obstacles.append(Obstacle(4 - i, x, y, obstacle_width, obstacle_height))
                x += obstacle_width + 5
            y += obstacle_height + 10
    return obstacles

def draw_lose():
    screen.blit(txtlose, (WIDTH / 3.5, 250))
    pygame.draw.rect(screen, (255, 0, 0), (170, 350, 260, 100), width=0)
    screen.blit(txtplay, (WIDTH / 3.5 + 15, 370))
    mixer.music.stop()

def draw_win():
    screen.blit(txtwin, (WIDTH / 3.5 + 15, 250))
    pygame.draw.rect(screen, (255, 0, 0), (170, 350, 260, 100), width=0)
    screen.blit(txtplay, (WIDTH / 3.5 + 15, 370))
    mixer.music.stop()

def play_button(x, y, game_status):
    if 170 < x < 430 and 350 < y < 450:
        return "interlude"
    return game_status

def new_game(dif):
    obstacles = create_obstacles(dif)
    mixer.music.play()
    create_obstacles(dif)
    health = 3
    counter = 0
    start_x, start_y = WIDTH // 2, 350
    start_speed_x, start_speed_y = 4, 4
    last_collision = None
    ball = Ball(10, start_x, start_y, start_speed_x, start_speed_y)
    buffs = [Buffs(20, random.randint(150, 500), -1500, 1, 'health'),
             Buffs(20, random.randint(150, 500), -1500, 1, 'platform'),
             Buffs(20, random.randint(150, 500), -1500, 1, 'ball')]
    buff_index = random.randint(0, len(buffs) - 1)
    is_active = 0
    return obstacles, health, counter, ball, start_x, start_y, start_speed_x, start_speed_y, last_collision, "game", buffs, buff_index, is_active

def draw_buttons():
    pygame.draw.rect(screen, colors[0], (150, 100, 300, 100), width=0)
    pygame.draw.rect(screen, colors[1], (150, 225, 300, 100), width=0)
    pygame.draw.rect(screen, colors[2], (150, 350, 300, 100), width=0)

    screen.blit(txteasy, (245, 125))
    screen.blit(txtmedium, (225, 250))
    screen.blit(txthard, (245, 375))
def check_click(x, y):
    if 150 < x < 450 and 100 < y < 200:
        return "easy", 20
    elif 150 < x < 450 and 225 < y < 325:
        return "medium", 60
    elif 150 < x < 450 and 350 < y < 450:
        return "hard", 150
    return None




class Obstacle:
    def __init__(self, toughness, pos_x, pos_y, width, height):
        self.toughness = toughness
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, colors[self.toughness], (self.pos_x, self.pos_y, self.width, self.height), width=0)

    def is_collision(self, ball_x, ball_y, radius, speed_x, speed_y, last, counter):
        # check bottom and top
        if (self.pos_x - abs(speed_x) <= ball_x <= self.pos_x + self.width + abs(speed_x)
                and (self.pos_y + self.height - abs(speed_y) <= ball_y - radius <= self.pos_y + self.height + abs(
                    speed_y)
                     or self.pos_y - abs(speed_y) <= ball_y + radius <= self.pos_y + abs(speed_y)) and last != self):
            speed_y *= -1
            self.toughness -= 1
            last = self
            counter += 1
        # check right and left
        elif (self.pos_y - abs(speed_x) <= ball_y <= self.pos_y + self.height + abs(speed_x)
              and (self.pos_x + self.width - abs(speed_x) <= ball_x - radius <= self.pos_x + self.width + abs(speed_x)
                   or self.pos_x - abs(speed_x) <= ball_x + radius <= self.pos_x + abs(speed_x)) and last != self):
            speed_x *= -1
            self.toughness -= 1
            last = self
            counter += 1

        return speed_x, speed_y, last, counter


class Ball:
    def __init__(self, radius, pos_x, pos_y, speed_x, speed_y):
        self.radius = radius
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self):
        pygame.draw.circle(screen, (250, 0, 0), (self.pos_x, self.pos_y), self.radius)

    def movement(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

class Buffs:
    def __init__(self, radius, pos_x, pos_y, speed_y, buff):
        self.radius = radius
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_y = speed_y
        self.buff = buff

    def draw(self):
        if self.buff == 'health':
            pygame.draw.circle(screen, (255, 51, 153), (self.pos_x, self.pos_y), self.radius)
        elif self.buff == 'platform':
            pygame.draw.circle(screen, (51, 255, 255), (self.pos_x, self.pos_y), self.radius)
        elif self.buff == 'ball':
            pygame.draw.circle(screen, (0, 204, 0), (self.pos_x, self.pos_y), self.radius)

    def movement(self, is_active):
        self.pos_y += self.speed_y
        if  (platform.pos_x <= self.pos_x <= platform.pos_x + platform.width
                and platform.pos_y - self.speed_y <= self.pos_y + self.radius <= platform.pos_y + self.speed_y):
            self.pos_y = 700
            is_active = 1
        return is_active

class Platform:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.pos_x, self.pos_y, self.width, self.height), width=0)

    def movement(self):
        self.pos_x = pygame.mouse.get_pos()[0]
        if self.pos_x <= 0:
            self.pos_x = 5
        elif self.pos_x + self.width >= WIDTH:
            self.pos_x = WIDTH - self.width - 5


pygame.init()

WIDTH = 605
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid")

clock = pygame.time.Clock()
FPS = 60
play = True

game_status = 'interlude'
font = pygame.font.SysFont("comicsans", 50)
txtwin = font.render("You won!", True, (255, 255, 255))

txtlose = font.render("Game over!", True, (255, 255, 255))

txtplay = font.render("Play again", True, (255, 255, 255))

txteasy = font.render("Easy", True, (0, 0, 0))

txtmedium = font.render("Medium", True, (0, 0, 0))

txthard = font.render("Hard", True, (0, 0, 0))

obstacle_width = 55
obstacle_height = 30
colors = [
    (128, 255, 0),
    (255, 128, 0),
    (255, 51, 51),
    (0, 0, 204),
    (102, 0, 204)
]

health = 3
counter = 0
heart_width = 40
heart_height = 40
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (heart_width, heart_height))



platform = Platform(WIDTH / 2, 530, 55, 20)

mixer.init()
mixer.music.load('push_me.mp3')
while play:
    clock.tick(FPS)
    screen.fill("black")
    if game_status == 'game':
        for obstacle in obstacles:
            if -1 < obstacle.toughness < 6:
                obstacle.draw()

                ball.speed_x, ball.speed_y, last_collision, counter = obstacle.is_collision(ball.pos_x, ball.pos_y, ball.radius, ball.speed_x,
                                                                   ball.speed_y, last_collision, counter)
        is_active = buffs[buff_index].movement(is_active)
        buffs[buff_index].movement(is_active)
        buffs[buff_index].draw()
        if buffs[buff_index].pos_y > 2000:
            buffs[buff_index].pos_y = -1500
        if buffs[buff_index].pos_y <= -1500:
            if buffs[buff_index].buff == "platform" and is_active == 2:
                platform.width /= 2
                is_active = 0
            elif buffs[buff_index].buff == "ball" and is_active == 2:
                ball.radius /= 2
                is_active = 0
            buffs[buff_index].pos_x = random.randint(150, 500)
            buff_index = random.randint(0, len(buffs) - 1)
        if is_active == 1:
            if buffs[buff_index].buff == "health":
                health +=1
                is_active = 0
            elif buffs[buff_index].buff == "platform":
                platform.width *= 2
                is_active = 2
            elif buffs[buff_index].buff == "ball":
                ball.radius *= 2
                is_active = 2

        ball.movement()
        ball.draw()
        platform.movement()
        platform.draw()

        heart_x = 5
        for i in range(health):
            screen.blit(heart_image, (heart_x, 5))
            heart_x += heart_width + 10

        if (
                platform.pos_x <= ball.pos_x <= platform.pos_x + platform.width and platform.pos_y - ball.speed_y <= ball.pos_y + ball.radius <= platform.pos_y + ball.speed_y
                or ball.pos_y - ball.radius <= 50):
            ball.speed_y *= -1
            last_collision = "paddle"
        elif ball.pos_x - ball.radius < 5 or ball.pos_x + ball.radius > WIDTH - 5:
            ball.speed_x *= -1
            last_collision = "wall"
        elif ball.pos_y > HEIGHT + 100:
            ball.speed_x = start_speed_x
            ball.speed_y = start_speed_y
            ball.pos_x = start_x
            ball.pos_y = start_y
            health -= 1
        if health == 0:
            game_status = 'lose'
        if counter == win_points:
            game_status = 'win'
    elif game_status == 'lose':
       draw_lose()
    elif game_status == 'win':
        draw_win()
    elif game_status == "interlude":
        draw_buttons()
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_status == 'win' or game_status == 'lose':
                x, y = pygame.mouse.get_pos()
                game_status= play_button(x, y, game_status)
            elif game_status == 'interlude':
                x, y = pygame.mouse.get_pos()
                difficulty, win_points = check_click(x, y)
                obstacles, health, counter, ball, start_x, start_y, start_speed_x, start_speed_y, last_collision, game_status, buffs, buff_index, is_active = new_game(difficulty)