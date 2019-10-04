import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
screen_width, screen_height = win.get_width(), win.get_height()

pygame.display.set_caption("First game")

walk_right = [pygame.image.load(f"R{i}.png") for i in range(1, 10)]
walk_left = [pygame.image.load(f"L{i}.png") for i in range(1, 10)]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
bullet_sound = pygame.mixer.Sound('bullet.wav')
hit_sound = pygame.mixer.Sound('hit.wav')
# bullet_sound.play()

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

class Player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.right:
                win.blit(walk_right[0], (self.x, self.y))
            else:
                win.blit(walk_left[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.is_jump = False
        self.jump_count = 10
        self.x, self.y = 60, 410
        self.walk_count = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Enemy():
    walk_right = [pygame.image.load(f"R{i}E.png") for i in range(1, 12)]
    walk_left = [pygame.image.load(f"L{i}E.png") for i in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.width = width
        self.height = height
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.visible:
            self.move()
            if self.walk_count + 1 >= 33:
                self.walk_count = 0
            if self.vel > 0:
                win.blit(self.walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1

            pygame.draw.rect(win, (255, 0, 0),
                            (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 100, 0),
                            (self.hitbox[0], self.hitbox[1] - 20, 5*self.health, 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    text = font.render(f'Score: {score}', 1, (0, 0, 0))
    win.blit(text, (350, 10))
    man.draw(win)
    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = Player(300, 410, 64, 64)
enemy = Enemy(100, 410, 64, 64, 450)
shoot_loop = 0
bullets = []
score = 0
font = pygame.font.SysFont('comicsans', 30, True)

run = True
while run:
    clock.tick(27)

    if enemy.visible:
        if man.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and \
            man.hitbox[1] + man.hitbox[3] > enemy.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > enemy.hitbox[0] and \
                man.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                man.hit()
                score -= 5

    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 10:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and \
            bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and \
                bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                hit_sound.play()
                enemy.hit()
                if enemy.health:
                    score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        bullet_sound.play()
        if man.right:
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width//2),
                                      round(man.y + man.height//2),
                                      6, (0, 0, 0), facing))
        shoot_loop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left, man.right  = True, False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screen_width - man.width - man.vel:
        man.x += man.vel
        man.right, man.left  = True, False
        man.standing = False
    else:
        man.standing = True
        man.walk_count = 0

    if not man.is_jump:
        if keys[pygame.K_UP]:
            man.is_jump = True
            # man.right, man.left = False, False
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            man.y -= (man.jump_count*abs(man.jump_count))*0.5
            man.jump_count -= 1
        else:
            man.is_jump = False
            man.jump_count = 10

    redraw_game_window()

pygame.quit()
