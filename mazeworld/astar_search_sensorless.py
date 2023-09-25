from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object
    def __init__(self, state, heuristic, parent=None, transition_cost=0, direction=None):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.cost = transition_cost
        self.direction = direction

    def priority(self):
        # you write this part
        return self.cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()

# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.direction)
        current = current.parent
    result.reverse()
    return result[1:]

def set_to_sorted_tuple(set):
    sorted_list = sorted(set)
    return tuple(sorted_list)

def astar_search_sensorless(search_problem, heuristic_fn):
    init_states = search_problem.init_states
    start_node = AstarNode(init_states, heuristic_fn(search_problem.init_states))
    pqueue = []
    heappush(pqueue, start_node)
    visited_cost = {set_to_sorted_tuple(init_states): 0}
    
    while pqueue:
        cur_node = heappop(pqueue)
        cur_state = cur_node.state

        if len(cur_state) == 1:
            path = backchain(cur_node)
            search_problem.path = path
            print('Solution found!!🤖🙌')
            return path

        for direction in ['N','S','E','W']:
            next_state = search_problem.get_successors(cur_state, direction)
            action_cost = 1
            new_cost = cur_node.cost + action_cost
            next_state_tuple = set_to_sorted_tuple(next_state)
            if next_state_tuple not in visited_cost or new_cost < visited_cost[next_state_tuple]:
                visited_cost[next_state_tuple] = new_cost
                new_node = AstarNode(next_state, heuristic_fn(next_state), cur_node, new_cost, direction)
                heappush(pqueue, new_node)
        print('seaching....')
    return 'no solution!!'