import pygame

class Shape():
    def __init__(self, xvalue, yvalue, width, height, color=None):
        if color == None:
            self._color = (255,255,255)
        else:
            self._color = color
        self._shape = pygame.Rect(xvalue,yvalue,width,height)


    #Defualt draw
    def draw(self, screen):
        pygame.draw.rect(screen,self._color,self._shape)


class Ball(Shape):
    BALL_VELOCITY = 5
    def __init__(self, xvalue, yvalue, width, height, color=None):
        self._velocity = [0,0]
        super().__init__(xvalue,yvalue,width,height,color)

    def start_velocity(self):
        self._velocity = [-self.BALL_VELOCITY, -self.BALL_VELOCITY]

    #Override draw to draw a circle
    def draw(self, screen):
        pygame.draw.circle(screen,self._color,(self._shape.centerx,self._shape.centery),int(self._shape.width/2))

    def xvelocity(self):
        return self._velocity[0]

    def yvelocity(self):
        return self._velocity[1]

    # Add a function called update_xvelocity(xvelocity) that updates the balls xvelocity with the given value
    def update_xvelocity(self, xvelocity):
        self._velocity[0]= xvelocity
    # Add a function called update_yvelocity(yvelocity) that updates the balls yvelocity with the given value
    def update_yvelocity(self, yvelocity):
        self._velocity[1]= yvelocity

    #Create an update_position method that changes the xvalue and yvalue of the ball based on the velocity
    def update_position(self, position = None):
        if position == None:
            self._shape = self._shape.move(self._velocity[0],self._velocity[1])
        else:
            self._shape.left = position[0]
            self._shape.top = position[1]

    def update_positionx(self, x = None):
        if x == None:
            self._shape = self._shape.move(self._velocity[0], 0)
        else:
            self._shape = self._shape.move(x, 0)

    def update_positiony(self, y = None):
        if y == None:
            self._shape = self._shape.move(0, self._velocity[1])
        else:
            self._shape = self._shape.move(0, y)

    def _check_collision_shape(self,brick):
        return (brick._shape.top <= self._shape.top <= brick._shape.bottom or brick._shape.top <= self._shape.bottom <= brick._shape.bottom)and (brick._shape.left <= self._shape.right <= brick._shape.right or brick._shape.left <= self._shape.left <= brick._shape.right)

    def checkhandle_collision_brickx(self,brick):
        if brick._shape.top <= self._shape.top <= brick._shape.bottom or brick._shape.top <= self._shape.bottom <= brick._shape.bottom:
            #hit from left
            if brick._shape.left <= self._shape.right <= brick._shape.right:
                self.update_xvelocity(self.xvelocity()*-1)
                self._shape.right = brick._shape.left-1
                return True
            #hit from right
            elif brick._shape.left <= self._shape.left <= brick._shape.right:
                self.update_xvelocity(self.xvelocity() * -1)
                self._shape.left = brick._shape.right + 1
                return True
        return False

    def checkhandle_collision_bricky(self,brick):
        if brick._shape.left <= self._shape.right <= brick._shape.right or brick._shape.left <= self._shape.left <= brick._shape.right:
            #Hit from Bottom
            if brick._shape.top <= self._shape.top <= brick._shape.bottom:
                self.update_yvelocity(self.yvelocity()*-1)
                self._shape.top = brick._shape.bottom+1
                return True
            #Hit from Top
            if brick._shape.top <= self._shape.bottom <= brick._shape.bottom:
                self.update_yvelocity(self.yvelocity() * -1)
                self._shape.bottom = brick._shape.top - 1
                return True
        return False


    def checkhandle_collision_paddley(self, paddle):
        #Check to see if ball can hit paddle
        if self._shape.bottom  >= paddle._shape.top >= self._shape.top:
            if paddle._shape.left <= self._shape.right <= paddle._shape.right or paddle._shape.left <= self._shape.left <= paddle._shape.right:
                self._shape.bottom = paddle._shape.top +1
                self.update_yvelocity(self.yvelocity() * -1)
                # Update x velocity based of where ball hit paddle
                x = self._shape.centerx - paddle._shape.centerx
                xvelocitychange = (x* self.BALL_VELOCITY)/(paddle._shape.width/2)
                xvelocitychange = round(xvelocitychange)
                self.update_xvelocity(self.xvelocity()+ int(xvelocitychange))

    def checkhandle_collision_wallx(self, x):
        #Modify Method to return true if ball hits the bottom of the screen else false
        if self._shape.left <= 0:
            self._shape.left = 1
            self.update_xvelocity(self._velocity[0]*-1)
        elif self._shape.right >= x:
            self._shape.right = x - 1
            self.update_xvelocity(self._velocity[0]*-1)

    def checkhandle_collision_wally(self,y):
        if self._shape.top <= 0:
            self._shape.top = 1
            self.update_yvelocity(self._velocity[1]*-1)
        elif self._shape.bottom >= y:
            return True

        return False


class Paddle(Shape):
    #Create a update_position method for the paddle that takes in an xchange value and calls self.shape.move(xchange, 0)
    def update_position(self, xchange, window_width):
        if xchange + self._shape.left < 0 :
            self._shape.left = 0
        elif xchange + self._shape.right > window_width:
            self._shape.right = window_width
        else:
            self._shape = self._shape.move(xchange,0)
