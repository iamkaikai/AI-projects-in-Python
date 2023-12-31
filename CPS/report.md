# Constraint satisfaction

In the quest to solve Constraint Satisfaction Problems (CSPs) efficiently, this report elaborates on the incorporation of heuristics and inference techniques into a simple backtracking solver. Initially, the solver was applied to the map-coloring problem, which was modeled as a CSP. Subsequently, the solver's versatility was tested on a circuit-board layout problem without requiring additional backtracking code. Heuristics such as Minimum Remaining Values (MRV) and Least Constraining Value (LCV), along with an inference technique (AC-3), were integrated, offering toggle-able settings for ease of comparison and debugging.

**Backtracking Solver Implementation:**

   In my implementation of the backtracking algorithm for solving Constraint Satisfaction Problems (CSPs), I've structured the algorithm in a recursive manner to efficiently traverse through the search space of possible solutions. The core of this algorithm resides in the `back_tracking` method of my `backTracking` class. I've organized this class to accept arguments during initialization which act as switches for various heuristics, although for the moment, let’s focus on the fundamental backtracking process.

   1. **Initialization**:
      - When an instance of the `backTracking` class is created, I have the option to specify whether or not to use certain heuristics by passing arguments to the `__init__` method. This design allows for easy toggling of heuristic strategies.

   2. **Recursion**:
      - The recursive nature of my algorithm is embodied in the `back_tracking` method. This method takes two arguments: `assignment`, which is a dictionary representing the current assignment of values to variables, and `csp`, which is an object encapsulating the constraint satisfaction problem to be solved.

   3. **Base Case**:
      - The recursion employs a base case to determine when a solution has been found. This is achieved by the `is_complete` method, which checks if all variables have been assigned a value. If so, the current assignment is returned as the solution.

   4. **Variable Selection**:
      - If the base case hasn’t been reached, my algorithm proceeds to select an unassigned variable from the CSP. This is done using the `get_unassigned_variables` method, which simply iterates through the variables and returns the first unassigned one it encounters.

   5. **Domain Iteration**:
      - Having selected an unassigned variable, my algorithm then iterates through the possible values in the domain of that variable. This is straightforward as the domain values are accessed from the `csp` object.

   6. **Consistency Check**:
      - For each value in the domain, a consistency check is performed using the `is_consistent` method to ensure that the current value assignment does not violate any constraints. If the assignment is consistent, it's added to the `assignment` dictionary.

   7. **Recursive Call**:
      - With a consistent value assignment, a recursive call to `back_tracking` is made with the updated `assignment`. This dives deeper into the search tree, seeking a solution.

   8. **Backtrack**:
      - If a point is reached where a consistent assignment cannot be found for a particular variable, the algorithm backtracks by removing the current variable from the `assignment` and tries a different value for the previously assigned variable. This is the essence of backtracking, providing a systematic way to explore different value assignments.

   9. **No Solution Found**:
      - If the search exhausts all possibilities without finding a solution, a `'Solution not found!'` message is returned. This occurs when the algorithm has traversed the entire search space without encountering a complete and consistent assignment.

   This structured and recursive approach enables an orderly exploration of the solution space, while also allowing for easy integration of additional heuristics to further optimize the search process.


----

**Modeling Problems as CSPs**

- Map Coloring Problem    
In the map coloring problem, I've structured the CSP as follows:

    1. **Variables**:
        - The regions that need to be colored like 'WA', 'NT', 'SA', etc., are represented as a list of variables.

    2. **Domains**:
        - The domain for each region is a list of colors `['R', 'G', 'B']` representing the possible colors a region can take.

    3. **Constraints**:
        - The constraints ensure that neighboring regions do not share the same color. They are generated by iterating over all color combinations and filtering out the conflicting ones.
    4. **Neighbors**:
        - I've utilized a `Graph` class to represent the neighboring relations between regions. In this graph, each node represents a region, and edges represent neighboring relations.
        - The `get_neighbors` method is used to fetch the neighbors of a given region from the graph structure.

