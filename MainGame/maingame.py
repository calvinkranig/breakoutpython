import sys
import pygame
import shapes
import random
from enum import Enum

#Optional Value if you want to play in windowed mode
WINDOW = 500, 500
#Brick Creation Constants
NUMBER_OF_BRICKS = 80
BRICKS_IN_ROW = 18
BRICK_SCORE = 5
#update color constants to be an enum class called Color
class Color(Enum):
# Color constants
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0,0,255)

#Create an Enum for keeping track of the game_state. The following values will be needed: BALL_ON_PADDLE, PLAYING, GAME_OVER, WON
class Game_State(Enum):
    BALL_ON_PADDLE = 0
    PLAYING = 1
    GAME_OVER = 2
    WON = 3

class MainGame:

    def __init__(self):

        self.screen = pygame.display.set_mode(WINDOW)
        self.font = pygame.font.Font(None, int((self.screen.get_width()) / (BRICKS_IN_ROW + 2)))
        self.new_game()

    #Make a method to inialize the bricks, paddle, and ball and create a new game
    def new_game(self):
        self.lives = 2
        self.score = 0
        self.game_state = Game_State.BALL_ON_PADDLE

        brickwidth = int((self.screen.get_width()) / (BRICKS_IN_ROW + 2))
        brickheight = int(brickwidth / 2)
        self.createBricks(brickwidth, brickheight)
        # Create a self.paddle such that it has a y value one brickheight from the bottom, and has a x value of self.screen.get_width()/2
        # The paddle should also have a height of brickheight/2, and a width of brickwidth*2
        paddley = int(self.screen.get_height()) - brickheight*2
        paddlex = int(self.screen.get_width()/2)
        self.paddle = shapes.Paddle(paddlex, paddley, brickwidth*2, int(brickheight/2), Color.WHITE.value)
        #Create a self.ball such that it starts in the middle of the paddle, and has a width and height of 1/2 a brickwidth
        balldiameter = brickheight
        self.ball = shapes.Ball(paddlex + brickwidth-int(balldiameter/2), paddley-balldiameter,balldiameter, balldiameter, Color.YELLOW.value)

    def createBricks(self, brickwidth, brickheight):
        self.bricks = []
        rcolors = [Color.RED.value,Color.GREEN.value,Color.BLUE.value]


        y = brickheight*2
        #Make Bricks
        while(len(self.bricks) < NUMBER_OF_BRICKS):
            x = brickwidth
            for i in range(BRICKS_IN_ROW):
                rcolor = random.choice(rcolors)
                self.bricks.append(shapes.Shape(x,y,brickwidth,brickheight,rcolor))
                x+= brickwidth
            y += brickheight

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.paddle.update_position(5, WINDOW[0])

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.paddle.update_position(-5, WINDOW[0])

        if pressed[pygame.K_SPACE] and self.game_state == Game_State.BALL_ON_PADDLE:
            self.ball.start_velocity()
            self.game_state = Game_State.PLAYING

        if pressed[pygame.K_RETURN] and (self.game_state == Game_State.GAME_OVER or self.game_state == Game_State.WON):
            self.new_game()

    def update_checkhandle_collisions(self):
        #Handle x change
        self.ball.update_positionx()
        for brick in self.bricks:
            if self.ball.checkhandle_collision_brickx(brick):
                self.bricks.remove(brick)
                self.score += BRICK_SCORE
                if len(self.bricks) <=0:
                    self.game_state = Game_State.WON
        self.ball.checkhandle_collision_wallx(WINDOW[0])

        #Handle y change
        self.ball.update_positiony()
        for brick in self.bricks:
            if self.ball.checkhandle_collision_bricky(brick):
                self.bricks.remove(brick)
                self.score += BRICK_SCORE
                if len(self.bricks) <= 0:
                    self.game_state = Game_State.WON
        self.ball.checkhandle_collision_paddley(self.paddle)
        #Modify code to see if ball collides with bottom of screen, if so decrease lives by one and change games state to:
        # BALL_ON_PADDLE if self.lives > 0 or GAME_OVER if self.lives <= 0
        if self.ball.checkhandle_collision_wally(WINDOW[0]):
            self.lives -= 1
            if self.lives <=0:
                self.game_state = Game_State.GAME_OVER
            else:
                self.game_state = Game_State.BALL_ON_PADDLE

    def draw_bricks(self):
        for brick in self.bricks:
            brick.draw(self.screen)

    def draw_ball(self):
        self.ball.draw(self.screen)

    def draw_paddle(self):
        self.paddle.draw(self.screen)

    def show_message(self,message, position=None):
        if position == None:
            size = self.font.size(message)
            x = int((WINDOW[0] - size[0]) / 2)
            y = int((WINDOW[1] - size[1]) / 2)
            position = (x,y)

        font_surface = self.font.render(message,False, Color.WHITE.value)
        self.screen.blit(font_surface, position)

    def run(self):
        done = False
        clock = pygame.time.Clock()

        while not done:
            # This limits the game to 30 fps
            clock.tick(70)
            self.screen.fill(Color.BLACK.value)


            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            self.handle_input()
            if self.game_state == Game_State.BALL_ON_PADDLE:
                self.show_message("Press Space To Start")
                positionx = self.paddle._shape.left + int(self.paddle._shape.width/2) - int(self.ball._shape.width / 2)
                positiony = self.paddle._shape.top-self.ball._shape.height
                self.ball.update_position((positionx, positiony))
                self.show_message("Score: " + str(self.score) + " Lives: " + str(self.lives), (0,0))
            elif self.game_state == Game_State.PLAYING:
                self.update_checkhandle_collisions()
                self.show_message("Score: " + str(self.score) + " Lives: " + str(self.lives), (0,0))
            elif self.game_state == Game_State.GAME_OVER:
                self.show_message("Game Over Your Score Is: " + str(self.score))
            else:
                self.show_message("You Won Your Score Is: " + str(self.score))


            self.draw_bricks()
            self.draw_ball()
            self.draw_paddle()
            pygame.display.flip()

    def show_bug(self):
        clock = pygame.time.Clock()
        self.game_state = Game_State.PLAYING
        self.ball.update_yvelocity(5)
        self.ball.update_xvelocity(-5)
        self.ball.update_position((self.paddle._shape.right + 25, self.ball._shape.top - 10))
        for x in range(20):
            # This limits the game to 30 fps
            clock.tick(1)
            self.screen.fill(Color.BLACK.value)
            pygame.event.pump()
            self.paddle.update_position(5, WINDOW[0])
            self.update_checkhandle_collisions()
            self.draw_bricks()
            self.draw_ball()
            self.draw_paddle()
            pygame.display.flip()

    def show_bug2(self):
        clock = pygame.time.Clock()
        self.game_state = Game_State.PLAYING
        self.ball.update_xvelocity(6)
        self.ball.update_yvelocity(2)
        self.ball.update_position((self.bricks[0]._shape.left - self.ball._shape.width - 18,self.bricks[0]._shape.top + self.bricks[0]._shape.height  - self.ball._shape.height))

        for x in range(20):
            # This limits the game to 30 fps
            clock.tick(1)
            self.screen.fill(Color.BLACK.value)
            pygame.event.pump()
            self.update_checkhandle_collisions()
            self.draw_bricks()
            self.draw_ball()
            self.draw_paddle()
            pygame.display.flip()


if __name__ == "__main__":
    # Loop until the user clicks the close button.
    pygame.init()
    MainGame().run()
    #MainGame().show_bug()
    #MainGame().show_bug2()
    pygame.quit()
