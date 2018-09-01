from heap import Heap
import operator
import json
import time


if False:
	h = Heap()

	print h.string()

	h.add("abc", 1)
	h.add("def", 2)
	h.add("ghi", 0)
	h.add("jkl", -1)
	h.add("mno", 3)
	h.add("pqr", 1)
	h3 = Heap(elems=h.elems(), comp=operator.lt)

	print h.string()
	print h.pop_all()
	print h.string()
	print "\n"

if False:
	def e(key, priority=0, value=None):
		return {'key': key, 'priority': priority, 'value': value}

	h2 = Heap(elems=[e("abc", 2), e("def", 1), e("ghi", 3), e("jkl", -1), e("mno", 1)])

	print h2.string()
	print h2.pop_all()
	print h2.string()

if False:
	print "\n"
	print h3.string()
	h3.set_priority("jkl", 3)
	print h3.string()
	h3.set_priority("jkl", -4)
	print h3.string()
	h3.set_priority("jkl", 8)
	print h3.string()
	print h3.remove("mno")
	print h3.string()

def build_path(preds, node):
	path = [node]
	while node in preds:
		prev = preds[node]
		path.append(prev)
		node = prev
	return path[::-1]

class Graph(object):
	def __init__(self, nodes, edges, is_directed=False):
		self.nodes = nodes
		self.edges = {}
		for node in self.nodes:
			self.edges[node] = []
		for (fr, to, weight) in edges:
			self.edges[fr].append((to, weight))
			if not is_directed:
				self.edges[to].append((fr, weight))
	
	def json(self):
		return {'nodes': self.nodes, 'edges': self.edges}
	
	def dijkstra_no_path(self, start, goal):
		h = Heap(comp=operator.lt)
		h.add(start, 0)
		costs = {}
		preds = {}
		while not h.is_empty():
			entry = h.pop()
			curr, cost = entry['key'], entry['priority']
			costs[curr] = cost
			if curr == goal:
				break
			for (neighbor, weight) in self.edges[curr]:
				if neighbor not in costs:
					h.add_or_update(neighbor, cost + weight)
		return costs

	def dijkstra(self, start, goal):
		h = Heap(comp=operator.lt)
		h.add(start, 0)
		done = set()
		costs = {start: 0}
		preds = {}
		explored = 0
		while not h.is_empty():
			explored += 1
			curr = h.pop()['key']
			cost = costs[curr]
			done.add(curr)
			if curr == goal:
				return build_path(preds, curr), costs, explored, cost
			for (neighbor, weight) in self.edges[curr]:
				# 1. already done with this node: skip
				if neighbor in done:
					continue
				# 2. have not yet seen this node: add
				new_cost = cost + weight
				if neighbor not in costs:
					h.add(neighbor, new_cost)
					costs[neighbor] = new_cost
					preds[neighbor] = curr
					continue
				# 3. have already seen this node, and new cost is lower than old: update cost
				if new_cost < costs[neighbor]:
					h.set_priority(neighbor, new_cost)
					costs[neighbor] = new_cost
					preds[neighbor] = curr
		return None, costs, explored, None

	def astar(self, start, goal, heuristic):
		h = Heap(comp=operator.lt)
		start_cost = heuristic(start, goal)
		h.add(start, start_cost)
		actual_costs = {start: 0}
		preds = {}
		done = set()
		explored = 0
		while not h.is_empty():
			explored += 1
			curr = h.pop()['key']
			cost = actual_costs[curr]
			done.add(curr)
			if curr == goal:
				return build_path(preds, curr), actual_costs, h, explored, cost
			for (neighbor, weight) in self.edges[curr]:
				# 1. already done with this node: skip
				if neighbor in done:
					continue
				# 2. have not yet seen this node: add
				cost_so_far = cost + weight
				total_cost = cost_so_far + heuristic(neighbor, goal)
				if neighbor not in actual_costs:
					h.add(neighbor, total_cost)
					preds[neighbor] = curr
					actual_costs[neighbor] = cost_so_far
					continue
				# 3. have already seen this node, and new cost is lower than old: update cost
				if cost_so_far < actual_costs[neighbor]:
					h.set_priority(neighbor, total_cost)
					actual_costs[neighbor] = cost_so_far
					preds[neighbor] = curr
		return None, actual_costs, h, explored, None

