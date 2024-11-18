"""
Each futoshiki board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8

Empty values in the board are represented by 0

An * after the letter indicates the inequality between the row represented
by the letter and the next row.
e.g. my_board['A*1'] = '<' 
means the value at A1 must be less than the value
at B1

Similarly, an * after the number indicates the inequality between the
column represented by the number and the next column.
e.g. my_board['A1*'] = '>' 
means the value at A1 is greater than the value
at A2

Empty inequalities in the board are represented as '-'

"""
import sys

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#
import numpy as np
import copy
import time
#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

ROW = "ABCDEFGHI"
COL = "123456789"

class Board:
    '''
    Class to represent a board, including its configuration, dimensions, and domains
    '''
    
    def get_board_dim(self, str_len):
        '''
        Returns the side length of the board given a particular input string length
        '''
        d = 4 + 12 * str_len
        n = (2+np.sqrt(4+12*str_len))/6
        if (int(n) != n):
            raise Exception("Invalid configuration string length")

        
        return int(n)
        
    def get_config_str(self):
        '''
        Returns the configuration string
        '''
        return self.config_str
        
    def get_config(self):
        '''
        Returns the configuration dictionary
        '''
        return self.config
        
    def get_variables(self):
        '''
        Returns a list containing the names of all variables in the futoshiki board
        '''
        variables = []
        for i in range(0, self.n):
            for j in range(0, self.n):
                variables.append(ROW[i] + COL[j])
        return variables
    
    def convert_string_to_dict(self, config_string):
        '''
        Parses an input configuration string, retuns a dictionary to represent the board configuration
        as described above
        '''
        config_dict = {}
        
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_string[0]
                config_string = config_string[1:]
                
                config_dict[ROW[i] + COL[j]] = int(cur)
                
                if(j != self.n - 1):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + COL[j] + '*'] = cur
                    
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_string[0]
                    config_string = config_string[1:]
                    config_dict[ROW[i] + '*' + COL[j]] = cur
                    
        return config_dict
        
    def print_board(self):
        '''
        Prints the current board to stdout
        '''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    print('_', end=' ')
                else:
                    print(str(cur), end=' ')
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        print(' ', end=' ')
                    else:
                        print(cur, end=' ')
            print('')
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        print(' ', end='   ')
                    else:
                        print(cur, end='   ')
            print('')
        
    def __init__(self, config_string):
        '''
        Initialising the board
        '''
        self.config_str = config_string
        self.n = self.get_board_dim(len(config_string))
        if(self.n > 9):
            raise Exception("Board too big")
            
        self.config = self.convert_string_to_dict(config_string)
        self.domains = self.reset_domains()
        
        self.forward_checking(self.get_variables())
        
        
    def __str__(self):
        '''
        Returns a string displaying the board in a visual format. Same format as print_board()
        '''
        output = ''
        config_dict = self.config
        for i in range(0, self.n):
            for j in range(0, self.n):
                cur = config_dict[ROW[i] + COL[j]]
                if(cur == 0):
                    output += '_ '
                else:
                    output += str(cur)+ ' '
                
                if(j != self.n - 1):
                    cur = config_dict[ROW[i] + COL[j] + '*']
                    if(cur == '-'):
                        output += '  '
                    else:
                        output += cur + ' '
            output += '\n'
            if(i != self.n - 1):
                for j in range(0, self.n):
                    cur = config_dict[ROW[i] + '*' + COL[j]]
                    if(cur == '-'):
                        output += '    '
                    else:
                        output += cur + '   '
            output += '\n'
        return output
    
        
    def reset_domains(self):
        '''
        Resets the domains of the board assuming no enforcement of constraints
        '''
        domains = {}
        variables = self.get_variables()
        for var in variables:
            if(self.config[var] == 0):
                domains[var] = [i for i in range(1,self.n+1)]
            else:
                domains[var] = [self.config[var]]
                
        self.domains = domains
                
        return domains


    def generate_config_str(self):
        '''
        Generates the configuration string from the current board configuration (self.config)
        '''
        config_str = ''
        for i in range(self.n):
            for j in range(self.n):
                var = ROW[i] + COL[j]
                config_str += str(self.config[var])
                if j != self.n - 1:
                    key = var + '*'
                    config_str += self.config.get(key, '-')
            if i != self.n - 1:
                for j in range(self.n):
                    key = ROW[i] + '*' + COL[j]
                    config_str += self.config.get(key, '-')
        return config_str
    
    def apply_inequality(self, var1, var2, inequality):
        '''
        Enforces the inequality between var1 and var2.
        Returns False if inconsistency is found.
        '''
        domain1 = self.domains[var1]
        domain2 = self.domains[var2]

        new_domain1 = []
        new_domain2 = []

        for v1 in domain1:
            possible = False
            for v2 in domain2:
                if inequality == '>':
                    if v1 > v2:
                        possible = True
                elif inequality == '<':
                    if v1 < v2:
                        possible = True
                if possible:
                    break
            if possible:
                new_domain1.append(v1)

        for v2 in domain2:
            possible = False
            for v1 in domain1:
                if inequality == '>':
                    if v1 > v2:
                        possible = True
                elif inequality == '<':
                    if v1 < v2:
                        possible = True
                if possible:
                    break
            if possible:
                new_domain2.append(v2)

        if not new_domain1 or not new_domain2:
            return False

        self.domains[var1] = new_domain1
        self.domains[var2] = new_domain2

        return True


        
    def forward_checking(self, reassigned_variables):
        '''
        Runs the forward checking algorithm to restrict the domains of all variables based on the values
        of reassigned variables.
        '''
        queue = reassigned_variables.copy()

        while queue:
            var = queue.pop(0)
            value = self.config[var]
            row, col = var[0], var[1]

            # remove assigned value from peers in the same row and column
            for c in COL[:self.n]:
                neighbor = row + c
                if neighbor != var and value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    if not self.domains[neighbor]:
                        return False
                    if len(self.domains[neighbor]) == 1 and neighbor not in queue:
                        self.config[neighbor] = self.domains[neighbor][0]
                        queue.append(neighbor)

            for r in ROW[:self.n]:
                neighbor = r + col
                if neighbor != var and value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    if not self.domains[neighbor]:
                        return False
                    if len(self.domains[neighbor]) == 1 and neighbor not in queue:
                        self.config[neighbor] = self.domains[neighbor][0]
                        queue.append(neighbor)

            # apply inequalities involving var
            inequalities = []

            # right neighbor
            inequality_key = var + '*'
            if inequality_key in self.config and self.config[inequality_key] != '-':
                inequality = self.config[inequality_key]
                neighbor_col_index = COL.index(col) + 1
                if neighbor_col_index < self.n:
                    neighbor_col = COL[neighbor_col_index]
                    neighbor = row + neighbor_col
                    inequalities.append((var, neighbor, inequality))

            # left neighbor
            if col != COL[0]:
                left_col_index = COL.index(col) - 1
                left_col = COL[left_col_index]
                neighbor = row + left_col
                inequality_key = neighbor + '*'
                if inequality_key in self.config and self.config[inequality_key] != '-':
                    inequality = self.config[inequality_key]
                    inequalities.append((neighbor, var, inequality))

            # down neighbor
            inequality_key = row + '*' + col
            if inequality_key in self.config and self.config[inequality_key] != '-':
                inequality = self.config[inequality_key]
                neighbor_row_index = ROW.index(row) + 1
                if neighbor_row_index < self.n:
                    neighbor_row = ROW[neighbor_row_index]
                    neighbor = neighbor_row + col
                    inequalities.append((var, neighbor, inequality))

            # up neighbor
            if row != ROW[0]:
                upper_row_index = ROW.index(row) - 1
                upper_row = ROW[upper_row_index]
                neighbor = upper_row + col
                inequality_key = upper_row + '*' + col
                if inequality_key in self.config and self.config[inequality_key] != '-':
                    inequality = self.config[inequality_key]
                    inequalities.append((neighbor, var, inequality))

            # apply inequalities
            for (v1, v2, inequality) in inequalities:
                if not self.apply_inequality(v1, v2, inequality):
                    return False
                else:
                    # if domains reduced to singleton, add to queue
                    if len(self.domains[v1]) == 1 and self.config[v1] == 0:
                        self.config[v1] = self.domains[v1][0]
                        queue.append(v1)
                    if len(self.domains[v2]) == 1 and self.config[v2] == 0:
                        self.config[v2] = self.domains[v2][0]
                        queue.append(v2)

        return True
        #=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
        
    #=================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the Board Class #*#*#*#
	#=================================================================================#
        
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#        

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

