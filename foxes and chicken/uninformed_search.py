
from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
# keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node and all search nodes wrap a state object
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        return None

# you might write other helper functions, too. For example,
# I like to separate out backchaining, and the dfs path checking functions

def trace_parent(node):
    chain = []
    while node:
        chain.append(node.state)
        node = node.parent
    chain.reverse()
    return chain
    
def bfs_search(search_problem):
    explored = set()
    start_node = SearchNode(search_problem.start_state)
    solution = SearchSolution(search_problem, "BFS")
    q = deque()
    q.append(start_node)
    
    while q:
        current_node = q.popleft()
        current_state = current_node.state
        explored.add(current_state)
        solution.nodes_visited += 1
        
        if search_problem.goal_check(current_state):
            solution.sovled = True
            solution.path = trace_parent(current_node)
        
        successors = search_problem.get_successors(current_state)
        
        for state in successors:
            if state not in explored:
                explored.add(state)
                q.append(SearchNode(state, current_node))
    
    return solution


# Don't forget that your dfs function should be recursive and do path checking,
# rather than memoizing (no visited set!) to be memory efficient
# We pass the solution along to each new recursive call to dfs_search
# so that statistics like number of nodes visited or recursion depth might be recorded
def path_check(node, state):
        while node.parent:
            if (state == node.parent.state):
                return False
            node = node.parent
        return True
    
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    
    # initialize the node and solution    
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    result = solution           
    
    # base case
    if depth_limit == 0 or solution.sovled:
        return solution  
    
    # back tracking the path if solution is found 
    if search_problem.goal_check(node.state):
        while node:
            solution.path.append(node.state)
            node = node.parent
        solution.path.reverse()
        solution.sovled = True
        return solution
                        
    # recursion
    for s in search_problem.get_successors(node.state):
        child_node = SearchNode(s, node)
        solution.nodes_visited += 1
        if path_check(node, s):
            result = dfs_search(search_problem, depth_limit-1, child_node, solution)
    if result:
        return result

def ids_search(search_problem, depth_limit=100):
    iter_depth = 1
    
    while iter_depth <= depth_limit:
        solution = dfs_search(search_problem, iter_depth)
        if solution.sovled:
            return solution
        iter_depth +=1

    return dfs_search(search_problem, iter_depth)

# Memoizing DFS for extension
def memoizing_dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    
    q = []
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "memoizing_DFS")
    
    q.append(node)
    explored = set()
    explored.add(node.state)
    solution.nodes_visited += 1
    
    while q:
        cur_node = q.pop()
        current_state = cur_node.state
        
        if search_problem.goal_check(current_state):
            while cur_node:
                solution.path.append(cur_node.state)
                cur_node = cur_node.parent
            solution.path.reverse()
            solution.sovled = True
            return solution
            
        for s in search_problem.get_successors(current_state):
            if s not in explored:
                explored.add(s)
                solution.nodes_visited += 1
                child = SearchNode(s, cur_node)
                q.append(child)
    return solution