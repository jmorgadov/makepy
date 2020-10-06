import os
import re
from pathlib import Path
import typer
from typer.colors import RED
from utils import *
import platform

app = typer.Typer()

@app.command(name='generate')
def generate_compile_line(
    path: Path = typer.Argument(
        default=Path('.'),
        exists=True,
        dir_okay=True,
        readable=True,
        resolve_path=True),
    out: str = typer.Argument(
        default='a'
    )):

    c_files = {}
    main_name = None

    for root, dirs, files in os.walk(str(path)):
        for f in files:
            if f.endswith('.c'):
                c_files[f[:-2]] = (str(Path(root) / Path(f)))

    if len(c_files.keys()) == 0:
        typer.secho('No C files found')
        return

    dependency_graph = {Node(f):[] for f in c_files.keys()}
    nodes = {node.name:node for node in dependency_graph.keys()}

    for f in dependency_graph.keys():
        text = []
        with open(c_files[f.name], 'r') as fi:
            text = fi.readlines()
        for line in text:

            # search dependency
            match = re.search(r'#include "\w*.h"', line)
            if match:
                dep = line[match.pos:][10:].split('.')[0]
                if dep != f.name and dep in c_files.keys():
                    item = nodes[dep]
                    dependency_graph[f].append(item)

            # check if main
            match = re.search(r'int main\(', line)
            if match:
                if main_name:
                    typer.secho('There are two definitions of \
                                \'main\' in the project', fg=RED)
                    return
                else:
                    main_name = f.name
    
    if not main_name:
        typer.secho('There is no \'main\' function in any file', fg=RED)
        return

    # Eliminating unused dependencies
    dfs(dependency_graph, nodes[main_name])

    for n in list(dependency_graph.keys()):
        if not n.visit:
            dependency_graph.pop(n)

    # Validating and order dependencies    
    valid, order = topological_sort(dependency_graph)

    if not valid:
        typer.secho('Your C files contains cyclic references', fg=RED)
        return        

    make_path = path / Path('makefile')
    save = True

    make_line = 'gcc ' + ' '.join(order)

    if out != 'a':
        plt = platform.system()
        extension = ''
        if plt == 'Linux':
            extension = '.out'
        elif plt == 'Windows':
            extension = '.exe'
        make_line += f' -o {out + extension}'

    if make_path.exists():
        typer.secho(f'There is already a makefile in {str(path)}')
        typer.secho('Do you whant to overwrite it? (y/n)')
        ipt = input()
        save = ipt in ['y', 'Y']

    if save:
        with open(str(make_path), 'w') as f:
            f.write('compile:\n')
            f.write('\t' + make_line)
        typer.secho('File saved')

if __name__ == '__main__':    
    app()