def backtracking(board):
    '''
    Performs the backtracking algorithm to solve the board
    Returns only a solved board
    '''
    # base case: if all variables have a domain size of 1
    if all(len(board.domains[var]) == 1 for var in board.get_variables()):
        for var in board.get_variables():
            board.config[var] = board.domains[var][0]

        # update config_str to reflect solved board
        board.config_str = board.generate_config_str()
        return board

    # get the variable with the smallest domain size
    var = min([v for v in board.get_variables() if len(board.domains[v]) > 1], key=lambda v: len(board.domains[v]))
    # print(f"Trying to assign a value to {var} with domain {board.domains[var]}")

    # try each value in the variable's domain
    for value in board.domains[var]:
        # print(f"Trying value {value} for variable {var}")
        new_board = copy.deepcopy(board)
        new_board.config[var] = value
        new_board.domains[var] = [value]
        
        if new_board.forward_checking([var]):
            result = backtracking(new_board)
            if result:
                return result
    
    # print(f"Backtracking failed for variable {var}")
    return None

    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#
    
def solve_board(board):
    '''
    Runs the backtrack helper and times its performance.
    Returns the solved board and the runtime
    '''
    #================================================================#
	#*#*#*# TODO: Call your backtracking algorithm and time it #*#*#*#
	#================================================================#

    start_time = time.time()
    solved_board = backtracking(board)
    end_time = time.time()
    runtime = end_time - start_time
    return solved_board, runtime
    
    #=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

