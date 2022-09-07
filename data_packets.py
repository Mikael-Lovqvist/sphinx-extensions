# Note - this is just a sketch so far

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

from dataclasses import dataclass

@dataclass
class packet_field:
	size: int
	title: str


class data_packet_node(nodes.General, nodes.Inline, nodes.Element):
	pass


def visit_data_packet_html(self, node):

	def format_field(index, field):
		if index:
			border = '; border-left: 1px solid var(--pst-color-on-surface)'
		else:
			border = ''

		return f'<div style="display: table-cell; padding: 5px 10px; background-color: var(--pst-color-surface){border}"><p style="color: var(--pst-color-inline-code); margin: 0;">{field.title}</p><p style="margin: 0;">{field.size}{node["suffix"]}</p></div>'

	packet_columns = [format_field(index, field) for index, field in enumerate(node['packet'])]
	count = len(node['packet'])

	rows = [
		f'<div style="display: table-row">{"".join(packet_columns)}</div>',
	]

	table = f'<div style="display: table">{"".join(rows)}</div><p>{node["name"]}</p>'
	self.body.append(table)

def depart_data_packet_html(self, node):
	pass


class data_packet(Directive):
	has_content = True

	def run(self):

		options = list()
		data = list()
		pending_targets = iter((options, data))

		target = next(pending_targets)
		for item in self.content:
			if item:
				target.append(item)
			else:
				target = next(pending_targets)

		name = options.pop(0)

		suffix = ' bytes'
		for opt in options:
			if opt == ':no-suffix:':
				suffix = ''

		packet = list()
		for item in data:
			size, info = item.split('  ', maxsplit=1)
			packet.append(packet_field(size, info))

		return [data_packet_node(
			name=name,
			packet=packet,
			suffix=suffix,
		)]

def setup(app):
	app.add_directive("data_packet", type('data_packet', (data_packet,), dict(app=app)))
	app.add_node(data_packet_node,
		html=(visit_data_packet_html, depart_data_packet_html),
		singlehtml=(visit_data_packet_html, depart_data_packet_html),
	)

	return dict(
		version = '0.1',
		parallel_read_safe = True,
		parallel_write_safe = True,
	)