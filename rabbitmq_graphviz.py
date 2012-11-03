import argparse
import json
import sys

def escape_id(id_str):
    return id_str.replace('-', '').replace('.', '_')

def build_definitions(definitions, render_producers, render_consumers):
    return ''.join([
        'digraph {\n',
        '  bgcolor=transparent;\n',
        '  truecolor=true;\n',
        '  rankdir=LR;\n',
        '  node [style="filled"];\n\n',
        ''.join([build_queue(q, render_consumers) for q in definitions['queues']]),
        ''.join([build_exchange(x, render_producers) for x in definitions['exchanges']]),
        ''.join([build_binding(b) for b in definitions['bindings']]),
        '}'])

def build_queue(queue, render_consumers):
    lines = [
        '  subgraph cluster_Q_%s {\n' % escape_id(queue['name']),
        '    label="%s";\n' % queue['name'],
        '    color=transparent;\n',
        '    "Q_%s" [label="{||||}", fillcolor="red", shape="record"];\n' % escape_id(queue['name']),
        '  }\n\n']

    if render_consumers:
        lines.append('  "C_%s" [label="C", fillcolor="#33ccff"];' % escape_id(queue['name']))
        lines.append('  "Q_%(name)s" -> "C_%(name)s"' % { 'name': escape_id(queue['name'])})

    return ''.join(lines)

def build_exchange(exchange, render_producers):
    lines = [
        '  subgraph cluster_X_%s {\n' % escape_id(exchange['name']),
        '    label="%s\\ntype=%s";\n' % (exchange['name'], exchange['type']),
        '    color=transparent;\n',
        '    "X_%s" [label="X", fillcolor="#3333CC", shape="ellipse"];\n' % escape_id(exchange['name']),
        '  }\n\n']

    if render_producers:
        lines.append('  "P_%s" [label="P", style="filled", fillcolor="#00ffff"];' % escape_id(exchange['name']))
        lines.append('  "P_%(name)s" -> "X_%(name)s";' % { 'name': escape_id(exchange['name']) })

    return ''.join(lines)

def build_binding(binding):
    return '  X_%s -> Q_%s [label="%s"];\n' % (escape_id(binding['source']), escape_id(binding['destination']), binding['routing_key'])

def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--definitions', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Definitions file')    
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file')
    parser.add_argument('-p', '--producers', action='store_true', help='Render producers')
    parser.add_argument('-c', '--consumers', action='store_true', help='Render consumers')    
    return parser.parse_args()    

if __name__ == '__main__':
    args = parse_args()

    definitions = json.load(args.definitions)
    args.definitions.close()
        
    args.outfile.write(build_definitions(definitions, args.producers, args.consumers))
    args.outfile.close()
