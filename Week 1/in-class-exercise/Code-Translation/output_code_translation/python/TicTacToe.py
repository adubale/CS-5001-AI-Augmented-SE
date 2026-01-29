from typing import List

class TicTacToe:
    def __init__(self, N: int = 3):
        # board is a 3xN grid initialized with spaces
        self.board: List[List[str]] = [[' ' for _ in range(N)] for _ in range(3)]
        self.current_player: str = 'X'

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        else:
            return False

    def check_winner(self) -> str:
        # Check rows
        for row in self.board:
            if row[0] != ' ' and row[0] == row[1] == row[2]:
                return row[0]

        # Check columns
        for col in range(3):
            if (self.board[0][col] != ' ' and
                self.board[0][col] == self.board[1][col] == self.board[2][col]):
                return self.board[0][col]

        # Check diagonals
        if (self.board[0][0] != ' ' and
            self.board[0][0] == self.board[1][1] == self.board[2][2]):
            return self.board[0][0]

        if (self.board[0][2] != ' ' and
            self.board[0][2] == self.board[1][1] == self.board[2][0]):
            return self.board[0][2]

        return '\0'

    def is_board_full(self) -> bool:
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def get_current_player(self) -> str:
        return self.current_player
