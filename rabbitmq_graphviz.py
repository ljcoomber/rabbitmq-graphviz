import argparse
import json
import logging
import sys

import pystache
from pystache import render as render

logging.basicConfig(level=logging.INFO)

# TODO:
# - vhost

def escape_id(id):
    return id.replace('-', '').replace('.', '_')

escaped_renderer = pystache.Renderer(escape=escape_id)

def mk_writer(file):
    def writer(tmpl, obj=None, escape=False):
        if obj:
            if escape:
                render_f = escaped_renderer.render
            else:
                render_f = render

            file.write(render_f(tmpl + '\n', obj))
        else:
            file.write(tmpl + '\n')

    return writer


def render_definitions(write, definitions):
    write('digraph {')
    write('  bgcolor=transparent;')
    write('  truecolor=true;')
    write('  rankdir=LR;')
    write('  node [style="filled"];\n')

    [render_queue(write, q) for q in definitions['queues']]
    [render_exchange(write, x) for x in definitions['exchanges']]
    [render_binding(write, b) for b in definitions['bindings']]

    write('}')

def render_queue(write, queue):
    write('  subgraph cluster_Q_{{name}} {', queue, escape=True)
    write('    label="{{name}}";', queue)
    write('    color=transparent;')
    write('    "Q_{{name}}" [label="{||||}", fillcolor="red", shape="record"];', queue, escape=True)
    write('  }\n')

def render_exchange(write, exchange):
    write('  subgraph cluster_X_{{name}} {', exchange, escape=True)
    write('    label="{{name}}\\ntype={{type}}";', exchange)
    write('    color=transparent;')
    write('    "X_{{name}}" [label="X", fillcolor="#3333CC", shape="ellipse"];', exchange, escape=True)
    write('  }\n')

def render_binding(write, binding):
    write('  X_{{source}} -> Q_{{destination}} [label="{{routing_key}}"];', binding, escape=True)

def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--definitions', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Definitions file')    
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    return parser.parse_args()    

if __name__ == '__main__':
    args = parse_args()

    definitions = json.load(args.definitions)
    args.definitions.close()

    render_definitions(mk_writer(args.outfile), definitions)

    args.outfile.close()
