import pygame
from pygame.locals import *
import time
import random

SIZE = 40
bg = (0, 0, 0)

class Apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load('C:/Users/Safal Bhandari/Desktop/apple (1).jpg').convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw (self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,14)*SIZE
        self.y = random.randint(0,14)*SIZE


class Snake:
    def __init__(self, parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("C:/Users/Safal Bhandari/Desktop/block1.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'up'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill((bg))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE




        self.draw()



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Safal Bhandari Snake and Apple Game")

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((800,600))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()


    def is_collision(self,x1,y1,x2,y2):
        if x1  >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load('C:/Users/Safal Bhandari/Downloads/Super Mario Bros. Theme Song.mp3')
        pygame.mixer.music.play()





    def render_background(self):
        ba = pygame.image.load("C:/Users/Safal Bhandari/Desktop/large_thumbnail.jpg")
        self.surface.blit(ba,(0,0))


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x,self.apple.y ):
            sound = pygame.mixer.Sound('C:/Users/Safal Bhandari/Downloads/swiftly-610.mp3')
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.apple.move()


        #snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                sound = pygame.mixer.Sound('C:/Users/Safal Bhandari/Downloads/hasty-ba-dum-tss-615.mp3')
                pygame.mixer.Sound.play(sound)
                raise Exception('Game Over')

        if not (0 <= self.snake.x[0] <= 800 and 0 <= self.snake.y[0] <= 600):
            sound = pygame.mixer.Sound('C:/Users/Safal Bhandari/Downloads/hasty-ba-dum-tss-615.mp3')
            pygame.mixer.Sound.play(sound)

            raise Exception("Hit the boundry error")



    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30, bold=2)
        line1 = font.render(f'Game over! Your Score: {self.snake.length}',True,(255,255,255))
        self.surface.blit(line1,(200,200))
        line2 = font.render(f'To play again press Enter . To exit press Escape',True,(255,255,255))
        self.surface.blit(line2,(100,250))
        pygame.display.flip()

        pygame.mixer.music.pause()


    def display_score(self):
        font = pygame.font.SysFont('arial',30,bold=2)
        score = font.render(f'Score: {self.snake.length}',True,(255,255,255))
        self.surface.blit(score,(600,10))



    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.play()
                        pause = False

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                   self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()



            time.sleep(0.2)






if __name__ == '__main__':
    game = Game()
    game.run()
