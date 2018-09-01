from heap import Heap
import operator
from collections import defaultdict
import json

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

class Graph(object):
	def __init__(self, nodes, edges, is_directed=False):
		self.nodes = nodes
		self.edges = defaultdict(list)
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
		def build_path(node):
			path = [node]
			while node in preds:
				prev = preds[node]
				path.append(prev)
				node = prev
			return path[::-1]
		while not h.is_empty():
			curr = h.pop()['key']
			cost = costs[curr]
			done.add(curr)
			if curr == goal:
				return build_path(curr), costs
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
		return None, costs

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
			nodes.append("{}-{}".format(row, col))
			if row < (rows - 1):
				edges.append(("{}-{}".format(row, col), "{}-{}".format(row+1, col), weight(row, col)))
			if col < (cols - 1):
				edges.append(("{}-{}".format(row, col), "{}-{}".format(row, col+1), weight(row, col)))
	return Graph(nodes, edges)

graph_eg2 = grid_graph(3, 3)
#print json.dumps(graph_eg2.json(), indent=2)
print graph_eg2.dijkstra('0-0', '2-2')
print graph_eg2.dijkstra('0-0', '0-2')

graph3 = grid_graph(5, 5, lambda x, y: x * y + 1)

print graph3.json()
print
print graph3.dijkstra('0-0', '4-4')