graph_eg1 = Graph(["a", "b", "c", "d", "e"], [("a", "b", 1), ("b", "c", 20), ("b", "d", 3), ("c", "e", 2), ("d", "e", 4)])

print graph_eg1.dijkstra("a", "e")
print graph_eg1.dijkstra_no_path("a", "e")
print graph_eg1.dijkstra("a", "c")
print graph_eg1.dijkstra_no_path("a", "c")
print "\n"

def grid_graph(rows=10, cols=10, weight=lambda x,y: 1):
	nodes = []
	edges = []
	for row in range(rows):
		for col in range(cols):
			nodes.append((row, col))
			if row < (rows - 1):
				edges.append(((row, col), (row+1, col), weight(row, col)))
			if col < (cols - 1):
				edges.append(((row, col), (row, col+1), weight(row, col)))
	return Graph(nodes, edges)

def graph_hole(rows, cols, holes, weight=lambda x,y: 1):
	skips = set()
	nodes = []
	edges = []
	for (a, b, c, d) in holes:
		for row in range(a, c + 1):
			for col in range(b, d + 1):
				skips.add((row, col))
	for row in range(rows):
		for col in range(cols):
			nodes.append((row, col))
			if (row, col) in skips:
				continue
			if row < (rows - 1):
				edges.append(((row, col), (row+1, col), weight(row, col)))
			if col < (cols - 1):
				edges.append(((row, col), (row, col+1), weight(row, col)))
	return Graph(nodes, edges)

graph_eg2 = grid_graph(3, 3)
#print json.dumps(graph_eg2.json(), indent=2)
print graph_eg2.dijkstra((0, 0), (2, 2))
print
print graph_eg2.dijkstra((0, 0), (0, 2))

graph3 = grid_graph(5, 5, lambda x, y: x * y + 1)

#print graph3.json()
print
print graph3.dijkstra((0, 0), (4, 4))
print

graph4 = graph_hole(3, 3, [(0, 0, 1, 1)])
print graph4.json()
print 

graph5 = graph_hole(20, 20, [(10, 3, 12, 13)])
print graph5.dijkstra((0, 5), (15, 5))
print

def grid_distance(node, goal):
	return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

graph6 = graph_hole(4, 4, [(1, 0, 1, 1)])
#for x in sorted(graph6.json()['edges'].items(), key=lambda x: x[0]):
#	print x
print graph6.astar((3, 0), (0, 0), heuristic=grid_distance)
print graph6.dijkstra((3, 0), (0, 0))

#graph7 = grid_graph(1000, 1000)
#print "graph7 dijkstra:", graph7.dijkstra((99, 99), (0, 0))[-2:]
#print "graph7 astar:", graph7.astar((99, 99), (0, 0), heuristic=grid_distance)[-2:]

def measure_time(f):
	start = time.time()
	return_val = f()
	stop = time.time()
	return return_val, stop - start

graph8 = grid_graph(1000, 1000)
print "done building graph8"
print "graph8 astar:", measure_time(lambda: graph8.astar((99, 99), (0, 0), heuristic=grid_distance)[-2:])
print "graph8 astar:", measure_time(lambda: graph8.astar((999, 999), (0, 0), heuristic=grid_distance)[-2:])
print "graph8 dijkstra:", measure_time(lambda: graph8.dijkstra((99, 99), (0, 0))[-2:])
print "graph8 dijkstra:", measure_time(lambda: graph8.dijkstra((999, 999), (0, 0))[-2:])

