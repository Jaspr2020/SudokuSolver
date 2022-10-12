def input_to_board(input_string):
    # Create board
    board = [[0 for i in range(9)] for j in range(9)]
    # For every row and column in the board
    for row in range(9):
        for col in range(9):
            # Set the value at (row, col) to the value of the input string as a number
            board[row][col] = 0 if input_string[row * 9 + col] == '.' else int(input_string[row * 9 + col])
    return board
        
    
def print_board(board):
    # Output string
    output = ""
    # For every row and column in the board
    for row in range(9):
        # Add a spacing line every 3 rows
        if row != 0 and row % 3 == 0:
            output += "---------------------\n"
        for col in range(9):
            # Add spaces between numbers and vertical bars between every 3 numbers
            if col != 0:
                output += " "
                if col % 3 == 0:
                    output += "| "
            output +=  str(board[row][col])
        output += "\n"
    print(output)

# input_string = input("Enter an unsolved Sudoku Grid: ")
input_string = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
board = input_to_board(input_string)
print_board(board)