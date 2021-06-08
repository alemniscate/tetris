import numpy as np 

blank_ = [
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]] 

I = [
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0],
        [0,1,0,0]] 

S = [
        [0,0,0,0],
        [0,1,1,0],
        [1,1,0,0],
        [0,0,0,0]]

Z = [
        [0,0,0,0],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,0,0]]

L = [
        [0,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,0,0]]

J = [
        [0,0,1,0],
        [0,0,1,0],
        [0,1,1,0],
        [0,0,0,0]]

O = [
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0]]

T = [
        [0,1,0,0],
        [1,1,1,0],
        [0,0,0,0],
        [0,0,0,0]]

class Piece:

    def __init__(self, id):
        self.id = id
        self.shape, self.degree = self.get_initial_shape()
   
        left_rotate = np.array([[0, -1], [1, 0]])
        down_rotate = np.array([[-1, 0], [0, -1]])
        right_rotate = np.array([[0, 1], [-1, 0]])
        left_bias = np.array([3, 0])
        down_bias = np.array([3, 3])
        right_bias = np.array([0, 3])
        self.left_rotate_dict = self.make_rotate_dict(left_rotate, left_bias)
        self.right_rotate_dict = self.make_rotate_dict(right_rotate, right_bias)
        self.down_rotate_dict = self.make_rotate_dict(down_rotate, down_bias)

    def get_initial_shape(self):

        if self.id == "I":
            shape = I
        elif self.id == "S":
            shape = S    
        elif self.id == "Z":
            shape = Z    
        elif self.id == "J":
            shape = J    
        elif self.id == "O":
            shape = O    
        elif self.id == "T":
            shape = T
        elif self.id == "L":
            shape = L
        else:
            shape = blank_    

        shape = np.array(shape)
        degree = 0

        if self.id == "T":
            degree = 270

        return shape, degree

    def show(self):

        shape = self.get_current_shape()

        for row in shape:
            for i, col in enumerate(row):
                if i > 0:
                    print(" ", end="")
                if col == 1:
                    print("0", end="")
                else:
                    print("-", end="")
            print()           
    
        print()

    def make_rotate_dict(self, rotate_matrix, bias_vector):
        rotate_dict = {}
        for i in range(4):
            for j in range(4):
                vector = np.array([i, j])
                result_vector = rotate_matrix.dot(vector) + bias_vector
                key = tuple(vector)
                value = tuple(result_vector)
                rotate_dict[key] = value
        return rotate_dict

    def rotate_shape(self, rotate_dict):
        new_shape = [
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]] 

        for i in range(4):
            for j in range(4):
                key = tuple([i, j])
                value = rotate_dict[key]
                row, col = value
                new_shape[row][col] = self.shape[i][j]

        return np.array(new_shape)

    def up_shape(self, shape):
        for i in range(1, 4):
            shape[i - 1] = shape[i]
        shape[3] = [0, 0, 0, 0]
        return shape

    def left_shape(self, shape):
        for i in range(4):
            for j in range(1, 4):
                shape[i][j - 1] = shape[i][j]
            shape[i][3] = 0
        return shape

    def right_shape(self, shape):
        for i in range(4):
            for j in range(1, 4):
                shape[i][4 - j] = shape[i][4 - j - 1]
            shape[i][0] = 0
        return shape

    def rotate(self):
        self.degree += 90
        if self.degree == 360:
            self.degree = 0

    def copy_shape(self):
        new_shape = [
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0],
                    [0,0,0,0]]

        for i in range(4):
            for j in range(4):
                new_shape[i][j] = self.shape[i][j] 
        
        return new_shape

    def get_current_shape(self):
        if self.id == "O":
            shape1 = self.copy_shape()
            return self.up_shape(shape1)

        if self.degree == 0:
            shape1 = self.copy_shape()
            if self.id in ("S"):
                shape1 = self.up_shape(shape1)
            if self.id in ("Z"):
                shape1 = self.up_shape(shape1)
                shape1 = self.right_shape(shape1)
            return shape1

        elif self.degree == 90: 
            shape1 = self.rotate_shape(self.left_rotate_dict)
            if self.id in ("S"):
                shape1 = self.up_shape(shape1)
            if self.id in ("T"):
                shape1 = self.up_shape(shape1)
                shape1 = self.right_shape(shape1)
            if self.id in ("Z", "L", "J"):
                shape1 = self.up_shape(shape1)
            if self.id in ("I"):
                shape1 = self.up_shape(shape1)
                shape1 = self.up_shape(shape1)
            return shape1

        elif self.degree == 180:
            shape1 = self.rotate_shape(self.down_rotate_dict)
            if self.id in ("L"):
                shape1 = self.up_shape(shape1)
            if self.id in ("T"):
                shape1 = self.up_shape(shape1)
                shape1 = self.up_shape(shape1)
            if self.id in ("J", "Z", "S"):
                shape1 = self.up_shape(shape1)
            if self.id in ("I"):
                shape1 = self.left_shape(shape1)
            return shape1

        elif self.degree == 270:
            shape1 = self.rotate_shape(self.right_rotate_dict)
            if self.id in ("T"):
                shape1 = self.left_shape(shape1)
            if self.id in ("J"):
                shape1 = self.up_shape(shape1)
            return shape1

