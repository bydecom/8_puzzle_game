import heapq
class Find:

    class PuzzleNode:
        def __init__(self, state, parent, move, depth, cost):
            self.state = state
            self.parent = parent
            self.move = move
            self.depth = depth
            self.cost = cost
        def __lt__(self, other):
            return self.cost < other.cost

    def __init__(self, initial_state,size):
        self.size = size
        self.move = []
        self.initial_state = initial_state
        self.solve_puzzle(self.initial_state,self.size)

    def generate_winning_state(self,size):
        winning_state = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == size - 1 and j == size - 1:
                    row.append(0)
                else:
                    row.append(i * size + j + 1)
            winning_state.append(row)
        return winning_state

    def get_blank_pos(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def is_valid(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def is_goal_state(self, state, size):
        goal_state = self.generate_winning_state(self.size)
        return state == goal_state

    def print_solution(self, node):
        if node is None:
            return
        self.print_solution(node.parent)
        if node.move is not None:
            self.move.append(node.move)


    def solve_puzzle(self, initial_state, size):
        moves = [(0, -1, 'LEFT'), (0, 1, 'RIGHT'), (-1, 0, 'UP'), (1, 0, 'DOWN')]
        initial_node = self.PuzzleNode(initial_state, None, None, 0, 0)
        priority_queue = []
        heapq.heappush(priority_queue, initial_node)
        seen_states = set()

        while priority_queue:
            current_node = heapq.heappop(priority_queue)

            if self.is_goal_state(current_node.state, size):
                self.print_solution(current_node)
                return

            x, y = self.get_blank_pos(current_node.state)

            for dx, dy, move in moves:
                new_x, new_y = x + dx, y + dy
                if self.is_valid(new_x, new_y):
                    new_state = [row[:] for row in current_node.state]
                    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                    new_cost = current_node.cost + 1
                    new_depth = current_node.depth + 1
                    new_node = self.PuzzleNode(new_state, current_node, move, new_depth, new_cost)

                    # Kiểm tra nếu trạng thái mới đã xuất hiện trước đó
                    if tuple(map(tuple, new_state)) not in seen_states:
                        heapq.heappush(priority_queue, new_node)
                        seen_states.add(tuple(map(tuple, new_state)))



