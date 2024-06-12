from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class Kamisado(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.current_player = 1
        self.board = [[' 0'] * 8 for _ in range(8)]
        self.setup_board()
        self.current_color = None

    def setup_board(self):
        white = 7
        black = 0
        # Initialize the starting positions of towers for each player
        for i in range(8):
            self.board[0][i] = f"{white}1"  # White player tower
            white -= 1

            self.board[7][i] = f"{black}2"  # Black player tower
            black += 1

    def get_board_color(self, i, j):
        BOARD_COLORS = [
            [7, 6, 5, 4, 3, 2, 1, 0],
            [2, 7, 4, 1, 6, 3, 0, 5],
            [1, 4, 7, 2, 5, 0, 3, 6],
            [4, 5, 6, 7, 0, 1, 2, 3],
            [3, 2, 1, 0, 7, 6, 5, 4],
            [6, 3, 0, 5, 2, 7, 4, 1],
            [5, 0, 3, 6, 1, 4, 7, 2],
            [0, 1, 2, 3, 4, 5, 6, 7]
        ]
    
        return BOARD_COLORS[i][j]

    def possible_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j][1] == str(self.current_player) and (self.board[i][j][0] == str(self.current_color) or self.current_color == None):
                    moves.extend(self.valid_moves_for_piece(i, j))
        return moves
    
    def valid_moves_for_piece(self, i, j):
        moves = []
        for new_x in range(8):
            for new_y in range(8):
                if self.board[new_x][new_y] == ' 0':
                    if self.board[i][j][1] == '2' and ( (new_x < i and new_y == j) or ((i - new_x == abs(new_y - j) and new_x < i)) ):
                        moves.append([i, j, new_x, new_y])
                    elif self.board[i][j][1] == '1' and ( (new_x > i and new_y == j) or ((new_x - i == abs(new_y - j) and new_x > i)) ):
                        moves.append([i, j, new_x, new_y])

        return moves
             
    def make_move(self, move):
        i, j, new_x, new_y = move
        self.board[new_x][new_y] = self.board[i][j]
        self.board[i][j] = ' 0'
        self.current_color = self.get_board_color(new_x, new_y)

    def loss_condition(self):
        # Check if the opponent's tower reaches the opposite end
        for j in range(8):
            if self.board[0][j][1] == '2':
                return True
            if self.board[7][j][1] == '1':
                return True
        return False

    def is_over(self):
        return self.loss_condition() or self.possible_moves() == []

    def show(self):
        print("\n".join([" ".join([str(cell) for cell in row]) for row in self.board]))

        color = ""
        if self.current_color == 0:
            color = "brown"
        elif self.current_color == 1:
            color = "green"
        elif self.current_color == 2:
            color = "red"
        elif self.current_color == 3:
            color = "yellow"
        elif self.current_color == 4:
            color = "pink"
        elif self.current_color == 5:
            color = "purple"
        elif self.current_color == 6:
            color = "blue"
        else:
            color = "orange"
        
        print(f"current color : {color}, color_num : {self.current_color}")

    def scoring(self):
        return -100 if self.loss_condition() else 0

if __name__ == "__main__":
    # Initialize the game with AI and human players
    game = Kamisado([AI_Player(Negamax(3)), Human_Player()])

    # Start playing the game
    game.play()
    # print(game.board)
    