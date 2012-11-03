import argparse
import json
import sys

def escape_id(id_str):
    return id_str.replace('-', '').replace('.', '_')

def render_definitions(write, definitions, render_producers):
    write('digraph {')
    write('  bgcolor=transparent;')
    write('  truecolor=true;')
    write('  rankdir=LR;')
    write('  node [style="filled"];\n')

    [render_queue(write, q) for q in definitions['queues']]
    [render_exchange(write, x, render_producers) for x in definitions['exchanges']]
    [render_binding(write, b) for b in definitions['bindings']]

    write('}')

def render_queue(write, queue):
    write('  subgraph cluster_Q_%s {' % escape_id(queue['name']))
    write('    label="%s";' % queue['name'])
    write('    color=transparent;')
    write('    "Q_%s" [label="{||||}", fillcolor="red", shape="record"];' % escape_id(queue['name']))
    write('  }\n')

def render_exchange(write, exchange, render_producers):
    write('  subgraph cluster_X_%s {' % escape_id(exchange['name']))
    write('    label="%s\\ntype=%s";' % (exchange['name'], exchange['type']))
    write('    color=transparent;')
    write('    "X_%s" [label="X", fillcolor="#3333CC", shape="ellipse"];' % escape_id(exchange['name']))
    write('  }\n')
    write('  "P_%s" [label="P", style="filled", fillcolor="#00ffff"];' % escape_id(exchange['name']))
    write('  "P_%(name)s" -> "X_%(name)s";' % { 'name': escape_id(exchange['name']) })

def render_binding(write, binding):
    write('  X_%s -> Q_%s [label="%s"];' % (escape_id(binding['source']), escape_id(binding['destination']), binding['routing_key']))

def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--definitions', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Definitions file')    
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    parser.add_argument('-p', '--producers', action='store_true', help='Render producers')
    return parser.parse_args()    

if __name__ == '__main__':
    args = parse_args()

    definitions = json.load(args.definitions)
    args.definitions.close()

    def writer(s):
        args.outfile.write(s)
        args.outfile.write('\n')
        
    render_definitions(writer, definitions, args.producers)
    args.outfile.close()
