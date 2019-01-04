from heap import Heap
from html import graph_html
import graph
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

if True:
	graph_eg1 = graph.Graph(["a", "b", "c", "d", "e"], [("a", "b", 1), ("b", "c", 20), ("b", "d", 3), ("c", "e", 2), ("d", "e", 4)])

	print graph.dijkstra(graph_eg1, "a", "e")
	print graph.dijkstra_no_path(graph_eg1, "a", "e")
	print graph.dijkstra(graph_eg1, "a", "c")
	print graph.dijkstra_no_path(graph_eg1, "a", "c")
	print "\n"

gg1 = """
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
"""

if True:
	graph_eg2 = graph.GridGraph(3, 3)
	#print json.dumps(graph_eg2.json(), indent=2)
	print graph.dijkstra(graph_eg2, (0, 0), (2, 2))
	print
	print graph.dijkstra(graph_eg2, (0, 0), (0, 2))

if True:
	graph3 = graph.GridGraph(5, 5, lambda _, (x, y): x * y + 1)
	#print graph3.json()
	print
	print graph.dijkstra(graph3, (0, 0), (4, 4))
	print

if True:
	graph4 = graph.GridGraph(3, 3, holes=[graph.Hole((0, 0), (1, 1))])
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
	graph9 = graph.GridGraph(22, 22, holes=[graph.Hole((7, 5), (8, 15)), graph.Hole((8, 13), (13, 15))])
	print
	print "graph9 dijkstra:", measure_time(lambda: graph.dijkstra(graph9, (2, 19), (18, 3))[-2:])
	print "graph9 astar, grid_distance:", measure_time(lambda: graph.astar(graph9, (2, 19), (18, 3), heuristic=grid_distance)[-2:])
	print "graph9 astar, bird_distance:", measure_time(lambda: graph.astar(graph9, (2, 19), (18, 3), heuristic=bird_distance)[-2:])
	print "graph9 astar, bird_distance / 2:", measure_time(lambda: graph.astar(graph9, (2, 19), (18, 3), heuristic=lambda *xs: bird_distance(*xs) / 2.0)[-2:])
	print "graph9 astar, bird_distance * 2:", measure_time(lambda: graph.astar(graph9, (2, 19), (18, 3), heuristic=lambda *xs: bird_distance(*xs) * 2.0)[-2:])
	d_path, d_costs, d_explored_count, d_cost = graph.dijkstra(graph9, (19, 2), (3, 18))
	path, costs, hp, explored_count, cost = graph.astar(graph9, (19, 2), (3, 18), heuristic=grid_distance)

	graph9_b = graph9 # graph.GridGraph(3, 3)
	dfs_seen, dfs_edges, dfs_succeeded = graph.dfs(graph9_b, (0, 0), (18, 18))
	print "nodes, edges:", len(list(graph9_b.nodes())), len(dfs_edges)
	graph9_dfs = graph.Graph(graph9_b.nodes(), dfs_edges)
	bfs_seen, bfs_edges, bfs_succeeded = graph.bfs(graph9_b, (0, 0), (18, 18))
	print "more nodes, edges:", len(list(graph9_b.nodes())), len(bfs_edges)
	graph9_bfs = graph.Graph(graph9_b.nodes(), bfs_edges)

	with open('graph.html', 'w') as f:
		f.write(graph_html([
			(graph9, d_path, d_costs), 
			(graph9, path, costs),
			(graph9_bfs, [], dict((k, 1) for k in bfs_seen)),
			(graph9_dfs, [], dict((k, 1) for k in dfs_seen)),
			]))

if True:
	graph10 = graph.Graph(
		['a', 'b', 'c', 'd', 'e'], 
		[
			('a', 'a', 0),
			('b', 'a', 1),
			('a', 'c', 3),
			('d', 'd', 1),
			('e', 'e', 1),
			('d', 'e', 6),
			('d', 'e', 4),
			('d', 'e', 2),
		])
	print "graph10 prim:", graph.prim(graph10)
	print "graph10 kruskal:", graph.kruskal(graph10)

	graph11 = graph.GridGraph(4, 4, weight = lambda (r1, c1), (r2, c2): min(abs(r1-c1), abs(r2-c2)) + 1)
	print "graph11 prim:", graph.prim(graph11)
