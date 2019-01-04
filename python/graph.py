from heap import Heap
import operator

def build_path(preds, node):
	path = [node]
	while node in preds:
		prev = preds[node]
		path.append(prev)
		node = prev
	return path[::-1]

class Graph(object):
	def __init__(self, nodes, edges, is_directed=False):
		self._nodes = list(nodes)
		self._edges = {}
		for node in self._nodes:
#			print "node:", node
			self._edges[node] = []
		for (fr, to, weight) in edges:
#			print "edge:", fr, to, weight
			self._edges[fr].append((to, weight))
			if not is_directed:
				self._edges[to].append((fr, weight))
	def json(self):
		return {'nodes': self.nodes, 'edges': self.edges}
	def nodes(self):
		return self._nodes
	def edges(self, from_node):
		return self._edges[from_node]

class Hole(object):
	def __init__(self, start, end):
		self._row_start, self._col_start = start
		self._row_end, self._col_end = end
	def contains(self, r, c):
		return self._row_start <= r < self._row_end and self._col_start <= c < self._col_end

class GridGraph(object):
	def __init__(self, rows, cols, weight=lambda x,y: 1, holes=[]):
		self._rows = rows
		self._cols = cols
		self._holes = [hole for hole in holes]
		self._nodes = ()
		self._weight = weight
	def nodes(self):
		return ((r, c) for r in range(self._rows) for c in range(self._cols))
	def _is_valid_node(self, r, c):
		return 0 <= r < self._rows and 0 <= c < self._cols
	def _is_in_a_hole(self, r, c):
		for h in self._holes:
			if h.contains(r, c):
				return True
		return False
	def edges(self, from_node):
		r, c = from_node
		if not self._is_valid_node(r, c):
			raise ValueError("invalid node: {}".format(from_node))
		out = []
		for (row, col) in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
#			print "edge?", row, col
			if self._is_valid_node(row, col) and not self._is_in_a_hole(row, col):
				out.append(((row, col), self._weight((r, c), (row, col))))
		return out
	def json(self):
		nodes = self.nodes()
		return {'nodes': nodes, 'edges': [self.edges(node) for node in nodes]}

def dijkstra_no_path(graph, start, goal):
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
		for (neighbor, weight) in graph.edges(curr):
			if neighbor not in costs:
				h.add_or_update(neighbor, cost + weight)
	return costs

def dijkstra(graph, start, goal):
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
		for (neighbor, weight) in graph.edges(curr):
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

def astar(graph, start, goal, heuristic):
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
		for (neighbor, weight) in graph.edges(curr):
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

def prim(graph, starts=None):
	h = Heap(comp=operator.lt)
	def add(to, priority, pred):
		if not h.has_key(to):
			h.add(to, priority, pred)
		elif priority < h.item(to)['priority']:
			h.set_priority(to, priority, pred)
	# let's use the priority as the current cost, and the predecessor as the value
	trees = []
	starts = graph.nodes() if starts is None else starts
	closed = set()
	for node in starts:
		if node in closed:
			continue
		edges = []
		closed.add(node)
		fringe = set(node)
		for (to, weight) in graph.edges(node):
			# we don't need to check for dupes/already-done here, right?
			if to not in fringe:
				add(to, weight, node)
		while not h.is_empty():
			curr_item = h.pop()
			curr_key, curr_cost, pred = curr_item['key'], curr_item['priority'], curr_item['value']
			closed.add(curr_key)
			edges.append((pred, curr_key, curr_cost))
			for (to, weight) in graph.edges(curr_key):
				if to not in closed:
					add(to, weight, curr_key)
		trees.append(edges)
	return trees

class UnionFind(object):
	def __init__(self, elems):
		self._parent = dict((e, e) for e in elems)
		self._size = dict((e, 1) for e in elems)
	def find(self, a):
		curr = a
		while curr != self._parent[curr]:
			curr, self._parent[curr] = self._parent[curr], self._parent[self._parent[curr]]
		return curr
	def merge(self, a, b):
		ra, rb = self.find(a), self.find(b)
		sa, sb = self._size[ra], self._size[rb]
		if sa >= sb:
			self._parent[rb] = ra
			self._size[ra] = sa + sb
		else:
			self._parent[ra] = rb
			self._size[rb] = sa + sb

def kruskal(graph):
	nodes = list(graph.nodes())
	uf = UnionFind(nodes)
	h = Heap(comp=operator.lt)
	edges = []
	# add all edges to heap
	i = 0
	for node in nodes:
		for (to, weight) in graph.edges(node):
			h.add(i, weight, value=(node, to))
			i += 1
	# the "real" stuff
	while not h.is_empty(): # and uf.size() > 1:
		next = h.pop()
		fr, to = next['value']
		if uf.find(fr) == uf.find(to):
			continue
		weight = next['priority']
		uf.merge(fr, to)
		edges.append((fr, to, weight))
	return edges

class Queue(object):
	def __init__(self, elems=[]):
		self._front = []
		self._back = elems
		self._rotate()
	def _rotate(self):
		for x in self._back[::-1]:
			self._front.append(x)
		self._back = []
	def add(self, elem):
		self._back.append(elem)
	def pop(self):
		if len(self._front) > 0:
			return self._front.pop()
		self._rotate()
		if len(self._front) > 0:
			return self._front.pop()
		raise ValueError("unable to pop: empty")
	def is_empty(self):
		if len(self._front) > 0:
			return False
		self._rotate()
		return len(self._front) == 0
	def size(self):
		return len(self._back) + len(self._front)
	def json(self):
		return {'front': self._front, 'back': self._back}

def bfs(graph, start, stop):
	q = Queue([(start, None)])
	seen = {start: None}
	edges = []
	i = 0
	while not q.is_empty():
		(node, pred) = q.pop()
#		print "bfs next:", node, pred, q.size(), i, len(seen), q._back, q._front, seen
		i += 1
		for (to, weight) in graph.edges(node):
#			print "edge: ", to
#			if to == (5, 11):
#				print to, to in seen, q.size(), len(seen), i, seen
			if to not in seen:
#				print "bfs not in seen:", to, node
				q.add((to, node))
				seen[to] = node
				edges.append((node, to, weight))
			# kind of a hack for handling finding the goal
			if to == stop:
				return seen, edges, True
	return seen, edges, False

def dfs(graph, start, stop):
	st = [(start, None, 0)]
	seen = {}
	edges = []
	while len(st) > 0:
		(node, pred, weight) = st.pop()
		if node in seen:
			continue
		seen[node] = pred
		if pred is not None:
			edges.append((pred, node, weight))
		for (to, cost) in graph.edges(node):
			st.append((to, node, cost))
			# kind of a hack for handling finding the goal
			if to == stop:
				seen[to] = node
				return seen, edges, True
	return seen, edges, False

def bfs_dual(graph, start, stop):
	seen = {}
	edges = []

	while start not in seen_stop and stop not in seen_start:
		bfs(seen_start)
		if stop in seen_start:
			done
		bfs(seen_stop)
		if start in seen_stop:
			done
	return seen_start, seen_stop, (path, edges)

def topological_sort(graph):
	pass

def all_pairs_shortest_path(graph):
	pass

def max_flow(path):
	pass

def tarjan(graph):
	pass
