from icons import icons, abbrev


class Manipulate:

    def __init__(self, col, row, icon, player):
        self.col = col
        self.row = row
        self.icon = icon
        self.player = player


class ChessBoard:

    # the constructor function
    def __init__(self, path=None):
        # if no map file path is specified
        if path is None:
            # set up dimesions
            self._col = 5
            self._row = 3
            # init
            self._board = [['' for r in range(self._row)] for c in range(self._col)]
        else:
            # read from the map file
            # path must not be none
            self._col, self._row = self._load_from_file(path)

    def update(self, manipulate):
        if (manipulate.col >= self._col) or \
                (manipulate.row >= self._row) or \
                (manipulate.icon not in icons.keys()):
            raise ValueError
        self._board[manipulate.col][manipulate.row] = manipulate.icon

    def load(self, board):
        if len(board) != col or len(board[0]) != row:
            raise ValueError
        self._board = board

    # load the chessboard from specified map file
    # return the column / row number of the chessboard
    def _load_from_file(self, path):
        self._board = []
        with open(path, 'r') as map_file:
            contents = map_file.readlines()
        col, row = len(contents[0].strip()), len(contents)
        self._board = [['' for r in range(row)] for c in range(col)]
        for r in range(row):
            for c in range(col):
                self._board[c][r] = abbrev[contents[r][c]]
        return col, row

    def get(self, col, row):
        return self._board[col][row]

    def size(self):
        return (self._col, self._row)
