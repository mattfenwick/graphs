
def html_table(graph, path, visited):
	node_strings = {}
	for (i, node) in enumerate(path):
		node_strings[node] = str(i)
	for node in visited:
		if not node in node_strings:
			node_strings[node] = '({})'.format(visited[node])#'X'
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
		rows[-1].append({
			'key': node_strings.get(node, '*'), #str(node),
			'hor': hor,
			'ver': ver
		})
	html = [
		'<html>',
		"<head> <link href='./style.css' rel='stylesheet' type='text/css'> </head>",
		'<table>\n']
	for row in rows:
		html_row = []
		html_edges = []
		for node in row:
			html_row.append(node['key'])
			html_row.append(node['hor'])
			html_edges.append(node['ver'])
			html_edges.append('')
		html.append('<tr>')
		html.extend(['<td><pre>' + val + '</pre></td>' for val in html_row])
		html.append('</tr>\n')
		html.append('<tr>')
		html.extend(['<td><pre>' + val + '</pre></td>' for val in html_edges])
		html.append('</tr>\n')
	html.extend(['</table>', '</html>'])
	return ''.join(html)

