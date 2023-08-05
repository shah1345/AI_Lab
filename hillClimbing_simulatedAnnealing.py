import math, time, random
from random import randint

SIZE = 4
TEMPERATURE, ALPHA = 1, 0.99



N = 4

def configureRandomly(board, state):


	for i in range(N):

		# Getting a random row index
		state[i] = randint(0, 100000) % N;

		board[state[i]][i] = 1;

def printBoard(board):

	for i in range(N):
		print(*board[i])

def printState( state):
	print(*state)

def compareStates(state1, state2):


	for i in range(N):
		if (state1[i] != state2[i]):
			return False;

	return True;


def fill(board, value):

	for i in range(N):
		for j in range(N):
			board[i][j] = value;



def calculateObjective( board, state):


	attacking = 0;

	for i in range(N):


		row = state[i]
		col = i - 1;
		while (col >= 0 and board[row][col] != 1) :
			col -= 1

		if (col >= 0 and board[row][col] == 1) :
			attacking += 1;


		row = state[i]
		col = i + 1;
		while (col < N and board[row][col] != 1):
			col += 1;

		if (col < N and board[row][col] == 1) :
			attacking += 1;

		row = state[i] - 1
		col = i - 1;
		while (col >= 0 and row >= 0 and board[row][col] != 1) :
			col-= 1;
			row-= 1;

		if (col >= 0 and row >= 0 and board[row][col] == 1) :
			attacking+= 1;

		row = state[i] + 1
		col = i + 1;
		while (col < N and row < N and board[row][col] != 1) :
			col+= 1;
			row+= 1;

		if (col < N and row < N and board[row][col] == 1) :
			attacking += 1;

		row = state[i] + 1
		col = i - 1;
		while (col >= 0 and row < N and board[row][col] != 1) :
			col -= 1;
			row += 1;

		if (col >= 0 and row < N and board[row][col] == 1) :
			attacking += 1;

		row = state[i] - 1
		col = i + 1;
		while (col < N and row >= 0 and board[row][col] != 1) :
			col += 1;
			row -= 1;

		if (col < N and row >= 0 and board[row][col] == 1) :
			attacking += 1;

	return int(attacking / 2);

def generateBoard( board, state):
	fill(board, 0);
	for i in range(N):
		board[state[i]][i] = 1;

def copyState( state1, state2):

	for i in range(N):
		state1[i] = state2[i];


def getNeighbour(board, state):

	opBoard = [[0 for _ in range(N)] for _ in range(N)]
	opState = [0 for _ in range(N)]

	copyState(opState, state);
	generateBoard(opBoard, opState);

	opObjective = calculateObjective(opBoard, opState);


	NeighbourBoard = [[0 for _ in range(N)] for _ in range(N)]

	NeighbourState = [0 for _ in range(N)]
	copyState(NeighbourState, state);
	generateBoard(NeighbourBoard, NeighbourState);

	for i in range(N):
		for j in range(N):

			if (j != state[i]) :

				NeighbourState[i] = j;
				NeighbourBoard[NeighbourState[i]][i] = 1;
				NeighbourBoard[state[i]][i] = 0;

				temp = calculateObjective( NeighbourBoard, NeighbourState);


				if (temp <= opObjective) :
					opObjective = temp;
					copyState(opState, NeighbourState);
					generateBoard(opBoard, opState);

				NeighbourBoard[NeighbourState[i]][i] = 0;
				NeighbourState[i] = state[i];
				NeighbourBoard[state[i]][i] = 1;

	copyState(state, opState);
	fill(board, 0);
	generateBoard(board, state);




def hillClimbing(board, state):


	neighbourBoard = [[0 for _ in range(N)] for _ in range(N)]
	neighbourState = [0 for _ in range(N)]

	copyState(neighbourState, state);
	generateBoard(neighbourBoard, neighbourState);

	while True:


		copyState(state, neighbourState);
		generateBoard(board, state);

		# Getting the optimal neighbour

		getNeighbour(neighbourBoard, neighbourState);

		if (compareStates(state, neighbourState)) :



			printBoard(board);
			break;

		elif (calculateObjective(board, state) == calculateObjective( neighbourBoard,neighbourState)):


			neighbourState[randint(0, 100000) % N] = randint(0, 100000) % N;
			generateBoard(neighbourBoard, neighbourState);

# Driver code
state = [0] * N
board = [[0 for _ in range(N)] for _ in range(N)]








class Board:

    @staticmethod
    def getBoard():
        return [random.randint(0, SIZE - 1) for i in range(0, SIZE)]
        # board[row] = col

    @staticmethod
    def getNeighbour(board):
        neighbour = board.copy()
        i = random.randint(0, SIZE - 1)
        while True:
            j = random.randint(0, SIZE - 1)
            if neighbour[i] != j:
                neighbour[i] = j
                return neighbour

    @staticmethod
    def getCost(board):
        threats = 0
        # we know that each row has exactly one queen
        for queen in range(0, SIZE):
            for nextQueen in range(queen + 1, SIZE):
                if board[queen] == board[nextQueen]  or abs(queen - nextQueen) == abs(board[queen] - board[nextQueen]):
                    threats += 1

        return threats

    @staticmethod
    def show(board):
        for i in range(SIZE):
            for j in range(SIZE):
                print('0', end = ' ') if board[i] != j else print('1', end = ' ')
            print()
        print('Number of pairs of queens that are attacking each other:   %s\n'     %Board.getCost(board))


def simulatedAnnealing(board):
    currentState = board
    global TEMPERATURE
    epsilon = math.e ** (-100)
    while Board.getCost(currentState) != 0 and TEMPERATURE > epsilon:
        TEMPERATURE *= ALPHA
        neighbour = Board.getNeighbour(currentState)
        dE = Board.getCost(neighbour) - Board.getCost(currentState)
        if dE <= 0 or random.uniform(0,1) < math.e ** (-dE / TEMPERATURE):
            currentState = neighbour

    return currentState




if __name__ == '__main__':
    inithialState = Board.getBoard()
    print('\tInitial State:')
    Board.show(inithialState)

    startTime = time.time()
    finalState = simulatedAnnealing(inithialState)
    stopTime = time.time()

    print('\tFinal State OF SimulatedAnnealing:')
    Board.show(finalState)

    print('exec time:    %s  seconds' %(stopTime - startTime))
print('\tInitial State:')
configureRandomly(board, state);
printBoard(board);
print('Number of pairs of queens that are attacking each other:   %s\n'     %calculateObjective(board, state))
print('\tFinal State OF hillClimbing:')
startTime2 = time.time()
hillClimbing(board, state);
stopTime2 = time.time()
print('Number of pairs of queens that are attacking each other:   %s\n'     %calculateObjective(board, state))
print('exec time:    %s  seconds' %(stopTime2 - startTime2))
