# Quickie D3JS-NX interface for Jupyter Notebooks
# Copyright (c) Nick Timkovich 2015
# MIT Licensed
from __future__ import absolute_import, division, print_function
import uuid
import json

from IPython.display import HTML
import jinja2

__all__ = ['nx_force']

env = jinja2.Environment()

template = env.from_string('''
<style>
    .node {
      stroke: #fff;
      stroke-width: 1.5px;
    }

    .link {
      stroke: #999;
      stroke-opacity: .6;
    }
</style>
<script>
+function() {
    var options = {
        'divid': '#{{ divid }}',
        'data': {{ data }},
        'width': {{ width }},
        'height': {{ height }},
    }

    if (window.d3 === undefined) {
        console.log('Loading D3 from CDN');
        $.getScript('https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.7/d3.js')
            .done(function() {
                plot_force(options);
            });
    } else {
        plot_force(options);
    }

    function plot_force(o) {
        var color = d3.scale.category20();

        var svg = d3.select(o.divid).append("svg")
            .attr("width", o.width)
            .attr("height", o.height);

        var force = d3.layout.force()
            .charge(-120)
            .linkDistance(30)
            .size([o.width, o.height])
            .nodes(o.data.nodes)
            .links(o.data.links)
            .start();

        var link = svg.selectAll(".link")
                .data(o.data.links)
            .enter().append("line")
                .attr("class", "link")
                .style("stroke-width", function(d) { return Math.sqrt(d.value); });

        var node = svg.selectAll(".node")
                .data(o.data.nodes)
            .enter().append("circle")
                .attr("class", "node")
                .attr("r", 5)
                .style("fill", function(d) { return color(d.group); })
                .call(force.drag);

        node.append("title")
            .text(function(d) { return d.name; });

        force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
        });
    }
}();
</script>
<div id="{{ divid }}">
</div>
'''.strip())

def nx_force(G, size=(600, 400)):
    """
    Provided a NetworkX graph, render it in JS using D3js.
    """
    data = {
        'nodes': [],
        'links': [],
    }
    node_index_map = {}
    for i, (node, ndata) in enumerate(G.nodes_iter(data=True)):
        node_index_map[node] = i
        data['nodes'].append({
                'name': str(node),
                'group': ndata.get('group', 0)
            })
    for u, v, edata in G.edges_iter(data=True):
        data['links'].append({
                'source': node_index_map[u],
                'target': node_index_map[v],
                'value': edata.get('weight', 1)
            })

    html = template.render(
            width=size[0],
            height=size[1],
            divid='x' + uuid.uuid4().hex,
            data=json.dumps(data),
        )
    return HTML(html)
