import heap
import operator

def merge_two(l1, l2, k):
	out = []
	i1, i2 = 0, 0
	while len(out) < k and i1 < len(l1) and i2 < len(l2):
		if l1[i1] <= l2[i2]:
			out.append(l1[i1])
			i1 += 1
		else:
			out.append(l2[i2])
			i2 += 1
	if i1 == len(l1):
		while len(out) < k and i2 < len(l2):
			out.append(l2[i2])
			i2 += 1
	elif i2 == len(l2):
		while len(out) < k and i1 < len(l1):
			out.append(l1[i1])
			i1 += 1
	return out


def merge(arrays, k):
	h = heap.Heap(initial_size=len(arrays), comp=operator.lt)
	for (ix, a) in enumerate(arrays):
		if len(a) == 0:
			continue
		h.add(ix, a[0], (0, a))
	out = []
	while len(out) < k and not h.is_empty():
#		print "heap dump:", h.string()
		next = h.peek()
		ni, na = next['value']
		nk = next['key']
#		print "out, na, ni:", out, na, ni
		out.append(na[ni])
		ni += 1
		if ni < len(na):
#			h.add(nk, na[ni], (ni, na))
			priority = na[ni]
			value = (ni, na)
			h.set_priority(nk, priority, value)
		else:
			h.pop()
	return out

two_egs = [
	([], [], 0),
	([], [], 2),
	([], [1,3,3], 0),
	([], [1,3,3], 2),
	([], [1,3,3], 4),
	([1,3,3], [], 0),
	([1,3,3], [], 2),
	([1,3,3], [], 4),
	([1,4,4,6], [2,3,3,4,8], 0),
	([1,4,4,6], [2,3,3,4,8], 2),
	([1,4,4,6], [2,3,3,4,8], 5),
	([1,4,4,6], [2,3,3,4,8], 15),
	([2,3,3,4,8], [1,4,4,6], 0),
	([2,3,3,4,8], [1,4,4,6], 2),
	([2,3,3,4,8], [1,4,4,6], 5),
	([2,3,3,4,8], [1,4,4,6], 15),
]

for (t1, t2, k) in two_egs:
	print "input:", t1, t2, k
	two = merge_two(t1, t2, k=k)
	print "merge_two:", two
	m = merge([t1, t2], k)
	print "merge:", m
	print "equal?", two == m
	print "\n"

n_egs = [
	([], 0),
	([], 8),
	([[3]], 0),
	([[3]], 1),
	([[3]], 3),
	([[3], [], [5, 8], [3], [3, 9]], 0),
	([[3], [], [5, 8], [3], [3, 9]], 2),
	([[3], [], [5, 8], [3], [3, 9]], 6),
	([[3], [], [5, 8], [3], [3, 9]], 10),
	([[3], [1,1,18,18], [4,5,8,8], [3,4], [3,9,91,92]], 20),
]

print
for (arrs, k) in n_egs:
	print "many input: ", arrs, k
	print merge(arrs, k)
	print
