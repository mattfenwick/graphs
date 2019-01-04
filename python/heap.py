import json
import operator

def parent(i):
	if i < 1:
		raise ValueError("cannot get parent of {}".format(i))
	return (i - 1) / 2

def left(i):
	return 2 * i + 1

def right(i):
	return 2 * i + 2

class Heap(object):
	"""Implements a max heap when comp=operator.gt; implements a min heap when comp=operator.lt"""
	def __init__(self, initial_size=10, elems=None, comp=operator.gt):
		self._key_to_index = {}
		self._comp = comp
		if elems is None:
			self._elems = [None] * initial_size
			self._size = 0
		else:
			size = len(elems) * 2 + 1
			self._elems = [None] * size
			for i in range(size):
				if i < len(elems):
					self._elems[i] = elems[i]
					self._key_to_index[elems[i]['key']] = i
			self._size = len(elems)
			for j in range(len(elems) / 2 - 1, -1, -1):
				self._sift_down(j)					
	
	def _get(self, i):
		if i < 0 or i >= self._size:
			raise ValueError("get: invalid index {} (expected 0 <= i < {})".format(i, self._size))
		return self._elems[i]
	
	def _set(self, i, value):
		if i < 0 or i >= self._size:
			raise ValueError("set: invalid index {} (expected 0 <= i < {})".format(i, self._size))
		self._elems[i] = value
		self._key_to_index[value['key']] = i
	
	def _clear(self, i):
		if i < 0 or i >= self._size:
			raise ValueError("clear: invalid index {} (expected 0 <= i < {})".format(i, self._size))
		item = self._elems[i]
		del self._key_to_index[item['key']]
		self._elems[i] = None
	
	def _resize(self):
		if self._size == len(self._elems):
			new_size = 1 + 2 * self._size
			self._elems = [self._elems[i] if i < len(self._elems) else None for i in range(new_size)]
	
	def _swap(self, i, j):
		"""swap does not restore the heap property.
		   It assumes the caller handles that."""
		iv = self._get(i)
		jv = self._get(j)
		self._set(i, jv)
		self._set(j, iv)
	
	def _sift_up(self, i):
		while i > 0:
			iv = self._get(i)
			p = parent(i)
			pv = self._get(p)
			if not self._comp(iv['priority'], pv['priority']):
				break
			self._swap(i, p)
			i = p
	
	def _sift_down(self, i):
		while i < self._size:
			next = i
			nv = self._get(next)
			
			l = left(i)
			if l < self._size:
				lv = self._get(l)
				if self._comp(lv['priority'], nv['priority']):
					next = l
					nv = lv
			
			r = right(i)
			if r < self._size:
				rv = self._get(r)
				if self._comp(rv['priority'], nv['priority']):
					next = r
			
			if next == i:
				break

			self._swap(i, next)
			i = next
				
	def add(self, key, priority, value=None):
		if key in self._key_to_index:
			raise ValueError("cannot add key {}: already present".format(key))
		self._resize()
		i = self._size
		self._size += 1
		self._set(i, {'priority': priority, 'key': key, 'value': value})
		self._sift_up(i)
	
	def is_empty(self):
		return self._size == 0
	
	def pop(self):
		if self._size == 0:
			return None
		return self._remove(0)
	
	def peek(self):
		if self._size == 0:
			return None
		return self._get(0)
	
	def remove(self, key):
		index = self._key_to_index[key]
		item = self._get(index)
		return self._remove(index)
	
	def item(self, key):
		index = self._key_to_index.get(key)
		if index is None:
			return None
		return self._get(index)
	
	def _remove(self, index):
		item = self._get(index)
		if index == self._size - 1:
			self._clear(index)
			self._size -= 1
			return item
		self._swap(index, self._size - 1)
		self._clear(self._size - 1)
		self._size -= 1
		self._sift_down(index)
		return item
	
	def set_priority(self, key, new_priority, value=None):
		i = self._key_to_index[key]
		item = self._get(i)
		item['priority'] = new_priority
		if value is not None:
			item['value'] = value
		self._sift_up(i)
		self._sift_down(i)
	
	def add_or_update(self, key, priority, value=None):
		if key in self._key_to_index:
			self.set_priority(key, priority, value)
		else:
			self.add(key, priority, value)
	
	def has_key(self, key):
		return key in self._key_to_index
	
	def elems(self):
		return [e for (i, e) in enumerate(self._elems) if i < self._size]
	
	def json(self):
		return {
			'elems': self._elems,
			'key_to_index': self._key_to_index,
			'size': self._size
		}
	
	def pop_all(self):
		items = []
		while not self.is_empty():
			items.append(self.pop())
		return items
	
	def string(self):
		return json.dumps(self.json(), indent=2)

