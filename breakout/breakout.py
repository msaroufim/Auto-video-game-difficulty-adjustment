import pygame, random
from GameState import GameState
from Action import Action
pygame.init()
screen = pygame.display.set_mode([650,480])
black = [0, 0, 0]

#Brick class to be put into brick array, has position and whether it is a powerup
class Brick(pygame.sprite.Sprite):
    imageRef = None

    def __init__(self, x, y,powerup=False):
        pygame.sprite.Sprite.__init__(self)
        self.powerup = powerup

        if powerup:
            Brick.imageRef = ("Explode.png")
        else:
            Brick.imageRef = ("brick.png")

        self.imageRef = Brick.imageRef

        # Make our top-left corner the passed-in location.
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 50, 16)
        self.rect.topleft = (self.x, self.y)

#Bricks class to load each Brick into an array, clear bricks when state ends
class Bricks:
    def __init__(self, brick_level_count=4, powerup_prob=0.05):
        self.brick_level_count = brick_level_count
        self.powerup_prob = powerup_prob

    def loadBricks(self):
        self.brick_array = []
        self.ispowerup = {}
        for i in range(0, 13):
            bricks_rows = []
            for j in range(1, self.brick_level_count):
                if (random.uniform(0, 1) < self.powerup_prob):
                    brick = Brick(50 * i, 50 * j, powerup=True)
                    self.ispowerup[brick] = True
                else:
                    brick = Brick(50 * i, 50 * j, powerup=False)
                    self.ispowerup[brick] = False
                bricks_rows.append(brick)
            self.brick_array.append(bricks_rows)

    def clearBricks(self):
        for row in self.brick_array:
            del row[:]

state = GameState()


myfont = pygame.font.SysFont("Arial", 22)

bricks = Bricks()
bricks.loadBricks()
brick_array = bricks.brick_array

#allows for holding of key
pygame.key.set_repeat(20, 20)


clock = pygame.time.Clock()
running = True
#game loop
movedDirection = "none"
paddleBallCollision = 0
ballBrickCollision = 0
while running:
    clock.tick(60)
    for event in pygame.event.get():
        #check if you've exited the game
        if event.type == pygame.QUIT:
            state.writeEndSession()
            running = False

        if event.type == pygame.MOUSEMOTION:
            coordinates = pygame.mouse.get_pos() #gives (x,y) coordinates
            if (coordinates[0]-state.paddle_width/2) != state.paddle_x:
                if (coordinates[0]-state.paddle_width/2) < state.paddle_x:
                    movedDirection = "left"
                else:
                    movedDirection = "right"

            state.paddle_x = coordinates[0] - state.paddle_width/2 #sets the paddle_x variable to the first item in coordinates
            if state.paddle_x < 0:
                state.paddle_x = 0
            if state.paddle_x > screen.get_width() - state.paddle_width:
                state.paddle_x = screen.get_width() - state.paddle_width



    #pause for 20 milliseconds
    pygame.time.delay(20)
    #make the screen completely white
    screen.fill(black)

    #move the ball
    state.ball_y = state.ball_y + state.ball_speed_y
    state.ball_x = state.ball_x + state.ball_speed_x
    #check if the ball is off the bottom of the screen
    if state.ball_y > screen.get_height() - state.ball_radius:
        state.resetVars()
        if state.gameLives==0:
            state.getBricksArray(bricks.brick_array)
            state.writeVars()
            bricks.clearBricks()
            state = GameState()
            bricks = Bricks()
            bricks.loadBricks()
            brick_array = bricks.brick_array
    #check if the ball hit the top of the screen
    if state.ball_y < state.ball_radius:
        state.ball_speed_y = -state.ball_speed_y
    #check if the ball hit the left side of the screen
    if state.ball_x < state.ball_radius:
        state.ball_speed_x = -state.ball_speed_x
    #check if the ball hit the right side of the screen
    if state.ball_x > screen.get_width() - state.ball_radius:
        state.ball_speed_x = -state.ball_speed_x

    #create imaginary rectangles around ball and paddle
    ball_rect = pygame.Rect(state.ball_x-state.ball_radius, state.ball_y-state.ball_radius, state.ball_radius*2,state.ball_radius*2) #circles are measured from the center, so have to subtract 1 radius from the x and y
    paddle_rect = pygame.Rect(state.paddle_x, state.paddle_y, state.paddle_width, state.paddle_height)
    paddle_left_end_rec = pygame.Rect(state.paddle_x, state.paddle_y, 3, state.paddle_height)
    paddle_right_end_rec = pygame.Rect((state.paddle_x+state.paddle_width)-3, state.paddle_y, 3, state.paddle_height)

    #see if the rectangles overlap
    if ball_rect.colliderect(paddle_rect):
        state.addHit()
        paddleBallCollision = 1
        if ball_rect.colliderect(paddle_left_end_rec) or ball_rect.colliderect(paddle_right_end_rec):
            state.addCloseCall()
        state.ball_speed_y = -state.ball_speed_y

    #Destruction of bricks, implementation of exploding brick
    for row_index in range(0, len(brick_array)):
        for column_index in range(0, len(brick_array[row_index])):
            brick = brick_array[row_index][column_index]
            if brick != None and brick.rect.colliderect(ball_rect):
                ballBrickCollision = 1
                if brick.powerup:
                    if brick_array[row_index][column_index] != None:
                        brick_array[row_index][column_index] = None
                        state.score += 1
                    if row_index > 0 and brick_array[row_index-1][column_index] != None:
                        brick_array[row_index-1][column_index] = None
                        state.score += 1
                    if row_index < 12 and brick_array[row_index+1][column_index] != None:
                        brick_array[row_index+1][column_index] = None
                        state.score += 1
                    if column_index > 0 and brick_array[row_index][column_index-1] != None:
                        brick_array[row_index][column_index-1] = None
                        state.score += 1
                    if column_index < 2 and brick_array[row_index][column_index+1] != None:
                        brick_array[row_index][column_index+1] = None
                        state.score += 1
                else:
                    state.score += 1
                    brick_array[row_index][column_index] = None
                state.ball_speed_y = - state.ball_speed_y


    #draw everything on the screen
    score_label = myfont.render("Score: " + str(state.score), 1, pygame.color.THECOLORS['white'])
    lives_label = myfont.render("Lives " + str(state.gameLives), 1, pygame.color.THECOLORS['white'])
    screen.blit(score_label, (5, 10))
    screen.blit(lives_label, (200, 10))
    for row in brick_array:
        for brick in row:
            if brick != None:
                screen.blit(pygame.image.load(brick.imageRef), brick.rect)
    pygame.draw.circle(screen, state.ball_color, [int(state.ball_x), int(state.ball_y)], state.ball_radius, 0)
    pygame.draw.rect(screen, state.paddle_color, [state.paddle_x, state.paddle_y, state.paddle_width, state.paddle_height], 0)
    #update the entire display
    pygame.display.update()
    if state.score == 39:
        state.getBricksArray(bricks.brick_array)
        state.writeVars()
        bricks.clearBricks()
        state = GameState()
        bricks = Bricks()
        bricks.loadBricks()
        brick_array = bricks.brick_array

    action = Action(movedDirection, paddleBallCollision, ballBrickCollision)
    state.getBricksArray(brick_array)
    currState = state.stateSnapshot(action)
    currState.pickle()

