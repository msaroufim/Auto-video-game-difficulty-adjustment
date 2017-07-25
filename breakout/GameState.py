import pickle
class GameState:
    def __init__(self,gameLives=3, hitCount=0, ball_x=50, ball_y=250,
                 ball_radius=10, ball_color=[220,50,50], ball_speed_x=3, ball_speed_y=5,
                 paddle_x=20, paddle_y=450, paddle_width=60, paddle_height=20, paddle_color=[20,180,180], paddle_speed=10,
                 powerup_prob = 0.05,
                 score=0,
                 closeCalls=0):
        self.gameLives = gameLives
        self.hitCount = hitCount
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_radius = ball_radius
        self.ball_color = ball_color
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.paddle_x = paddle_x
        self.paddle_y = paddle_y
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_color = paddle_color
        self.paddle_speed = paddle_speed
        self.powerup_prob = powerup_prob
        self.score = score
        self.closeCalls = closeCalls

        self.max_ball_speed_x = 10
        self.max_ball_speed_y = 15
        self.min_ball_speed_x = 0.5
        self.min_ball_speed_y = 0.5

    def resetVars(self):
        self.ball_x = 50
        self.ball_y = 250
        self.gameLives -= 1

        # adjust difficulty
        if self.hitCount >= 5:
            self.ball_speed_x = min(self.ball_speed_x + 0.5, self.max_ball_speed_x)
            self.ball_speed_y = min(self.ball_speed_y + 0.5, self.max_ball_speed_y)
            #change powerup spawn rate
        else:
            self.ball_speed_x = max(self.ball_speed_x-0.5, self.min_ball_speed_x)
            self.ball_speed_y = max(self.ball_speed_y-0.5, self.min_ball_speed_y)

        self.hitCount = 0

    def addCloseCall(self):
        self.closeCalls+=1

    def addHit(self):
        self.hitCount+=1

    def getBricksArray(self, bricks_array):
        self.bricks_array = bricks_array

    def writeVars(self):
        stateFile = open("GameStates.txt", "a")
        stateFile.write("----------------------------------------------------\n")
        stateFile.write("Lives left: " + str(self.gameLives) + "\n")
        #stateFile.write("Number of ball hits: " + str(self.hitCount) + "\n")
        stateFile.write("Blocks broken: " + str(self.score) + "\n")
        stateFile.write("Current powerup probability: " + str(self.powerup_prob) + "\n")
        stateFile.write("Ball speed in x direction: " + str(abs(self.ball_speed_x)) + "\n")
        stateFile.write("Ball speed in y direction: " + str(abs(self.ball_speed_y)) + "\n")
        stateFile.write("CLOSE CALLS: " + str(self.closeCalls) + "\n")
        stateFile.close()

    def stateSnapshot(self):
        currState = CurrState(self.gameLives, self.score, self.powerup_prob, abs(self.ball_speed_x),
                              abs(self.ball_speed_y), self.closeCalls, self.bricks_array)
        return currState

    def writeEndSession(self):
        stateFile = open("GameStates.txt", "a")
        stateFile.write("\n---------------END OF SESSION--------------------\n\n")
        stateFile.close()

class CurrState:
    def __init__(self, gameLives, score, powerup_prob, ball_speed_x, ball_speed_y, closeCalls, bricks_array):
        self.gameLives = gameLives
        self.score = score
        self.powerup_prob = powerup_prob
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.closeCalls = closeCalls
        self.bricks_array = bricks_array

    def pickle(self):
        f = open("Pickles.txt", "a")
        pickle.dump(self, f)
        f.write("\n")
        f.close()