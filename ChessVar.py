# Author: Colton Woodruff
# GitHub username: coltwood93
# Date: 08/07/2023
# Description: CS 162 final project - a variant of chess to demonstrate all concepts learned this quarter

class Piece:
    """
    Represents a generic chess piece object
    Will be inherited by specific classes
    """
    def __init__(self, color, pos):
        self._color = color
        self._symbol = self._color[0]   # creates text representation for printed chess board
        self._available_moves = []
        self._pos = pos
        self._type = None

    def get_color(self):
        """Returns color of game piece"""
        return self._color

    def get_symbol(self):
        """Returns symbol of game piece"""
        return self._symbol

    def get_available_moves(self):
        """Returns available_moves of game piece"""
        return self._available_moves

    def get_type(self):
        """Returns type of game piece"""
        return self._type

    def get_pos(self):
        """Returns piece position"""
        return self._pos

    def set_pos(self, pos):
        """Set new position for piece"""
        self._pos = pos


class Rook(Piece):
    """Represents a rook object"""
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self._symbol += 'R'
        self._type = 'rook'

    def update_moves(self, piece_locations, test_location = None):
        """Returns available spaces rook can move (before testing for legal takes or checking king"""
        moves = []
        row, col = self._pos // 8, self._pos % 8    # convert chess notation to row, col notation with zero index

        # allow overriding current position with hypothetical position for testing if move will put king in check
        if test_location is None:
            location = self._pos
        else:
            location = test_location

        # check possible moves. iteratively adds squares in each direction until board edge or other piece are found.
        # find all valid moves down
        count = 1
        while row - count > -1:
            moves.append(location - (count*8))
            if location - (count*8) in piece_locations:
                break
            count += 1

        # find all valid moves up
        count = 1
        while row + count < 8:
            moves.append(location + (count*8))
            if location + (count*8) in piece_locations:
                break
            count += 1

        # find all valid moves left
        count = 1
        while col - count > -1:
            moves.append(location - count)
            if location - count in piece_locations:
                break
            count += 1

        # find all valid moves right
        count = 1
        while col + count < 8:
            moves.append(location + count)
            if location + count in piece_locations:
                break
            count += 1

        # if testing hypothetical space, don't update pieces actual available moves. return for us in check_checker()
        if test_location is None:
            self._available_moves = moves
        else:
            return moves


class Bishop(Piece):
    """Represents a bishop object"""
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self._symbol += 'B'
        self._type = 'bishop'

    def update_moves(self, piece_locations, test_location = None):
        """Returns available spaces piece can move"""
        moves = []
        row, col = self._pos // 8, self._pos % 8

        # allow overriding current position with hypothetical position for testing if move will put king in check
        if test_location is None:
            location = self._pos
        else:
            location = test_location

        # check possible moves. iteratively adds squares in each direction until board edge or other piece are found.
        # find all valid moves down-left
        count = 1
        while row - count > -1 and col - count > -1:
            moves.append(location - (count * 9))
            if location - (count * 9) in piece_locations:
                break
            count += 1

        # find all valid moves up-left
        count = 1
        while row + count < 8 and col - count > -1:
            moves.append(location + (count * 7))
            if location + (count * 7) in piece_locations:
                break
            count += 1

        # find all valid moves down-right
        count = 1
        while row - count > -1 and col + count < 8:
            moves.append(location - (count * 7))
            if location - (count * 7) in piece_locations:
                break
            count += 1

        # find all valid moves up-right
        count = 1
        while row + count < 8 and col + count < 8:
            moves.append(location + (count * 9))
            if location + (count * 9) in piece_locations:
                break
            count += 1

        # if testing hypothetical space, don't update pieces actual available moves. return for us in check_checker()
        if test_location is None:
            self._available_moves = moves
        else:
            return moves


