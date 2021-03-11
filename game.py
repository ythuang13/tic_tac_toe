class TicTacToe:

    def __init__(self):
        self._round = 0
        self._board = [["", "", ""] for _ in range(3)]
        self._player1_score = self._player2_score = 0
        self._current_player = None
        self._win_move = None
        self._winner = None

    def __str__(self):
        board = "\n"
        for x in range(3):
            for y in range(3):
                if self._board[x][y] == "":
                    board += "_"
                else:
                    board += self._board[x][y]
            board += "\n"

        return board

    @property
    def current_player(self) -> int:
        return self._current_player

    @current_player.setter
    def current_player(self, cur_p) -> None:
        self._current_player = cur_p

    @property
    def score(self) -> tuple:
        return self._player1_score, self._player2_score

    @property
    def round(self) -> int:
        return self._round

    @property
    def board(self) -> list:
        return self._board

    @property
    def win_move(self) -> int:
        return self._win_move

    @property
    def winner(self) -> str:
        return self._winner

    def play_move(self, x: int, y: int, char: str):
        if 0 <= x <= 2 and 0 <= y <= 2:
            if self._board[x][y] == "":
                if self._round % 2 == 0 and char == "X":
                    self._board[x][y] = "X"
                    self._round += 1
                elif self._round % 2 == 1 and char == "O":
                    self._board[x][y] = "O"
                    self._round += 1
            else:
                print("Filled")
        print(self)

    def clear_board(self):
        self._board = [["", "", ""] for _ in range(3)]
        self._winner = None
        self._win_move = None

    def full_reset(self):
        self.clear_board()
        self._round = 0
        self._player1_score = self._player2_score = 0

    def check_win(self):
        b = self._board
        is_winner = False
        if b[0][0] == b[0][1] == b[0][2] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 1
        elif b[0][0] == b[0][1] == b[0][2] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 1
        elif b[1][0] == b[1][1] == b[1][2] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 2
        elif b[1][0] == b[1][1] == b[1][2] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 2
        elif b[2][0] == b[2][1] == b[2][2] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 3
        elif b[2][0] == b[2][1] == b[2][2] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 3
        elif b[0][0] == b[1][0] == b[2][0] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 4
        elif b[0][0] == b[1][0] == b[2][0] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 4
        elif b[0][1] == b[1][1] == b[2][1] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 5
        elif b[0][1] == b[1][1] == b[2][1] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 5
        elif b[0][2] == b[1][2] == b[2][2] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 6
        elif b[0][2] == b[1][2] == b[2][2] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 6
        elif b[0][0] == b[1][1] == b[2][2] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 7
        elif b[0][0] == b[1][1] == b[2][2] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 7
        elif b[0][2] == b[1][1] == b[2][0] == "O":
            self._player2_score += 1
            self._winner = "O"
            self._win_move = 8
        elif b[0][2] == b[1][1] == b[2][0] == "X":
            self._player1_score += 1
            self._winner = "X"
            self._win_move = 8

        if is_winner:
            self.clear_board()
        elif "" not in b[0] + b[1] + b[2]:
            print("Tie!")
            self.clear_board()
