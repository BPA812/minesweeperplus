import random
import re

class Board:
    def __init__(self, p1, p2):
        
        self.v3, self.v4 = p1, p2

        self.v2 = self.f1() 
        self.f2()
        self.v1 = set()

    def f1(self):
        board = [[None for _ in range(self.v3)] for _ in range(self.v3)]
        v1 = 0
        while v1 < self.v4:
            loc = random.randint(0, self.v3**2 - 1)
            row = loc // self.v3
            col = loc % self.v3

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            v1 += 1

        return board

    def f2(self):
        for r in range(self.v3):
            for c in range(self.v3):
                if self.v2[r][c] == '*':
                    continue
                self.v2[r][c] = self.f3(r, c)

    def f3(self, row, col):
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.v3-1, row+1)+1):
            for c in range(max(0, col-1), min(self.v3-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.v2[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def f4(self, row, col):
        self.v1.add((row, col))
        if self.v2[row][col] == '*':
            return False
        elif self.v2[row][col] > 0:
            return True
        for r in range(max(0, row-1), min(self.v3-1, row+1)+1):
            for c in range(max(0, col-1), min(self.v3-1, col+1)+1):
                if (r, c) in self.v1:
                    continue
                self.f4(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.v3)] for _ in range(self.v3)]
        for row in range(self.v3):
            for col in range(self.v3):
                if (row,col) in self.v1:
                    visible_board[row][col] = str(self.v2[row][col])
                else:
                    visible_board[row][col] = ' '
        string_rep, widths = '', []
        for idx in range(self.v3):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )
        indices = [i for i in range(self.v3)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.v3)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
def f5(p3=10, p4=10):
    board = Board(p3, p4)
    safe = True 

    while len(board.v1) < board.v3 ** 2 - p4:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.v3 or col < 0 or col >= p3:
            print("Invalid location. Try again.")
            continue
        safe = board.f4(row, col)
        if not safe:
            break
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY GAME OVER :(")
        board.v1 = [(r,c) for r in range(board.v3) for c in range(board.v3)]
        print(board)

if __name__ == '__main__':
    f5()
