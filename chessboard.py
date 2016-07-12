from icons import icons


class Manipulate:

    def __init__(self, col, row, icon, player):
        self.col = col
        self.row = row
        self.icon = icon
        self.player = player


class ChessBoard:

    def __init__(self, col, row):
        # set up dimesions
        self._col = col
        self._row = row
        # set up counter variable
        self.upd_counter = 0
        # init
        self._board = [['' for r in range(row)] for c in range(col)]

    def update(self, manipulate):
        if (manipulate.col >= self.col) or \
                (manipulate.row >= self.row) or \
                (manipulate.icon not in icons.keys()):
            raise ValueError
        self._board[manipulate.col][manipulate.row] = manipulate.icon
        self.udp_counter += 1

    def load(self, board):
        if len(board) != col or len(board[0]) != row:
            raise ValueError
        self._board = board

    def get(self, col, row):
        return self._board[col][row]

    def size(self):
        return (self._col, self._row)