class Knight(Piece):
    """Represents a knight object"""
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self._symbol += 'N'
        self._type = 'knight'

    def update_moves(self, piece_locations, test_location = None):
        """Returns available spaces piece can move"""

        # allow overriding current position with hypothetical position for testing if move will put king in check
        if test_location is None:
            location = self._pos
        else:
            location = test_location

        # on linear chess board, list of distances to valid knight moves
        possible_movement = [-10, 6, -17, 15, -15, 17, -6, 10]

        #remove possible moves that extend beyond left or right board edge
        if location % 8 == 0:
            possible_movement = possible_movement[2:]
        if location % 8 == 1:
            possible_movement = possible_movement[1:]
        if location % 8 == 6:
            possible_movement = possible_movement[:-1]
        if location % 8 == 7:
            possible_movement = possible_movement[:-2]

        # remove possible moves if above or below board edge
        moves = [location + move for move in possible_movement if -1 < location + move < 64]

        # if testing hypothetical space, don't update pieces actual available moves. return for us in check_checker()
        if test_location is None:
            self._available_moves = moves
        else:
            return moves


class King(Piece):
    """Represents a king object"""
    def __init__(self, color, pos):
        super().__init__(color, pos)
        self._symbol += 'K'
        self._type = 'king'

    def update_moves(self, piece_locations, test_location=None):
        """Returns available spaces piece can move"""

        # allow overriding current position with hypothetical position for testing if move will put king in check
        if test_location is None:
            location = self._pos
        else:
            location = test_location

        #remove possible moves that extend beyond left or right board edge
        possible_movement = [-9, -1, 7, -8, 8, -7, 1, 9]

        #remove possible moves that extend beyond left or right board edge
        if location % 8 == 0:
            possible_movement = possible_movement[3:]
        if location % 8 == 7:
            possible_movement = possible_movement[:-3]

        # remove possible moves if above or below board edge
        moves = [location + move for move in possible_movement if -1 < location + move < 64]

        # if testing hypothetical space, don't update pieces actual available moves. return for us in check_checker()
        if test_location is None:
            self._available_moves = moves
        else:
            return moves


