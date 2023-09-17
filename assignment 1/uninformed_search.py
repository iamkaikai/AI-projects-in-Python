
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
    q = deque()
    q.append(start_node)
    
    while q:
        current_node = q.popleft()
        current_state = current_node.state
        explored.add(current_state)
        
        if search_problem.goal_check(current_state):
            return trace_parent(current_node)
        
        successors = search_problem.get_successors(current_state)
        
        for state in successors:
            if state not in explored:
                explored.add(state)
                q.append(SearchNode(state, current_node))
    
    return f'\n{search_problem} cannot be solved!!\n'


# Don't forget that your dfs function should be recursive and do path checking,
# rather than memoizing (no visited set!) to be memory efficient
# We pass the solution along to each new recursive call to dfs_search
# so that statistics like number of nodes visited or recursion depth might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # base casse
    if search_problem.goal_check(node.state) == search_problem.goal_state:
        trace_parent(node)
        
    if depth_limit < 0:
        return f'\n{search_problem} cannot be solved!!\n'
    
    # recursion
    for s in search_problem.get_successors(search_problem.start_state):
        node = SearchNode(s, node)
        dfs_search(search_problem, depth_limit-1, node, solution)
    
    


def ids_search(search_problem, depth_limit=100):
#     # you write this part
    return None