Alright, let's break down the instructions for your report step by step:

1. **Initial discussion and introduction**
   - Calculate and describe an upper bound on the number of states without considering legality. 
   - Create a graph of states using a drawing program. 
   
2. **Code design**
   - Understand the provided code.
   - Think about your own approach to the problem.
   
3. **Building the model**
   - Use FoxProblem.py as the starting point.
   - Represent key information about the problem.
   - Implement the starting state, a get_successors method, a goal_test, and other required methods.
   
4. **Breadth-first search (BFS)**
   - Implement BFS in uninformed_search.py.
   - Implement backchaining to extract the path from the graph.
   - Test BFS.
   - Use foxes.py for testing.
   
5. **Memoizing depth-first search (DFS)**
   - Discuss if memoizing DFS saves significant memory compared to BFS.
   
6. **Path-checking depth-first search**
   - Implement a recursive path-checking DFS.
   - Discuss if path-checking DFS saves significant memory compared to BFS.
   - Provide an example graph illustrating this point.
   
7. **Iterative deepening search (IDS)**
   - Discuss the concept of depth-limited search and iterative deepening search.
   - Implement IDS.
   - Discuss your implementation in the report.
   - Test your implementation to ensure it returns the shortest path.
   
8. **Discussion questions**
   - Consider the use of path-checking DFS or memoizing DFS in IDS.
   - Discuss the modified problem where a certain number of chickens can be eaten.
   
