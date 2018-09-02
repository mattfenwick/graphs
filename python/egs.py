from heap import Heap
from graph import Graph
from html import graph_html
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

if False:
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

if False:
	graph_eg2 = grid_graph(3, 3)
	#print json.dumps(graph_eg2.json(), indent=2)
	print graph_eg2.dijkstra((0, 0), (2, 2))
	print
	print graph_eg2.dijkstra((0, 0), (0, 2))

if False:
	graph3 = grid_graph(5, 5, lambda x, y: x * y + 1)
	#print graph3.json()
	print
	print graph3.dijkstra((0, 0), (4, 4))
	print

if False:
	graph4 = graph_hole(3, 3, [(0, 0, 1, 1)])
	print graph4.json()
	print

if False:
	graph5 = graph_hole(20, 20, [(10, 3, 12, 13)])
	print graph5.dijkstra((0, 5), (15, 5))
	print

def grid_distance(node, goal):
	return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def bird_distance(node, goal):
	return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

if False:
	graph6 = graph_hole(4, 4, [(1, 0, 1, 1)])
	#for x in sorted(graph6.json()['edges'].items(), key=lambda x: x[0]):
	#	print x
	print graph6.astar((3, 0), (0, 0), heuristic=grid_distance)
	print graph6.dijkstra((3, 0), (0, 0))

if False:
	graph7 = grid_graph(1000, 1000)
	print "graph7 dijkstra:", graph7.dijkstra((99, 99), (0, 0))[-2:]
	print "graph7 astar:", graph7.astar((99, 99), (0, 0), heuristic=grid_distance)[-2:]

def measure_time(f):
	start = time.time()
	return_val = f()
	stop = time.time()
	return return_val, stop - start

if False:
	graph8 = grid_graph(1000, 1000)
	print "done building graph8"
	print "graph8 astar:", measure_time(lambda: graph8.astar((99, 99), (0, 0), heuristic=grid_distance)[-2:])
	print "graph8 astar:", measure_time(lambda: graph8.astar((999, 999), (0, 0), heuristic=grid_distance)[-2:])
	print "graph8 dijkstra:", measure_time(lambda: graph8.dijkstra((99, 99), (0, 0))[-2:])
	print "graph8 dijkstra:", measure_time(lambda: graph8.dijkstra((999, 999), (0, 0))[-2:])

if True:
	graph9 = graph_hole(22, 22, [(7, 5, 8, 15), (9, 13, 13, 15)])
	print
	print "graph9 dijkstra:", measure_time(lambda: graph9.dijkstra((2, 19), (18, 3))[-2:])
	print "graph9 astar, grid_distance:", measure_time(lambda: graph9.astar((2, 19), (18, 3), heuristic=grid_distance)[-2:])
	print "graph9 astar, bird_distance:", measure_time(lambda: graph9.astar((2, 19), (18, 3), heuristic=bird_distance)[-2:])
	print "graph9 astar, bird_distance / 2:", measure_time(lambda: graph9.astar((2, 19), (18, 3), heuristic=lambda *xs: bird_distance(*xs) / 2.0)[-2:])
	print "graph9 astar, bird_distance * 2:", measure_time(lambda: graph9.astar((2, 19), (18, 3), heuristic=lambda *xs: bird_distance(*xs) * 2.0)[-2:])
	d_path, d_costs, d_explored_count, d_cost = graph9.dijkstra((19, 2), (3, 18))
	path, costs, hp, explored_count, cost = graph9.astar((19, 2), (3, 18), heuristic=grid_distance)

	with open('graph.html', 'w') as f:
		f.write(graph_html([(graph9, path, costs), (graph9, d_path, d_costs)]))