def print_stats(runtimes):
    '''
    Prints a statistical summary of the runtimes of all the boards
    '''
    min = 100000000000
    max = 0
    sum = 0
    n = len(runtimes)

    for runtime in runtimes:
        sum += runtime
        if(runtime < min):
            min = runtime
        if(runtime > max):
            max = runtime

    mean = sum/n

    sum_diff_squared = 0

    for runtime in runtimes:
        sum_diff_squared += (runtime-mean)*(runtime-mean)

    std_dev = np.sqrt(sum_diff_squared/n)

    print("\nRuntime Statistics:")
    print("Number of Boards = {:d}".format(n))
    print("Min Runtime = {:.8f}".format(min))
    print("Max Runtime = {:.8f}".format(max))
    print("Mean Runtime = {:.8f}".format(mean))
    print("Standard Deviation of Runtime = {:.8f}".format(std_dev))
    print("Total Runtime = {:.8f}".format(sum))


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running futoshiki solver with one board $python3 futoshiki.py <input_string>.
        print("\nInput String:")
        print(sys.argv[1])
        
        print("\nFormatted Input Board:")
        board = Board(sys.argv[1])
        board.print_board()
        
        solved_board, runtime = solve_board(board)
        
        print("\nSolved String:")
        print(solved_board.get_config_str())
        
        print("\nFormatted Solved Board:")
        solved_board.print_board()
        
        print_stats([runtime])

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board.get_config_str())
        outfile.write('\n')
        outfile.close()

    else:
        # Running futoshiki solver for boards in futoshiki_start.txt $python3 futoshiki.py

        #  Read boards from source.
        src_filename = 'futoshiki_start.txt'
        try:
            srcfile = open(src_filename, "r")
            futoshiki_list = srcfile.read()
            srcfile.close()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        
        runtimes = []

        # Solve each board using backtracking
        for line in futoshiki_list.split("\n"):
            
            print("\nInput String:")
            print(line)
            
            print("\nFormatted Input Board:")
            board = Board(line)
            board.print_board()
            
            solved_board, runtime = solve_board(board)
            runtimes.append(runtime)
            
            print("\nSolved String:")
            print(solved_board.get_config_str())
            
            print("\nFormatted Solved Board:")
            solved_board.print_board()

            # Write board to file
            outfile.write(solved_board.get_config_str())
            outfile.write('\n')

        # Timing Runs
        print_stats(runtimes)
        
        outfile.close()
        print("\nFinished all boards in file.\n")
