#!/usr/bin/env python

import os
import re

compiler = 'gfortran'
options = '-std=f2003 -Wall -pedantic' # -O3 -fcheck=all

references = {}
companions = {}
components = {}

folders = ['.']

for folder in folders:
    for file in os.listdir(folder):
        if file.startswith('.'):
            continue

        path = folder + '/' + file

        if os.path.isdir(path):
            folders.append(path)

        elif path.endswith('.f90'):
            doto = path[2:-4] + '.o'

            references[doto] = set()

            with open(path) as code:
                for line in code:
                    match = re.match(
                        r'\s*(use|program|module)\s+(\w+)', line, re.I)

                    if match:
                        statement, name = match.groups()

                        if (statement == 'use'):
                            references[doto].add(name)

                        elif (statement == 'module'):
                            companions[name] = doto

                        elif (statement == 'program'):
                            components[name] = {doto}

for target, modules in references.items():
    references[target] = set(companions[name]
        for name in modules if name in companions)

related = set()

for doto in components.values():
    todo = list(doto)

    for target in todo:
        new = references[target] - doto

        doto |= new
        todo += new

    related |= doto

for target in references.keys():
    if target not in related:
        del references[target]

related |= set(name + '.mod'
    for name, doto in companions.items() if doto in related)

def join(these):
    return ' '.join(sorted(these))

programs = join(components)
adjuncts = join(related)

def listing(dependencies):
    return '\n'.join(target + ': ' + join(doto)
        for target, doto in sorted(dependencies.items()) if doto)

components = listing(components)
references = listing(references)

with open('makefile', 'w') as makefile:
    makefile.write('''# generated by makemake.py

compiler = {compiler}
options = {options}
programs = {programs}

.PHONY: all clean cleaner

all: $(programs)

clean:
\t@rm -f {adjuncts}

cleaner: clean
\t@rm -f $(programs)

$(programs):
\t@echo link $@
\t@$(compiler) -o $@ $^

%.o: %.f90
\t@echo compile $*
\t@$(compiler) $(options) -c $< -o $@

{components}

{references}
'''.format(**vars()))