class ChessVar:
    """Represents a chess board object, on which a variant of chess is played"""
    def __init__(self):
        self._turn = 'White'    # white starts the game
        self._game_state = 'UNFINISHED'
        self._board_index = []  # list of spaces in chess notation for conversion to zero-index numbering
        self._board_pieces = {} # dictionary of chess piece objects keyed to their position in chess notation
        self._white_moves = set()   # set of all potential white piece moves for checking if king is in check
        self._black_moves = set()   # set of all potential black piece moves for checking if king is in check

        # add list of board spaces in chess notation to _board_index list
        for num in range(8):
            for letter in 'abcdefgh':
                self._board_index.append(letter + str(num + 1))

        # initiate lists of chess pieces and their starting locations
        start_squares = ['a1', 'b1', 'c1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'f2', 'g2', 'h2']
        start_pieces = [King('White', 0),Bishop('White', 1),Knight('White', 2),
                        Knight('Black', 5),Bishop('Black', 6),King('Black', 7),
                        Rook('White', 8),Bishop('White', 9),Knight('White', 10),
                        Knight('Black', 13),Bishop('Black', 14),Rook('Black', 15)]

        #   add pieces to _board_pieces dictionary
        for key, piece in zip(start_squares, start_pieces):
            self._board_pieces[key] = piece

        # update each pieces available moves and add to corresponding team set
        for piece in self._board_pieces.values():
            piece.update_moves(self._board_pieces.keys())
            if piece.get_color() == 'White':
                self._white_moves.update(piece.get_available_moves())
            else:
                self._black_moves.update(piece.get_available_moves())

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def get_turn(self):
        """Returns current game turn"""
        return self._turn

    def game_update(self):
        """Updates game state and color turn"""
        # find current row of each team king
        white_king_row = [x.get_pos() // 8 for x in self._board_pieces.values() if
                          x.get_type() == 'king' and x.get_color() == 'White']
        black_king_row = [x.get_pos() // 8 for x in self._board_pieces.values() if
                          x.get_type() == 'king' and x.get_color() == 'Black']

        # check if white has ended turn without reaching end and advance turn
        if self._turn == 'White':
            self._turn = 'Black'
        # check if white finished on previous turn and black did not finish on current turn
        elif white_king_row[0] == 7 and black_king_row[0] < 7:
            self._game_state = 'WHITE_WON'
        # check if white finished then black finished on next turn
        elif black_king_row[0] == 7 and white_king_row[0] == 7:
            self._game_state = 'TIE'
        # check if black has finished before white
        elif black_king_row[0] == 7:
            self._game_state = 'BLACK_WON'
        # if no team has finished, advance to next turn
        else:
            self._turn = 'White'

    def update_moves(self):
        """Updates playable moves and reports if stalemate is reached"""
        # clear both teams available moves
        self._white_moves = set()
        self._black_moves = set()

        # update each pieces available moves and add to corresponding team set
        for piece in self._board_pieces.values():
            piece.update_moves([self._board_index.index(x) for x in self._board_pieces.keys()])
            if piece.get_color() == 'White':
                self._white_moves.update(piece.get_available_moves())
            else:
                self._black_moves.update(piece.get_available_moves())

    def check_checker(self):
        """Returns True if any piece has an available move on the king"""

        for piece in self._board_pieces.values():
        # if moved piece is a king, check if it has moved to a square that can be reached by other team
            if piece.get_type() == 'king' and piece.get_color() == 'White' and piece.get_pos() in self._black_moves:
                return True

            if piece.get_type() == 'king' and piece.get_color() == 'Black' and piece.get_pos() in self._white_moves:
                return True

    def make_move(self, current_square, to_square):
        """Moves game piece at current_square to to_square and updates/advances game"""
        # convert chess notation of selected square to linear index
        if to_square in self._board_index:
            to_index = self._board_index.index(to_square)
        else:
            return False

        # check if selected square is empty
        if current_square in self._board_pieces.keys():
            piece = self._board_pieces[current_square]
        else:
            return False

        # save current piece index in placeholder
        current_index = self._board_pieces[current_square].get_pos()

        # save target piece (if any) in placeholder
        target_piece = None
        if to_square in self._board_pieces:
            target_piece = self._board_pieces[to_square]

        # check if game is over
        if self._game_state != 'UNFINISHED':
            return False
        # check if piece was selected out of turn
        elif piece.get_color() != self._turn:
            return False
        # check if move-to-square is reachable by piece
        elif to_index not in piece.get_available_moves():
            return False
        # check if move-to-square is occupied by another piece of the same team
        elif (to_square in self._board_pieces.keys() and
                self._board_pieces[to_square].get_color() == piece.get_color()):
            return False
        # if all checks are good, make move
        else:
            self._board_pieces[to_square] = self._board_pieces.pop(current_square)
            self._board_pieces[to_square].set_pos(to_index)
            self.update_moves()

        # check if movement puts either king in check
        if self.check_checker():
            self._board_pieces[current_square] = self._board_pieces.pop(to_square)
            self._board_pieces[current_square].set_pos(current_index)
            if target_piece is not None:
                self._board_pieces[to_square] = target_piece
            self.update_moves()
            return False

        # update game state and refresh all pieces available moves
        self._board_pieces[to_square].set_pos(to_index)
        self.game_update()
        return True

    def print_board(self):
        """
        Prints game board to console
        Used for testing/debugging code
        """
        icons = []

        # create representation of chess board with piece._symbols and blank squares
        for square in self._board_index:
            if square in self._board_pieces.keys():
                icons.append(self._board_pieces[square].get_symbol())
            else:
                icons.append('__')

        # print each board row to console
        while len(icons) > 0:
            print(icons[-8:])
            icons = icons[:-8]

        print('\n\n')


def main():
    bd = ChessVar()
    bd.make_move('a2','a7')
    bd.make_move('f2', 'g4')
    bd.make_move('b2', 'f6')
    bd.make_move('g1', 'a7')
    bd.make_move('c2', 'e1')
    bd.make_move('g4', 'f6')
    bd.make_move('e1', 'g2')
    bd.make_move('h1', 'g2')
    bd.make_move('c1', 'e2')
    bd.make_move('g2', 'h3')
    bd.print_board()
    bd.make_move('b1', 'f5')
    bd.print_board()
    bd.make_move('h2', 'e2')
    bd.make_move('a1', 'a2')

if __name__ == '__main__':
    main()