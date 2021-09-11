class MazeGame():
    # 1 - wall
    # 0 - space
    # 2 - player start
    # 3 - goal
    board = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 3, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    goalX = 14
    goalY = 10

    def __init__(self):
        self.x = 1
        self.y = 1
        self.steps = 0
        self.penalties = 0


    # move return 0 - error, 1 - no error, 2 - victory
    def moveUp(self):
        if not self.checkWall(self.x, self.y - 1):            
            self.y -= 1
            self.steps += 1
            return self.checkVictory()
        
        return 0

    def moveDown(self):
        if not self.checkWall(self.x, self.y + 1):
            self.y += 1
            self.steps += 1
            return self.checkVictory()
        
        return 0

    def moveLeft(self):
        if not self.checkWall(self.x - 1, self.y):
            self.x -= 1
            self.steps += 1
            return self.checkVictory()
        
        return 0

    def moveRight(self):
        if not self.checkWall(self.x + 1, self.y):
            self.x += 1
            self.steps += 1
            return self.checkVictory()
        
        return 0

    def checkVictory(self):
        if self.board[self.y][self.x] == 3:
            return 2
        else:
            return 1

    def checkWall(self, x, y):
        if self.board[y][x] == 1:
            self.penalties += 1
            return True
        else:
            return False
    
    def isWallBetweenPositionAndGoal(self): # If yes, then return penalty
        xLocked = False
        yLocked = False

        if self.x < self.goalX:
            for i in range(self.x + 1, self.goalX + 1):
                if self.board[self.y][i] == 1:
                    xLocked = True
                    break
        
        elif self.x > self.goalX:
            for i in range(self.x - 1, self.goalX - 1, -1):
                if self.board[self.y][i] == 1:
                    xLocked = True
                    break

        if self.y < self.goalY:
            for i in range(self.y + 1, self.goalY + 1):
                if self.board[i][self.x] == 1:
                    yLocked = True
                    break
        
        elif self.y > self.goalY:
            for i in range(self.y - 1, self.goalY - 1, -1):
                if self.board[i][self.x] == 1:
                    yLocked = True
                    break

        # penalty
        penalty = 2
        if xLocked and yLocked:
            penalty = 3
        elif self.x == self.goalX and yLocked:
            penalty = 4
        elif self.y == self.goalY and xLocked:
            penalty = 4
        
        return penalty
        