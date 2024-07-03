import pygame
from constants import *
import random


transposition_table = {}

symbol = {
        "cross": 1,
        "circle": 2,
        "blank": 0,
        "max": 1,
        "min": 2
    }

agent = {
        "human": 0,
        "AI": 1
    }

def p(s):
    if(s == symbol["circle"]):
        return 1
    if(s == symbol["cross"]):
        return 0
    


class Board:
    # The att of the class is
    # self.size: the size of the board (by default 6*6)
    # self.__player_turn_symbol
    # self.__turn_number
    # self.SQUARE_SIZE
    # self.CIRCLE_RADIUS
    # self.cross_player_score & self.circle_player_score
    # self.representation: a unique string representation of the board
    def __init__(self, size = 6):
        self.size = size
        if(size < 4 or size > 12):
            self.size = 6
        self.__player_turn_symbol = symbol["cross"]
        self.hovered_square = (-1, -1)
        self.__turn_number = 1

        self.SQUARE_SIZE = BOARD_SIZE / self.size - LINE_WIDTH
        self.CIRCLE_RADIUS = (self.SQUARE_SIZE / 2) - SQUARE_PADDING

        self.cross_player_score = self.circle_player_score = self.cross_player_score_2 = self.cross_player_score_3 = self.circle_player_score_2 = self.circle_player_score_3 = 0
        self.cross_player_situation = self.circle_player_situation = 0

        self.representation = f"{symbol['blank']}" * self.size * self.size

    @property
    def cross_player_score(self):
        return self.__cross_player_score
    
    @cross_player_score.setter
    def cross_player_score(self, value):
        self.__cross_player_score = value
    
    @property
    def circle_player_score(self):
        return self.__circle_player_score
    
    @circle_player_score.setter
    def circle_player_score(self, value):
        self.__circle_player_score = value
    
    @property
    def size(self):
        return self.__size
    
    @size.setter
    def size(self, value):
        if(value < 4 or value > 12):
            print("invalid board size")
        else:
            self.__size = value
            self.representation = f"{symbol['blank']}" * self.size * self.size

    # sets the cell provided according to self.__player_turn_symbol
    # updates self.representation
    # updates self.player_turn_symbol
    # updates self.__turn_number
    # updates self.circle_player_score and self.cross_player_score
    # returns true or false (if the provided row and col are valid and everything goes ok or not)
    def set_cell(self, row, col):
        if row >= self.size or col >= self.size or row < 0 or col < 0:
             return False
        
        if self.representation[row * self.size + col] == str(symbol["blank"]):
            self.update_string_representation(row, col)

            if(self.player_turn_symbol == symbol["circle"]):
                self.circle_player_score += self.player_score_update(self.player_turn_symbol, row, col)
                self.circle_player_score_2 += self.player_score_update(self.player_turn_symbol, row, col, 2)
                self.circle_player_score_3 += self.player_score_update(self.player_turn_symbol, row, col, 3)
                self.cross_player_situation += self.player_situation_update(symbol["cross"], row, col)

            else:
                self.cross_player_score += self.player_score_update(self.player_turn_symbol, row, col)
                self.cross_player_score_2 += self.player_score_update(self.player_turn_symbol, row, col, 2)
                self.cross_player_score_3 += self.player_score_update(self.player_turn_symbol, row, col, 3)
                self.circle_player_situation += self.player_situation_update(symbol["circle"], row, col)
            
            
            self.player_turn_symbol = 1 # to update it
            self.__turn_number += 1
            
            return True
        
        return False
    
    @property
    def player_turn_symbol(self):
         return self.__player_turn_symbol
    
    @player_turn_symbol.setter
    def player_turn_symbol(self, n):
         if self.__player_turn_symbol == symbol["cross"]:
              self.__player_turn_symbol = symbol["circle"]
              return

         if self.__player_turn_symbol == symbol["circle"]:
              self.__player_turn_symbol = symbol["cross"]

    @property
    def turn_number(self):
         return self.__turn_number
    
    @property
    def hovered_square(self):
         return self.__hovered_square
    
    @hovered_square.setter
    def hovered_square(self, position):
         self.__hovered_square = position

    def player_score(self, symbol, n=4):
        board = self.representation
        size = self.size
        total_count = 0

        # Check horizontal lines
        for row in range(size):
            for col in range(size - n + 1):
                if all(board[row * size + col + i] == str(symbol) for i in range(n)):
                    total_count += 1

        # Check vertical lines
        for col in range(size):
            for row in range(size - n + 1):
                if all(board[(row + i) * size + col] == str(symbol) for i in range(n)):
                    total_count += 1

        # Check diagonal down-right lines
        for row in range(size - n + 1):
            for col in range(size - n + 1):
                if all(board[(row + i) * size + col + i] == str(symbol) for i in range(n)):
                    total_count += 1

        # Check diagonal down-left lines
        for row in range(size - n + 1):
            for col in range(n - 1, size):
                if all(board[(row + i) * size + col - i] == str(symbol) for i in range(n)):
                    total_count += 1

        return total_count
    
    def player_score_update(self, symbol, x, y, n=4):
        board = self.representation
        size = self.size
        total_count = 0

        # Check horizontal lines
        for col in range(max(0, y - n + 1), min(size - n + 1, y + 1)):
            if all(board[x * size + col + i] == str(symbol) for i in range(n)):
                total_count += 1

        # Check vertical lines
        for row in range(max(0, x - n + 1), min(size - n + 1, x + 1)):
            if all(board[(row + i) * size + y] == str(symbol) for i in range(n)):
                total_count += 1

        # Check diagonal down-right linesF
        for i in range(n):
            if x - i < 0 or y - i < 0 or x - i + n > size or y - i + n > size:
                continue
            if all(board[(x - i + j) * size + (y - i + j)] == str(symbol) for j in range(n)):
                total_count += 1

        # Check diagonal down-left lines
        for i in range(n):
            if x - i < 0 or y + i >= size or x - i + n > size or y + i - n + 1 < 0:
                continue
            if all(board[(x - i + j) * size + (y + i - j)] == str(symbol) for j in range(n)):
                total_count += 1

        return total_count


    def player_situation_update(self, s, x, y, n=4):
        board = self.representation
        size = self.size
        total_count = 0
        added_s = board[x * size + y]
        situation_not_changed = (added_s == s)
        list_representation = list(board)

        list_representation[x * size + y] = str(symbol["blank"])

        theoretical_old_board = "".join(list_representation)

        if situation_not_changed: return 0



        # Check horizontal lines
        for col in range(max(0, y - n + 1), min(size - n + 1, y + 1)):
            
            if all(theoretical_old_board[x * size + col + i] in [str(s), str(symbol["blank"])] for i in range(n)):
                total_count -= 1

        # Check vertical lines
        for row in range(max(0, x - n + 1), min(size - n + 1, x + 1)):
            
            if all(theoretical_old_board[(row + i) * size + y] in [str(s), str(symbol["blank"])] for i in range(n)):
                total_count -= 1

        # Check diagonal down-right lines
        for i in range(n):
            if x - i < 0 or y - i < 0 or x - i + n > size or y - i + n > size:
                continue

            if all(theoretical_old_board[(x - i + j) * size + (y - i + j)] in [str(s), str(symbol["blank"])] for j in range(n)):
                total_count -= 1

        # Check diagonal down-left lines
        for i in range(n):
            if x - i < 0 or y + i >= size or x - i + n > size or y + i - n + 1 < 0:
                continue

            if all(theoretical_old_board[(x - i + j) * size + (y + i - j)] in [str(s), str(symbol["blank"])] for j in range(n)):
                total_count -= 1

        return total_count


    
    

    def player_situation(self, player_symbol):
        board = self.representation
        size = self.size
        total_count = 0
        n = 4

        # Check horizontal lines
        for row in range(size):
            for col in range(size - n + 1):
                if all(board[row * size + col + i] == str(player_symbol) or board[row * size + col + i] == str(symbol["blank"]) for i in range(n)):
                    total_count += 1

        # Check vertical lines
        for col in range(size):
            for row in range(size - n + 1):
                if all(board[(row + i) * size + col] == str(player_symbol) or board[(row + i) * size + col] == str(symbol["blank"]) for i in range(n)):
                    total_count += 1

        # Check diagonal down-right lines
        for row in range(size - n + 1):
            for col in range(size - n + 1):
                if all(board[(row + i) * size + col + i] == str(player_symbol) or board[(row + i) * size + col + i] == str(symbol["blank"]) for i in range(n)):
                    total_count += 1

        # Check diagonal down-left lines
        for row in range(size - n + 1):
            for col in range(n - 1, size):
                if all(board[(row + i) * size + col - i] == str(player_symbol) or board[(row + i) * size + col - i] == str(symbol["blank"]) for i in range(n)):
                    total_count += 1

        return total_count

    def is_board_full(self):
        return self.representation.find('0') == -1
    
    def reset_board(self, size = 0):
         self.__init__(self.size)

    def draw_board(self, win):
         (mouse_x, mouse_y) = pygame.mouse.get_pos()
         self.hovered_square = (-1, -1)
         for row in range(self.size):
              for col in range(self.size):
                   if(mouse_x <= WINDOW_PADDING + LINE_WIDTH * row + row * self.SQUARE_SIZE + self.SQUARE_SIZE and 
                      mouse_x >= WINDOW_PADDING + LINE_WIDTH * row + row * self.SQUARE_SIZE and 
                      mouse_y <= WINDOW_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE + self.SQUARE_SIZE and 
                      mouse_y >= WINDOW_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE and 
                      self.representation[row * self.size + col] == str(symbol["blank"])):
                        pygame.draw.rect(win, YELLOW, (WINDOW_PADDING + LINE_WIDTH * row + row * self.SQUARE_SIZE, WINDOW_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                        self.hovered_square =  (row, col)
                   else:
                        pygame.draw.rect(win, GRAY, (WINDOW_PADDING + LINE_WIDTH * row + row * self.SQUARE_SIZE, WINDOW_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

         self.draw_figures(win)

         self.display_score(win)

    def draw_cross(self, win, row, col):

         pygame.draw.line(win, RED, (WINDOW_PADDING + SQUARE_PADDING + CROSS_WIDTH/10 + LINE_WIDTH * row + row * self.SQUARE_SIZE, WINDOW_PADDING + SQUARE_PADDING
                                      + LINE_WIDTH * col + col * self.SQUARE_SIZE),
                          (WINDOW_PADDING - (SQUARE_PADDING + CROSS_WIDTH/10)+ LINE_WIDTH * row + row * self.SQUARE_SIZE + self.SQUARE_SIZE,
                             WINDOW_PADDING - SQUARE_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE + self.SQUARE_SIZE), CROSS_WIDTH)
         
         pygame.draw.line(win, RED, (int(WINDOW_PADDING - (SQUARE_PADDING + CROSS_WIDTH/10) + LINE_WIDTH * row + row * self.SQUARE_SIZE + self.SQUARE_SIZE),
                                      int(WINDOW_PADDING + SQUARE_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE)),
                           (int(WINDOW_PADDING + SQUARE_PADDING + CROSS_WIDTH/10 + LINE_WIDTH * row + row * self.SQUARE_SIZE), int(WINDOW_PADDING - SQUARE_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE 
                            + self.SQUARE_SIZE)), CROSS_WIDTH)
    
    def draw_figures(self, win):
         for row in range(self.size):
              for col in range(self.size):
                if self.representation[row * self.size + col] == str(symbol["cross"]):
                    self.draw_cross(win, row, col)
                elif self.representation[row * self.size + col] == str(symbol["circle"]):
                    self.draw_circle(win, row, col)

    def display_score(self, win):
         fontname = 'times'
         fontsize = 38
         font = pygame.font.SysFont(fontname, fontsize)

         label = font.render("Connect 4 game", 1, (255, 255, 255))
         win.blit(label, (WINDOW_PADDING + self.SQUARE_SIZE * self.size + 100 + 50, WINDOW_PADDING))

         fontsize = 24
         font = pygame.font.SysFont(fontname, fontsize)
         # apply it to text on a label
         label = font.render(f"Turn Number: {self.turn_number}", 1, (255, 255, 255))
         # put the label object on the screen at point x=100, y=100
         win.blit(label, (WINDOW_PADDING + self.SQUARE_SIZE * self.size + 100 + 100, WINDOW_PADDING + 500))

         pygame.draw.circle( win, BLUE, (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2,
                                          WINDOW_PADDING + 200), 
                                          25, 7 )
         
         pygame.draw.line(win, RED, (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 - 20, WINDOW_PADDING + 200 + 120),
                          (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 - 20 + 40,
                             WINDOW_PADDING + 200 + 120 + 40), CROSS_WIDTH)
         
         pygame.draw.line(win, RED, (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 - 20 + 40, WINDOW_PADDING + 200 + 120),
                           (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 - 20, WINDOW_PADDING + 200 + 120 + 40), CROSS_WIDTH)
         if self.circle_player_score >= 1:
              if self.cross_player_score >= 1:
                   pass
         label = font.render(f"Score: {self.circle_player_score}", 1, (255, 255, 255))
         win.blit(label, (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 + 50, WINDOW_PADDING + 200 - 12.5))

         label = font.render(f"Score: {self.cross_player_score}", 1, (255, 255, 255))
         win.blit(label, (WINDOW_PADDING + LINE_WIDTH * self.size + self.size * self.SQUARE_SIZE + 100 + self.SQUARE_SIZE/2 + 50, WINDOW_PADDING + 200 + 8 + 120))

         self.display_winner(win)

    def draw_circle(self, win, row, col):
         pygame.draw.circle( win, BLUE, (WINDOW_PADDING + LINE_WIDTH * row + row * self.SQUARE_SIZE + self.SQUARE_SIZE / 2,
                                          WINDOW_PADDING + LINE_WIDTH * col + col * self.SQUARE_SIZE + self.SQUARE_SIZE / 2), 
                                          self.CIRCLE_RADIUS, CIRCLE_WIDTH )
    
    def display_winner(self, win):
         if(self.turn_number >= self.size * self.size + 1):
             fontname = 'times'
             fontsize = 24
             font = pygame.font.SysFont(fontname, fontsize)

             winner = "Tie"

             if(self.circle_player_score > self.cross_player_score):
                 winner = "Circle player wins"
                 label = font.render(winner, 1, (255, 255, 255))
                 win.blit(label, (WINDOW_PADDING + self.SQUARE_SIZE * self.size + 100 + 50 + 40, 630))
                 return
             elif(self.circle_player_score < self.cross_player_score):
                 winner = "Cross player wins"
                 label = font.render(winner, 1, (255, 255, 255))
                 win.blit(label, (WINDOW_PADDING + self.SQUARE_SIZE * self.size + 100 + 50 + 40, 630))
                 return
        
             label = font.render("Tie", 1, (255, 255, 255))
             win.blit(label, (WINDOW_PADDING + self.SQUARE_SIZE * self.size + 100 + 50 + 110, 630))
    
    # a quick way to update the string representation of the board
    # according to the change happend and the old representation
    # better then creating it from  scratch using string_representation
    # function.
    def update_string_representation(self, i, j):
         list_representation = list(self.representation)

         list_representation[i * self.size + j] = str(self.__player_turn_symbol)

         self.representation = "".join(list_representation)

    # Make a custom copy of the board in a fast and optimized way
    # that is needed in the minimax algorithm
    def custom_copy(self):
        new_board = Board(self.size)
        new_board.__player_turn_symbol = self.__player_turn_symbol
        # new_board.hovered_square = self.hovered_square # not needed in the minmax algo
        new_board.__turn_number = self.__turn_number # not needed in the minmax algo
        new_board.cross_player_score = self.cross_player_score
        new_board.cross_player_score_2 = self.cross_player_score_2
        new_board.cross_player_score_3 = self.cross_player_score_3
        new_board.circle_player_score = self.circle_player_score
        new_board.circle_player_score_2 = self.circle_player_score_2
        new_board.circle_player_score_3 = self.circle_player_score_3
        new_board.cross_player_situation = self.cross_player_situation
        new_board.circle_player_situation = self.circle_player_situation
        new_board.representation = self.representation

        return new_board
    
    #some functions used for debugging
    def generate_random_board(self):
        representation = []

        for i in range(self.size * self.size):
            representation.append(str(random.randint(0, 2)))

        self.representation = "".join(representation)

        self.cross_player_score = self.player_score(symbol["cross"])
        self.circle_player_score = self.player_score(symbol["circle"])

        self.cross_player_score_2 = self.player_score(symbol["cross"], 2)
        self.circle_player_score_2 = self.player_score(symbol["circle"], 2)

        self.cross_player_score_3 = self.player_score(symbol["cross"], 3)
        self.circle_player_score_3 = self.player_score(symbol["circle"], 3)

        self.cross_player_situation = self.player_situation(symbol["cross"])
        self.circle_player_situation = self.player_situation(symbol["circle"])

        self.__player_turn_symbol = random.randint(1, 2)

    def console_display_board(self):
        for row in range(self.size):
            print(self.representation[row * self.size: row * self.size + self.size])

    
        print("player 1 score: ", self.cross_player_score)
        print("player 1 score_2: ", self.cross_player_score_2)
        print("player 1 score_3: ", self.cross_player_score_3)
        print("player 1 situation: ", self.cross_player_situation)

        print("player 2 score: ", self.circle_player_score)
        print("player 2 score_2: ", self.circle_player_score_2)
        print("player 2 score_3: ", self.circle_player_score_3)
        print("player 2 situation: ", self.circle_player_situation)

    def random_empty_space(self):
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - 1)

        while(self.representation[row * self.size + col] != str(symbol["blank"])):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

        return row, col
    
    def is_test_correct(self):
        return self.circle_player_score == self.player_score(symbol["circle"]) and self.circle_player_score_2 == self.player_score(symbol["circle"], 2) and self.circle_player_score_3 == self.player_score(symbol["circle"], 3) and self.cross_player_score == self.player_score(symbol["cross"]) and self.cross_player_score_2 == self.player_score(symbol["cross"], 2) and self.cross_player_score_3 == self.player_score(symbol["cross"], 3) #and self.player_situation(symbol["cross"]) == self.cross_player_situation and self.player_situation(symbol["circle"]) == self.circle_player_situation
    
    def fill_empty_cells(self, filling):
        list_representation = list(self.representation)
        for i in range(self.size):
            for j in range(self.size):
                list_representation[i * self.size + j] = filling if list_representation[i * self.size + j] == str(symbol["blank"]) else list_representation[i * self.size + j]
        
        self.representation = "".join(list_representation)
                
        

