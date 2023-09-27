# Mazeworld
In this assignemnt, I developing a pathfinding solution for a robot navigating ASCII-represented mazes, utilizing the provided Maze.py code. Emphasis is on implementing the A* search algorithm, with the option to also explore Uniform-Cost-Search. The challenge amplifies with multi-robot coordination in mazes, requiring collision avoidance and fuel-efficient pathfinding. Another variant introduces a blind robot adhering to Pacman physics, aware of only the North direction, demanding heuristic-driven solutions to guide it from an unknown start to a known end position. 

**Previous work**
   - The discussion should describe the problem attacked by the paper, give a quick summary of the main result(s), and discuss the basic approach of the paper. 

**A-star search**

`A* search` is a generalization of `Uniform-Cost-Search (UCS)`. In UCS, we expand the node with the lowest path cost so far. In A* search, we expand the node with the lowest value of `g(n)+h(n)`, where `g(n)` is the cost from the start node to node n, and `h(n)` is the heuristic estimate of the cost from node n to the goal.

   - ##### Uniform-Cost-Search first.
      For UCS, I simply make the heuristic `h(n)` turn 0 so that the A* only has g(n) for the cost function. This would mean that the node's priority would be solely determined by its cost `g(n)`, making it a UCS. You can find the `null_heuristic()` in `test_mazeworld.py`
      
   - ##### How do you efficiently check if a node is in a priority queue, or replace it efficiently?

**Multi-robot coordination**

   - k robots live in an n x n rectangular maze. The coordinates of each robot are (x_i, y_i), and each coordinate is an integer in the range 0…n-1. For example, maybe the maze looks like this:  

      #######. #  
      #. . . # . . . #  
      #. #. #. ###  
      #. . . . . . . #  
      #. #####. #  
      #BC . . . . .  #  
      #A#######     

      That’s three robots A, B, C in a 6x9 maze. I’d like to get the robots to this locations:  
      
      #######A#  
      #. . . # . CB#  
      #. #. #. ###  
      #. . . . . . . #  
      #. #####.#  
      #. . . . . . .  #  
      #.#######    

   - ##### Describe how my multi-robot coordintion works (mention 5 states)
   - ##### Bonus: Have the robots move simultaneously
   - #### If there are not many walls, n is large (say 100x100), and several robots (say 10), do you expect a straightforwards breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?
   - ##### Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.
   - ##### give five cool examples from 5x5 to 40x40, describe why they are interesting
   - #### Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?
   - #### The state space of the 8-puzzle is made of two disjoint sets. Describe how you would modify your program to prove this.

**Blind robot with Pacman physics**
   - ##### describe how my sensorless robot works
   - ##### Describe what heuristic you used for the A* search. Is the heuristic optimistic? Are there other heuristics you might use? (An excellent might compare a few different heuristics for effectiveness and make an argument about optimality.)
   - #### examples (animation)

**Bonus: polynomial-time blind robot planning**
   - Prove that a sensorless plan of the type you found above always exists, as long as the size of the maze is finite and the goal is in the same connected component of the maze as the start.  
   Now describe (but do not implement) a motion planner that runs in time that is linear or polynomial in the number of cells in the maze. (Notice that the size of the belief space is exponential in the number of cells, so this would be a very interesting result!)


**Tests**

   - I've set up a testing section to create FoxProblem instances with varying starting states. Then, I run BFS, DFS, IDS, and memoizing DFS on these instances to test their functionality.
   - In my test case on a large graph, IDS does took way longer than BFS.
   test case:
      >`print(bfs_search(problemXL))`  
      >`print(dfs_search(problemXL))`  
      >`print(ids_search(problemXL))`  
      >`print(memoizing_dfs_search(problemXL))`