- Circuit Board Problem:  
  In the circuit board problem, the CSP is structured in the following manner:

    1. **Variables**:
       - The components to be placed on the board are represented as a set of variables, with each variable corresponding to a component ID.

    2. **Domains**:
       - The domain for each component is generated using the `generate_domain` method. It's a list of positions `(x,y)` the component could occupy on the board without going out of bounds.

    3. **Constraints**:
       - In the `generate_constraints` method, I iterate through all pairs of components, skipping comparisons of a component with itself. For each pair, a key is created using their IDs in the `constraints` dictionary. I then iterate through all possible positions for both components, calculating the end coordinates by adding their width and height to the start coordinates. To check for overlapping, I use four comparisons: checking if the end x-coordinate of the current component is less than or equal to the start x-coordinate of the other component, and similarly for the other three sides. If any of these conditions are true, it indicates no overlap, so I append the positions as a tuple to a list of legal positions. After examining all positions, I update the `constraints` dictionary with the legal positions list for the current pair of components. This process repeats for all pairs, ensuring only non-overlapping positions are considered legal, and the filled `constraints` dictionary is returned.

    4. **Neighbors**:
       - The neighboring relations between components are generated using the `generate_neighbors` and `get_neighbors` methods. These methods build a dictionary mapping each component to a list of other components it shares a constraint with.

    5. **Display**:
       - A `display` method is included to visualize the solution by creating a canvas and filling it based on the component positions in the solution.


    By breaking down the problem into these structured sections, I've created a clear framework within which the backtracking algorithm can operate to find solutions.

----

**Inference Technique Integration:**

In my implementation, I created a separate class named `AC3` to handle the AC-3 algorithm, which is an algorithm used for reducing the domain of variables in a CSP based on arc-consistency. The `AC3` class is initialized with a CSP object, and it takes the `constraints`, `domains`, and `neighbors` function from the CSP object to work with.

- The `need_modification` method in the `AC3` class is used to check if the domain of a variable `xi` needs modification concerning another variable `xj`. This is done by iterating through all values in the domain of `xi`, and for each value, it checks whether there's a satisfying value in the domain of `xj` based on the constraints. If no such satisfying value is found, the value from the domain of `xi` is removed, and the method returns `True` indicating a modification was made.

- The `inference` method is the core of the AC-3 algorithm. It initializes a queue with all the keys from the constraints dictionary. While the queue is not empty, it pops a pair of variables (`xi`, `xj`), and checks if a modification is needed using the `need_modification` method. If a modification is made and the domain of `xi` becomes empty, it immediately returns `False` as the CSP is not solvable. Otherwise, it adds the neighbors of `xi` (excluding `xj` to avoid infinite loops) back to the queue for further checking. The method returns `True` if the entire queue is processed without finding an unsolvable condition.

- Now, integrating AC-3 into the backtracking algorithm is done in the `back_tracking` method of the `backTracking` class. I included an `ac3` argument in the `__init__` method of the `backTracking` class to serve as a switch for activating AC-3. In the `back_tracking` method, I check if the `ac3` argument is set. If it is, an `AC3` object is created with the CSP, and the `inference` method of the `AC3` object is called. If `inference` returns `False`, it immediately returns 'Solution not found!' as the CSP is unsolvable with the current domains. Otherwise, it proceeds with the normal backtracking process. This integration helps in pruning the search space before the actual backtracking begins, potentially speeding up the search for a solution.

----

**Heuristic Integration:**  
In the implementation, I included the MRV (Minimum Remaining Values) and LCV (Least Constraining Value) heuristics as options to optimize the backtracking algorithm for solving constraint satisfaction problems. When initiating the `backTracking` class, I provided arguments for MRV and LCV as switches to toggle their usage. 

- #### Minimum Remaining Values  
    For MRV, when activated, within the method to fetch unassigned variables, I adjusted the logic to select the variable with the `smallest domain`, implying fewer remaining values. This heuristic operates on the premise that tackling variables with fewer choices first can potentially prune the search space more effectively.

- #### Least Constraining Value 
    On the other hand, for LCV, when activated, within the core backtracking method, I modified the logic to sort the `domain values` of the current variable. The sorting is done based on the count of constraints each value imposes on neighboring variables. The idea is to prioritize values that are least constraining to others, hoping to leave more room for subsequent variable assignments and thereby reduce the likelihood of encountering conflicts.

- #### Integration
    The integration of MRV and LCV into the backtracking process is seamless and is controlled by the arguments passed when creating an instance of the `backTracking` class. This design allows for a flexible approach where one can easily toggle the heuristics on or off to observe how they impact the efficiency of the algorithm in finding solutions.

