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

