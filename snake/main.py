import random
import pygame
from pygame.locals import *
import time

SIZE = 40


class Apple:
    def __init__(self, surface):
        self.apple = pygame.image.load('./python_projects/resources/apple.jpg').convert()
        self.parent_screen = surface
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load('./python_projects/resources/block.jpg').convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((8, 163, 161))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_backgorund_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_backgorund_music(self):
        pygame.mixer.music.load('./python_projects/resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound=pygame.mixer.Sound('./python_projects/resources/ding.mp3')
            pygame.mixer.Sound.play(sound)
            # print("Collision occured")
            self.snake.increase_length()
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # print("game over, you hit youself")
                # exit(0)s
                crash_sound=pygame.mixer.Sound("./python_projects/resources/crash.mp3")
                pygame.mixer.Sound.play(crash_sound)
                raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.surface.fill((8, 163, 161))
        font=pygame.font.SysFont('arial',30)
        line1= font.render(f"Game is over! Your score is {self.snake.length}",True,(200,200,200))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play game again press Enter. To exit press Escape!",True,(200,200,200))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake=Snake(self.surface,1)
        self.apple=Apple(self.surface)

    def run(self):
        running = True
        pause=False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if not pause:
                        if event.key == K_ESCAPE:
                            running = False
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                    if event.key == K_RETURN:
                        pause=False
                        pygame.mixer.music.unpause()


                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.3)


if __name__ == '__main__':
    game = Game()
    game.run()
