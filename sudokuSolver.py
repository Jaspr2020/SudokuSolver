def string_to_board(input_string):
    # Create board
    board = [[0 for i in range(9)] for j in range(9)]

    for row in range(9):
        for col in range(9):
            # Convert character to integer ('.' becomes 0)
            board[row][col] = 0 if input_string[row * 9 + col] == '.' else int(input_string[row * 9 + col])
            
    return board


def print_board(board):
    output = ""
    
    for row in range(9):
        # Horrizontal line every 3 rows
        if row != 0 and row % 3 == 0:
            output += "---------------------\n"
        for col in range(9):
            # Vertical bars between every 3rd column
            if col != 0 and col % 3 == 0:
                output += "| "
            # Value at index
            output += str(board[row][col]) + " "
        if row != 8:
            output += "\n"
        
    print(output)
    
def possible_values(position, board):
    # Return empty list if the value is known
    if board[position[0]][position[1]] != 0:
        return []
    
    # List of possible values
    values = [i for i in range(1, 10)]
    
    # Check row for invalid values
    for i in range(9):
        if board[position[0]][i] in values and i != position[1]:
            values.remove(board[position[0]][i])
            
    # Check column for invalid values
    for i in range(9):
        if board[i][position[1]] in values and i != position[0]:
            values.remove(board[i][position[1]])
            
    # Check square for invalid values
    square_x = int(position[1] / 3) * 3
    square_y = int(position[0] / 3) * 3
    for i in range(square_y, square_y + 3):
        for j in range(square_x, square_x + 3):
            if board[i][j] in values and (i, j) != position:
                values.remove(board[i][j])
                
    # Return the list of remaining values
    return values

def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    # If there are no unsolved spaces
    return None

def solve(board):
    # Get the row and column of the next value to set
    position = find_empty(board)
    
    # Solution found
    if not position:
        return True
    
    # Try all possible at position
    for n in possible_values(position, board):
        board[position[0]][position[1]] = n
        
        # If solved, stop searching for solutions
        if solve(board) == True:
            return True
        
        # Undo the move
        board[position[0]][position[1]] = 0
    
    # No solution found
    return False

def main():
    input_string = input("Enter an unsolved Sudoku Grid: ")
    board = string_to_board(input_string)
    solve(board)
    print_board(board)
    
if __name__ == "__main__":
    main()