----

**Performance Evaluation:**

- #### Coloring Map Problem
    In evaluating the solver's performance, different configurations were tested. For the map coloring problem, due to its simpler nature, only one trial was conducted for each configuration. The results reflected a substantial decrease in runtime when heuristics and AC-3 were applied, showcasing their effectiveness in solving such a straightforward problem quickly.


```
Solution:
{'WA': 'R', 'NT': 'R', 'SA': 'R', 'Q': 'R', 'NSW': 'R', 'V': 'R', 'T': 'R'}

Time in average:
backtracking in 1000 trials = 7.59124755859e-07  
backtracking + AC3 in 1000 trials = 1.41596794e-05  
backtracking + MRV in 1000 trials = 2.26593017e-06  
backtracking + LCV in 1000 trials = 1.42264366e-06  
backtracking + MRV + LCV in 1000 trials = 1.02233886e-06  
backtracking + MRV + LCV + AC3 in 1000 trials = 1.79295539e-05  

```
  
The results reveal that while MRV, LCV, and their combination can provide some level of optimization, the AC3 algorithm, in this case, led to a higher average runtime. This suggests that for simpler problems like map coloring, plain backtracking or backtracking with MRV and LCV heuristics might be more efficient. However, AC3, which is designed to reduce the domain sizes before the search, could introduce an overhead that outweighs its benefits in simpler problems. Hence, the choice of heuristics and algorithms should be tailored to the complexity and nature of the specific problem at hand.

- #### Circuitboard Problem
    On the other hand, the circuit board problem posed a more complex challenge. To account for the inherent depth-first search (DFS) nature of backtracking, which could potentially stumble upon a solution faster in some trials due to luck, a more robust evaluation was carried out over 100 trials for each configuration. This approach aimed to mitigate the luck factor and provide a more accurate measure of each configuration's performance.

```
Solution:
{'🔷': (0, 0), '🟢': (0, 3), '🟩': (3, 3), '🟦': (4, 0), '🔶': (0, 6), '🟪': (9, 0), '🟧': (4, 1), '🟠': (3, 9), '🟥': (0, 8), '🟫': (7, 7), '🟨': (7, 3)}

🟥🟥🟥🟠🟠🟠⬛️🟫🟫🟫
🟥🟥🟥🟩🟩🟩🟩🟫🟫🟫
🔶🔶🔶🟩🟩🟩🟩🟫🟫🟫
🔶🔶🔶🟩🟩🟩🟩🟨🟨🟪
🟢🟢🟢🟩🟩🟩🟩🟨🟨🟪
🟢🟢🟢🟩🟩🟩🟩🟨🟨🟪
🟢🟢🟢🟩🟩🟩🟩🟨🟨🟪
🔷🔷🔷🔷🟧🟧🟧🟧🟧🟪
🔷🔷🔷🔷🟧🟧🟧🟧🟧🟪
🔷🔷🔷🔷🟦🟦🟦🟦🟦🟪

Time in average:
backtracking in 100 trials = 0.62137263
backtracking + MRV in 100 trials = 0.31068737
backtracking + LCV in 100 trials = 0.20712552
backtracking + MRV + LCV in 100 trials = 0.15534457
backtracking + MRV + LCV + AC3 in 100 trials = 0.34677909

```

These evaluations provided valuable insights into the performance enhancements brought about by the heuristics and AC-3. The significant reduction in average runtime across configurations, especially in the more complex circuit board problem, demonstrated the effectiveness of these enhancements in optimizing the backtracking process. This exercise was crucial in understanding how to effectively integrate these heuristics and the AC-3 algorithm to optimize the solver for handling different complexities in constraint satisfaction problems.

----

**Conclusion:**

The exploration into enhancing a backtracking solver with heuristics and AC-3 for Constraint Satisfaction Problems yielded insightful takeaways. On applying these enhancements to a map-coloring problem, I noticed that while MRV and LCV heuristics optimized the search, AC-3 increased the average runtime, suggesting a possible overhead for simpler problems. However, in a more complex circuit-board problem, these heuristics, particularly when combined, significantly reduced the average runtime, displaying their effectiveness in optimizing the solver. This exercise illustrated the importance of tailoring the choice of heuristics and inference techniques to the problem's complexity, providing a solid groundwork for further optimization in solving Constraint Satisfaction Problems.






