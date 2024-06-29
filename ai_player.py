import numpy as np
from board import *

agent = {
        "human": 0,
        "AI": 1
    }

symbol = {
        "cross": 1,
        "circle": 2,
        "blank": 0,
        "max": 1,
        "min": 2
    }

def reverse(s):
    str = ""
    for i in s:
        str = i + str
    return str

DEPTH = 2

# find the next cell to check according to an order similar to C++
# pairs<int, int> type
def next_move(i, j, size):
    if i >= size - j - 1 and i < j:
        i += 1
    elif j > size - i - 1 and j <= i:
        j -= 1
    elif i >= j and j <= size - i - 1:
        i -= 1
    else:
        j += 1

    return [i, j]


class AI_player:
    # class att are:
    # self.symbol
    # self.table_counter
    def __init__(self, agent_symbol):
        self.symbol = agent_symbol
        self.table_counter = 0

    @property
    def symbol(self):
        return self.__symbol
    
    @symbol.setter
    def symbol(self, value):
        if value == symbol["circle"] or value == symbol["cross"]:
            self.__symbol = value

    #to know if the board is in a terminal state or not
    def terminal(self, board: Board):
        return board.is_board_full()
    
    def value(self,board: Board):
        return board.player_score(symbol["max"]) - board.player_score(symbol["min"])
    
    def playerTurn(self, board: Board):
        return board.player_turn_symbol
    
    def evaluation_function(self, board: Board):
        if board.representation in transposition_table:
            self.table_counter += 1
            return transposition_table[board.representation]
        
        reverse_representation = reverse(board.representation)
        if reverse_representation in transposition_table:
            self.table_counter += 1
            transposition_table[board.representation] = transposition_table[reverse_representation]
            return transposition_table[reverse_representation]
        
        evaluation = 0.5 * (board.player_situation(symbol["max"]) - board.player_situation(symbol["min"]))

        if(board.turn_number > 4 and board.turn_number <= board.size / 2 + board.size / 4):
            evaluation += 2*(board.player_score(symbol["max"], 2) - board.player_score(symbol["min"], 2))


        if(board.turn_number > 5 and board.turn_number <= board.size / 2 + board.size / 4):
            evaluation += 3*(board.player_score(symbol["max"], 3) - board.player_score(symbol["min"], 3))
        if(board.turn_number > 6):
            evaluation += 8 * self.value(board)

        transposition_table[board.representation] = evaluation
        return evaluation
    
    #debugged successfully
    def actions(self, board: Board):
        if board.is_board_full():
            return []
        
        board_possible_next_states = []
        board_copy = board.custom_copy()

        i = int(np.floor(board.size / 2) - (not board.size % 2))
        j = int(np.floor(board.size / 2) - (not board.size % 2) + (board.size + 1) % 2)
        while i != -1:
            if board_copy.set_cell(i, j):
                board_possible_next_states.append(board_copy)
                board_copy = board.custom_copy()

            l = next_move(i, j, board.size)
            i = l[0]; j = l[1]

        #remove this code
        for i in range(0, board_copy.size):
            for j in range(0, board_copy.size):
                if board_copy.set_cell(i, j):
                    board_possible_next_states.append(board_copy)
                    board_copy = board.custom_copy()


        return board_possible_next_states
    
    def minimax(self, board: Board, depth, alpha, beta, player_symbol):
        if depth == 0 or board.is_board_full():
            return self.evaluation_function(board)

        if player_symbol == symbol["max"]:
            possible_next_states = self.actions(board)
            max_evaluation = -np.inf
            for child in possible_next_states:
                if child.representation in transposition_table:
                    evaluation = transposition_table[child.representation]
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, evaluation)

                    if beta <= alpha:
                        break

                    continue

                reverse_representation = reverse(child.representation)
                if reverse_representation in transposition_table:
                    evaluation = transposition_table[reverse_representation]
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, evaluation)

                    if beta <= alpha:
                        break

                    continue

                evaluation = self.minimax(child, depth - 1, alpha, beta, symbol["min"])
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)

                if beta <= alpha:
                    break

            return max_evaluation

        elif player_symbol == symbol["min"]:
            possible_next_states = self.actions(board)
            min_evaluation = np.inf
            for child in possible_next_states:
                if child.representation in transposition_table:
                    evaluation = transposition_table[child.representation]
                    if(evaluation < min_evaluation):
                        min_evaluation = evaluation
                        beta = min(beta, evaluation)

                        if beta <= alpha:
                            break

                        continue

                    reverse_representation = reverse(child.representation)
                    if reverse_representation in transposition_table:
                        evaluation = transposition_table[reverse_representation]
                        if(evaluation < min_evaluation):
                            min_evaluation = evaluation
                            beta = min(beta, evaluation)

                        if beta <= alpha:
                            break

                        continue
                evaluation = self.minimax(child, depth - 1, alpha, beta, symbol["max"])
                transposition_table[child.representation] = evaluation

                if(evaluation < min_evaluation):
                    min_evaluation = evaluation

                beta = min(beta, evaluation)

                if beta <= alpha:
                    break

            return min_evaluation
            
    def next_move(self, board: Board):
        best_move = (-1, -1)
        copy_board = board.custom_copy()
        all_possible_actions = self.actions(copy_board)
        best_action = None

        if  len(all_possible_actions) == 0:
            print("no more moves can be taking here")
            return best_move
        
        if self.playerTurn(board) != board.player_turn_symbol:
            #print(f"it is not {list(symbol.values()).index(self.playerTurn)} turn yet")
            #print(f"it's {list(symbol.values()).index(board.player_turn_symbol)} turn")
            return best_move
        
        alpha = -np.inf
        beta = np.inf
        depth = DEPTH

        if self.symbol == symbol["max"]:
            possible_next_states = self.actions(copy_board)
            max_evaluation = -np.inf
            for child in possible_next_states:

                reverse_representation = reverse(child.representation)
                if reverse_representation in transposition_table:
                    evaluation = transposition_table[reverse_representation]

                    for row in range(copy_board.size):
                        for col in range(copy_board.size):
                            if copy_board.matrix[row][col] != child.matrix[row][col]:
                                best_move = (row, col)
                                break

                        if col != copy_board.size - 1:
                            break
                    
                    max_evaluation = max(max_evaluation, evaluation)
                    alpha = max(alpha, evaluation)

                    if beta <= alpha:
                        break

                    continue

                evaluation = self.minimax(child, depth, alpha, beta, symbol["min"])
                transposition_table[child.representation] = evaluation

                if(evaluation > max_evaluation):
                    best_action = child
                    max_evaluation = evaluation

                    for row in range(copy_board.size):
                        for col in range(copy_board.size):
                            if copy_board.matrix[row][col] != child.matrix[row][col]:
                                best_move = (row, col)
                                break

                        if col != copy_board.size - 1:
                            break

                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)

                if beta <= alpha:
                    break
                
            self.table_counter = 0
            return best_move
        
        elif self.symbol == symbol["min"]:
            possible_next_states = self.actions(copy_board)
            min_evaluation = np.inf
            for child in possible_next_states:

                reverse_representation = reverse(child.representation)
                if reverse_representation in transposition_table:
                    evaluation = transposition_table[reverse_representation]

                    for row in range(copy_board.size):
                        for col in range(copy_board.size):
                            if copy_board.matrix[row][col] != child.matrix[row][col]:
                                best_move = (row, col)
                                break

                        if col != copy_board.size - 1:
                            break
                    
                    min_evaluation = min(min_evaluation, evaluation)
                    beta = min(beta, evaluation)

                    if beta <= alpha:
                        break

                    continue
                evaluation = self.minimax(child, depth, alpha, beta, symbol["max"])
                
                if(evaluation < min_evaluation):
                    best_action = child
                    min_evaluation = evaluation

                    for row in range(copy_board.size):
                        for col in range(copy_board.size):
                            if copy_board.matrix[row][col] != child.matrix[row][col]:
                                best_move = (row, col)
                                break

                        if col != copy_board.size - 1:
                            break

                beta = min(beta, evaluation)

                if beta <= alpha:
                    break

            self.table_counter = 0
            return best_move
        


        


