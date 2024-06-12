from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
import pygame

class Kamisado(TwoPlayerGame):
    ######gui##########
    def __init__(self, players, gui=True):
        self.players = players
        self.current_player = 1
        self.board = [[' 0'] * 8 for _ in range(8)]
        self.setup_board()
        self.current_color = None
        self.game_log = ""
        self.block_count = 0
        self.last_player = 0
        self.gui = gui
        if self.gui:
            self.init_pygame()
        super().__init__()

    def init_pygame(self):
        pygame.init()
        self.CELL_SIZE = 64
        self.WIDTH, self.HEIGHT = 8 * self.CELL_SIZE, 8 * self.CELL_SIZE
        self.white = (255, 255, 255)
        self.playercolor = [(0, 0, 0), (255, 255, 255)]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("KAMISADO")

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if 0 <= i < 8 and 0 <= j < 8:
                    color = self.get_board_color(i, j)
                    rect = pygame.Rect(j * self.CELL_SIZE, i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    pygame.draw.rect(self.screen, self.playercolor[color], rect, width=0)



    def draw_towers(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != ' 0':
                    color = int(self.board[i][j][0]) % len(self.playercolor)
                    center = (j * self.CELL_SIZE + self.CELL_SIZE / 2, i * self.CELL_SIZE + self.CELL_SIZE / 2)
                    pygame.draw.circle(self.screen, self.playercolor[color], center, self.CELL_SIZE / 2, width=0)
                    pygame.draw.circle(self.screen, self.playercolor[(color + 1) % len(self.playercolor)], center, self.CELL_SIZE / 2, width=2)

    def draw_highlight(self, move):
        if move is not None:
            i, j, new_x, new_y = move
            rect = pygame.Rect(new_y * self.CELL_SIZE, new_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.playercolor[self.current_player - 1], rect, width=2)

    def main_loop(self):
        running = True
        move = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.loss_condition():
                    pos = pygame.mouse.get_pos()
                    move = self.convert_coordinates(pos)
                    if move in self.possible_moves():
                        self.make_move(move)
                        move = None

            self.screen.fill(self.white)
            self.draw_board()
            self.draw_towers()
            self.draw_highlight(move)
            pygame.display.flip()

        pygame.quit()

    def play(self):
        if self.gui:
            self.main_loop()
        else:
            super().play()
    
    ############################
#    def __init__(self, players):
#        self.players = players
#        self.current_player = 1
#        self.board = [[' 0'] * 8 for _ in range(8)]
#        self.setup_board()
#        self.current_color = None
#        self.game_log = ""
#        self.block_count = 0
#        self.last_player = 0

    def convert_coordinates(self, pos):
        x, y = pos
        row = x // self.CELL_SIZE
        col = y // self.CELL_SIZE
        return [col, row, col, row]  # Return a move [start_col, start_row, end_col, end_row]


    def setup_board(self):
        white = 7
        black = 0
        # Initialize the starting positions of towers for each player
        for i in range(8):
            self.board[0][i] = f"{white}1"  # White player tower
            white -= 1

            self.board[7][i] = f"{black}2"  # Black player tower
            black += 1

        # for i in range(8):
        #     self.board[3][i] = f"{white}1"  # White player tower
        #     white -= 1

        # for i in range(7):
        #     self.board[4][i] = f"{black}2"  # Black player tower
        #     black += 1
        
        # self.board[4][3] = " 0"
        # self.board[5][3] = "32"
        self.board[5][7] = f"{black}2";

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

        if 0 <= i < 8 and 0 <= j < 8:
            return BOARD_COLORS[i][j] % len(self.playercolor)
        else:
            # Handle out-of-range indices, returning a default color or raising an exception
            return 0  # You can modify this to return a default color or raise an exception as needed



    def possible_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j][1] == str(self.current_player) and (self.board[i][j][0] == str(self.current_color) or self.current_color == None):
                    moves.extend(self.valid_moves_for_piece(i, j))
        if moves == []:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j][1] == str(self.current_player) and (self.board[i][j][0] == str(self.current_color)):
                        moves.append([i, j, i, j])
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

        if self.current_player == 2:
            new_x = i - 1
            pivot_x = 0
            while 0 <= new_x <= 7:
                if self.board[new_x][j] != ' 0':
                    pivot_x = new_x
                elif new_x < pivot_x:
                    moves.remove([i, j, new_x, j])
                new_x -= 1

            new_x, new_y = i - 1, j - 1
            pivot_x, pivot_y = 0, 0
            while (0 <= new_x <= 7) and (0 <= new_y <= 7):
                if self.board[new_x][new_y] != ' 0':
                    pivot_x, pivot_y = new_x, new_y
                elif new_x < pivot_x and new_y < pivot_y:
                    moves.remove([i, j, new_x, new_y])
                new_x -= 1
                new_y -= 1

            new_x, new_y = i - 1, j + 1
            pivot_x, pivot_y = 0, 7
            while (0 <= new_x <= 7) and (0 <= new_y <= 7):
                if self.board[new_x][new_y] != ' 0':
                    pivot_x, pivot_y = new_x, new_y
                elif new_x < pivot_x and new_y > pivot_y:
                    moves.remove([i, j, new_x, new_y])
                new_x -= 1
                new_y += 1

        elif self.current_player == 1:
            new_x = i + 1
            pivot_x = 7
            while 0 <= new_x <= 7:
                if self.board[new_x][j] != ' 0':
                    pivot_x = new_x
                elif new_x > pivot_x:
                    moves.remove([i, j, new_x, j])
                new_x += 1

            new_x, new_y = i + 1, j - 1
            pivot_x, pivot_y = 7, 0
            while (0 <= new_x <= 7) and (0 <= new_y <= 7):
                if self.board[new_x][new_y] != ' 0':
                    pivot_x, pivot_y = new_x, new_y
                elif new_x > pivot_x and new_y < pivot_y:
                    moves.remove([i, j, new_x, new_y])
                new_x += 1
                new_y -= 1

            new_x, new_y = i + 1, j + 1
            pivot_x, pivot_y = 7, 7
            while (0 <= new_x <= 7) and (0 <= new_y <= 7):
                if self.board[new_x][new_y] != ' 0':
                    pivot_x, pivot_y = new_x, new_y
                elif new_x > pivot_x and new_y > pivot_y:
                    moves.remove([i, j, new_x, new_y])
                new_x += 1
                new_y += 1

        return moves
             
    def make_move(self, move):
        self.game_log += str(move)
        i, j, new_x, new_y = move
        if i == new_x and j == new_y:
            self.block_count += 1
        else:
            self.board[new_x][new_y] = self.board[i][j]
            self.board[i][j] = ' 0'
            self.current_color = self.get_board_color(new_x, new_y)
            self.last_player = self.current_player
            self.block_count = 0

    def loss_condition(self):
        # Check if the opponent's tower reaches the opposite end
        for j in range(8):
            if self.board[0][j][1] == '2':
                return True
            if self.board[7][j][1] == '1':
                return True
        
        if self.block_count == 2:
            if self.possible_moves()[0][0] == self.possible_moves()[0][2] and self.possible_moves()[0][1] == self.possible_moves()[0][3]:
                return True
        return False

    def is_over(self):
        return self.loss_condition()

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

#if __name__ == "__main__":
#    # Initialize the game with AI and human players
#    game = Kamisado([AI_Player(Negamax(5)), AI_Player(Negamax(5))])

#    # Start playing the game
#    game.play()
#    # print(game.board)
#    print("game log :\n" + game.game_log)
    


if __name__ == "__main__":
    # Initialize the game with one AI player and one human player
    game = Kamisado([AI_Player(Negamax(5)), Human_Player()])
    game.play()
    print("game log :\n" + game.game_log)