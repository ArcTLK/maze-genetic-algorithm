# Application of Genetic Algorithm in solving a 2D Maze

## Dependencies
1. wxPython
2. numpy (Optional)
3. numba (Optional)

## File Information
### maze.py
It contains the actual maze game on which the genetic algorithm is being applied on.

### maze_gui.py
It contains a GUI implementation of the maze game using wxPython. Running this script allows you to play the game using the "WASD" arrow keys.

### cli.py
Pass a set of moves to this script as an argument to get a visual representation of how those moves are executed against the maze. It uses the maze_gui.py file to do so.

### utils.py
It contains some utility functions.

### ga.py
It contains the genetic algorithm implementation using vanilla python. It lacks optimization but does work! Running the script starts the genetic algorithm from a random population sample, outputting the best 3 chromosomes for every generation.

### np_ga.py
It is an incomplete attempt at using numpy to optimize the genetic algorithm.