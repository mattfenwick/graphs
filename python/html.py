class Element(object):
	def __init__(self, name, children, attrs, classes):
		self.name = name
		self.attrs = attrs
		if len(classes) > 0:
			self.attrs.append(('class', ' '.join(classes)))
		self.children = children

	def html(self, lines, indent=0):
		ind = '  ' * indent
		attrs = ''
		if len(self.attrs) > 0:
			attrs = ''.join(' {}="{}"'.format(key, val) for (key, val) in self.attrs)
		open_tag = '{}<{}{}>'.format(ind, self.name, attrs)
		close_tag = '</{}>'.format(self.name)
		if len(self.children) == 1 and isinstance(self.children[0], str):
			lines.append('{}{}{}'.format(open_tag, self.children[0], close_tag))
			return
		lines.append(open_tag)
		for c in self.children:
			if isinstance(c, str):
				lines.append(c)
			else:
				c.html(lines, indent + 1)
		lines.append('{}{}'.format(ind, close_tag))

def html(children):
	return Element('html', children, [], [])

def head(children):
	return Element('head', children, [], [])

def link(attrs):
	return Element('link', [], attrs, [])

def table():
	return Element('table', [], [], [])

def tr(classes):
	return Element('tr', [], [], classes)

def td(text, classes):
	return Element('td', [text], [], classes)
		
def graph_table(graph, path, visited):
	node_strings = {}
	for (i, node) in enumerate(path):
		node_strings[node] = ('path', str(i))
	for node in visited:
		if not node in node_strings:
			node_strings[node] = ('fringe', str(visited[node]))
	rows = []
	nodes = sorted(graph.nodes)
	prev = None
	for node in nodes:
		if node[0] != prev:
			prev = node[0]
			rows.append([])
		hor = ''
		ver = ''
		for ((r, c), w) in graph.edges[node]:
			if r == (node[0] + 1) and c == node[1]:
				ver = str(w)
			if r == node[0] and c == (node[1] + 1):
				hor = str(w)
		html_class, val = node_strings.get(node, ('notvisited', '*'))
		rows[-1].append({
			'class': html_class,
			'val': val,
			'hor': hor,
			'ver': ver
		})
	tbl = table()
	for row in rows:
		tr_nodes = tr(classes=['nodes'])
		tr_edges = tr(classes=['edges'])
		for node in row:
			tr_nodes.children.append(td(node['val'], [node['class']]))
			hor = node['hor']
			ver = node['ver']
			tr_nodes.children.append(td(hor, ['edge' if hor != '' else 'filler']))
			tr_edges.children.append(td(ver, ['edge' if ver != '' else 'filler']))
			tr_edges.children.append(td('', ['filler']))
		tbl.children.extend([tr_nodes, tr_edges])
	return tbl

def graph_html(graphs):
	doc = html([
		head([
			link(attrs=[('href', './style.css'), ('rel', 'stylesheet'), ('type', 'text/css')])
		])
	])
	for (graph, path, visited) in graphs:
		doc.children.append(graph_table(graph, path, visited))
		doc.children.append(Element('hr', [], [], []))
	lines = []
	doc.html(lines)
	return '\n'.join(lines)