class Field:

    def __init__(self):
        self.dimensions = (10, 20)
        self.piece = Piece("blank")
        self.matrix = self.get_new_matrix()
        self.gameover = False
    
    def get_new_matrix(self):
        row, col = self.dimensions
        matrix = []
        for i in range(row): 
            cols = [0] * col
            matrix.append(cols)
        return matrix

    def copy_matrix(self):
        new_matrix = self.get_new_matrix()
        row, col = self.dimensions
        for i in range(row):
            for j in range(col):
                new_matrix[i][j] = self.matrix[i][j] 
        
        return new_matrix

    def get_matrix(self):
        if self.freeze:
            return self.matrix

        matrix = self.copy_matrix()
        shape = self.piece.get_current_shape()
        row_lowpos, col_lowpos = self.pos
        row_highpos = row_lowpos + 4
        col_highpos = col_lowpos + 4
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if row_lowpos <= row < row_highpos and col_lowpos <= col < col_highpos:
                        if shape[row - row_lowpos][col - col_lowpos] == 1:
                            matrix[row][col] = shape[row - row_lowpos][col - col_lowpos]
                            if matrix[row][col] == 1:
                                if row == self.dimensions[0] - 1:
                                    self.freeze = True
                                else:
                                    if matrix[row + 1][col] == 1:
                                        self.freeze = True

        if self.freeze:
            self.matrix = matrix

        return matrix

    def get_piece_matrix(self):
        matrix = self.get_new_matrix()
        shape = self.piece.get_current_shape()
        row_lowpos, col_lowpos = self.pos
        row_highpos = row_lowpos + 4
        col_highpos = col_lowpos + 4
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if row_lowpos <= row < row_highpos and col_lowpos <= col < col_highpos:
                        matrix[row][col] += shape[row - row_lowpos][col - col_lowpos]
        return matrix

    def is_validpos(self, pos):
        matrix = self.copy_matrix()
        shape = self.piece.get_current_shape()
        row_lowpos, col_lowpos = pos
        row_highpos = row_lowpos + 4
        col_highpos = col_lowpos + 4
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if row_lowpos <= row < row_highpos and col_lowpos <= col < col_highpos:
                        matrix[row][col] += shape[row - row_lowpos][col - col_lowpos]
                        if matrix[row][col] == 2:
                            return False
        return True

    def show_blank(self):
        self.show(blank=True)

    def show(self, blank=False, gameover_check=True, break_row=False):
        if blank:
            matrix = self.get_new_matrix()
        else:
            matrix = self.get_matrix()
            if self.freeze and break_row:
                deleterow = self.get_delete_row(matrix)
                while deleterow >= 0:
                    self.delete_row(deleterow, matrix)
                    deleterow = self.get_delete_row(matrix)
                    self.matrix = matrix

        for row in matrix:
            for i, col in enumerate(row):
                if i > 0:
                    print(" ", end="")
                if col == 1:
                    print("0", end="")
                else:
                    print("-", end="")
            print()           
    
        print()

        if gameover_check and self.is_gameover(matrix):
            self.gameover = True
            print("Game Over!")

    def is_gameover(self, matrix):
        col_sums = np.array(matrix).sum(axis=0)
        if col_sums.max() == self.dimensions[0]:
            return True
        return False

    def get_delete_row(self, matrix):
        index = -1
        for i, row in enumerate(matrix):
            if np.array(row).sum() == self.dimensions[1]:  
                index = i
        return index  

    def delete_row(self, row, matrix):
        for i in reversed(range(row)):
            matrix[i + 1] = matrix[i]
        matrix[0] = [0] * self.dimensions[1]

    def add_piece(self, id):
        self.piece = Piece(id)
        self.pos = (0, 3)
        self.freeze = False

    def add_dimensions(self, row, col):
        self.dimensions = (row, col)

    def is_leftwall(self):
        matrix = self.get_piece_matrix()
        for row in matrix:
            if row[0] == 1:
                return True
        return False           

    def is_rightwall(self):
        matrix = self.get_piece_matrix()
        for row in matrix:
            if row[-1] == 1:
                return True
        return False           

    def move_left(self):
        if self.freeze:
            self.show()
            return
        row, col = self.pos
        row += 1
        if not self.is_leftwall() and self.is_validpos((row, col - 1)):
            col -= 1
        if self.is_validpos((row, col)):
            self.pos = (row, col)
        self.show()

    def move_right(self):
        if self.freeze:
            self.show()
            return
        row, col = self.pos
        row += 1
        if not self.is_rightwall() and self.is_validpos((row, col + 1)):
            col += 1
        if self.is_validpos((row, col)):
            self.pos = (row, col)
        self.show()

    def move_down(self):
        if self.freeze:
            self.show()
            return
        row, col = self.pos
        row += 1
        if self.is_validpos((row, col)):
            self.pos = (row, col)
        self.show()
    
    def rotate(self):
        if self.freeze:
            self.show()
            return
        self.piece.rotate()
        row, col = self.pos
        row += 1
        if self.is_validpos((row, col)):
            self.pos = (row, col)
        self.show()

field = Field()
while not field.gameover:
    input_command = input()
    if input_command == "":
        continue
    command = input_command.split()
    if command[0] == "piece":
        continue
    if command[0] == "exit":
        break
    elif command[0] in ("I", "S", "Z", "L", "J", "O", "T"):
        id = command[0]
        field.add_piece(id)
        field.show(gameover_check=False)
    elif command[0].isnumeric():
        col = int(command[0])
        row = int(command[1])
        field.add_dimensions(row, col)
        print()
        field.show_blank()
    elif command[0] == "left":
        field.move_left()
    elif command[0] == "right":
        field.move_right()
    elif command[0] == "down":
        field.move_down()
    elif command[0] == "rotate":
        field.rotate()
    elif command[0] == "break":
        field.show(break_row=True)

