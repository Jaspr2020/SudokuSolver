def string_to_board(input_string):
    """
    Takes the passed input string and converts it into a 2D list
    """

    # Create board
    board = [[0 for i in range(9)] for j in range(9)]

    for row in range(9):
        for col in range(9):
            # Convert character to integer ('.' becomes 0)
            board[row][col] = 0 if input_string[row * 9 + col] == '.' else int(input_string[row * 9 + col])

    return board


def print_board(board):
    """
    Prints a readable version of the game board
    """

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
    """
    Returns a list of values which are not restricted by spaces in the same row, column, or square
    """

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

def empty_spaces(board):
    """
    Returns a list positions of the spaces with a value of zero
    """

    possible_spaces = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                possible_spaces.append((row, col))
    return possible_spaces

def num_constraints_caused(position, board):
    """
    Returns the number of undetermined variables effected by the passed position
    """

    constraints_caused = 0

    # Check row, ignoring values in square
    for i in range(9):
        if int(i / 3) != int(position[1] / 3) and board[position[0]][i] == 0:
            constraints_caused += 1
    # Check column, ignoring values in square
    for i in range(9):
        if int(i / 3) != int(position[0] / 3) and board[i][position[1]] == 0:
            constraints_caused += 1
    # Check square, ignoring position
    square_x = int(position[1] / 3) * 3
    square_y = int(position[0] / 3) * 3
    for i in range(square_y, square_y + 3):
        for j in range(square_x, square_x + 3):
            if (i, j) != position and board[i][j] == 0:
                constraints_caused += 1

    return constraints_caused

def num_constraints_caused_by_value(value, position, board):
    """
    Returns the number of constraints caused by setting the passed position to the passed value
    """

    starting = board[position[0]][position[1]]
    board[position[0]][position[1]] = value
    constraints_caused = num_constraints_caused(position, board)
    board[position[0]][position[1]] = starting
    return constraints_caused

def most_restricted_spaces(board):
    """
    Returns the list of most constrained variables
    """

    # List of empty spaces
    possible_spaces = empty_spaces(board)

    if len(possible_spaces) == 0:
        return None

    # Store list of variables
    most_constrained = [possible_spaces[0]]
    for space in possible_spaces:
        # Equally constrained -> Add to list
        if len(possible_values(space, board)) == len(possible_values(most_constrained[0], board)):
            most_constrained.append(space)
        # More constrained -> New list
        elif len(possible_values(space, board)) < len(possible_values(most_constrained[0], board)):
            most_constrained.clear()
            most_constrained.append(space)

    return most_constrained

def most_restricting_space(variable_list, board):
    """
    Returns the most constraining variable from variable_list
    """

    if variable_list == None:
        return None

    # Find variable causing the most constraints
    most_constraining = variable_list[0]
    constraints_caused = num_constraints_caused(most_constraining, board)
    
    for space in variable_list:
        space_constraints_caused = num_constraints_caused(space, board)
        if space_constraints_caused < constraints_caused:
            most_constraining = space
            constraints_caused = space_constraints_caused

    return most_constraining

def next_space(board):
    """
    Return the next space to check using MCV
    """

    # List of Most Constrained Variable (MCV)
    spaces = most_restricted_spaces(board)
    # Most Constraining Variable from list
    return most_restricting_space(spaces, board)

def values_to_try(position, board):
    """
    Returns a list of values ordered by LCV
    """

    values = possible_values(position, board)
    # Sorts list from least constraints caused to most constraints caused
    ordered_values = sorted(values, key = lambda n: num_constraints_caused_by_value(n, position, board))
    return ordered_values

def check_arc_consistency(board):
    """
    Returns true if all unassigned variables have at least one non-constrained value in their domain
    """
    
    # List of empty spaces
    possible_spaces = empty_spaces(board)

    for space in possible_spaces:
        # Space has no possible values
        if len(possible_values(space, board)) == 0:
            return False

    return True

def solve(board):
    """
    Solves the passed board
    """

    # Position of the next variable to set (using MCV)
    best_position = next_space(board)

    # Solution found
    if best_position == None:
        return True

    # Try all possible at position, sorted by LCV
    for n in values_to_try(best_position, board):
        # Set the move
        board[best_position[0]][best_position[1]] = n

        if not check_arc_consistency(board):
            # Undo the move
            board[best_position[0]][best_position[1]] = 0
            continue

        # Search for solution recursively
        solved = solve(board)
        # Solution is found
        if solved:
            return True

        # Undo the move
        board[best_position[0]][best_position[1]] = 0

    # No solution found
    return False

def main():
    # test_string_1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    # test_string_2 = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."
    input_string = input("Enter an unsolved Sudoku Grid: ")
    board = string_to_board(input_string)
    solve(board)
    print_board(board)

if __name__ == "__main__":
    main()