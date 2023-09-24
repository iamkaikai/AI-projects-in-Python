from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object
    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.cost = transition_cost

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
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    num_agent = len(search_problem.start_state) // 2
    start_node = AstarNode(tuple(search_problem.start_state), heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    visited_cost = {start_node.state: 0}

    while pqueue:
        cur_node = heappop(pqueue)
        cur_state = cur_node.state

        if cur_state == search_problem.goal:
            path = backchain(cur_node)
            search_problem.path = path
            print('Solution found!!🤖🙌')
            return path

        for i in range(num_agent):
            cur_state_agent = cur_state + (i,)
            next_states = search_problem.get_successors(cur_state_agent)
            for next_state in next_states:
                next_state = next_state[:-1]  # exclude the order at the end of tuple
                action_cost = 1
                new_cost = cur_node.cost + action_cost
                if next_state not in visited_cost or new_cost < visited_cost[next_state]:
                    visited_cost[next_state] = new_cost
                    new_node = AstarNode(next_state, heuristic_fn(next_state), cur_node, new_cost)
                    heappush(pqueue, new_node)
        print('-------------------------------------------------------------------------------- end of round')
    return 'no solution!!'
