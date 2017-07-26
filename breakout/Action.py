class Action:
    def __init__(self, movedDirection, paddleBallCollision, ballBrickCollision, closeCall, lifeLost):
        self.movedDirection = movedDirection
        self.paddleBallCollision = paddleBallCollision
        self.ballBrickCollision = ballBrickCollision
        self.closeCall = closeCall
        self.lifeLost = lifeLost

    def addBrickCollision(self, brick, row_index, column_index, closeCall):
        self.brick = brick
        self.row_index = row_index
        self.column_index = column_index
        self.closeCall = closeCall