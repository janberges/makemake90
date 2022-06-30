#!/usr/bin/env python3

'''Usage: makemake.py [src=...] [obj=...] [mod=...] [bin=...]

Optional arguments specify places for source (.f90), object (.o), module
(.mod), and executable files. They all default to the currect directory.
There is no need to specify them again when updating existing makefiles.
'''

import os
import re
import sys

args = {
    'src': '.',
    'obj': '.',
    'mod': '.',
    'bin': '.',
    }

preamble = ''
epilogue = ''

for filename in 'GNUmakefile', 'makefile', 'Makefile':
    if os.path.exists(filename):
        with open(filename) as makefile:
            for line in makefile:
                if 'generated by makemake' in line:
                    for arg in re.findall('\w+=[^\s:=]+', line):
                        sys.argv.insert(1, arg)
                    break

                preamble += line
            else:
                raise SystemExit('Unknown Makefile already exists')

            for line in makefile:
                if 'not generated by makemake' in line:
                    break

            for line in makefile:
                epilogue += line
        break

for arg in sys.argv[1:]:
    if '=' in arg:
        key, value = arg.split('=')

        if key in args:
            args[key] = value
    else:
        raise SystemExit(__doc__.rstrip())

preamble = preamble or '''
FC = gfortran

flags_gfortran = -std=f2008 -Wall -pedantic
flags_ifort = -O0 -warn all

FFLAGS = ${{flags_$(FC)}}

# exception.o: FFLAGS += -Wno-maybe-uninitialized
# LDLIBS = -llapack -lblas

modules_gfortran = -J{0}
modules_ifort = -module {0}

override FFLAGS += ${{modules_$(FC)}}

needless = {0}/*.mod
'''.format(args['mod'])

preamble = preamble.strip()
epilogue = epilogue.strip()

references = {}
companions = {}
components = {}

folders = [args['src']]

for folder in folders:
    for file in os.listdir(folder):
        if file.startswith('.'):
            continue

        path = folder + '/' + file

        if os.path.isdir(path):
            folders.append(path)

        elif path.endswith('.f90'):
            doto = re.sub('^%s/' % args['src'], '%s/' % args['obj'], path)
            doto = re.sub(r'\.f90$', '.o', doto)

            references[doto] = set()

            with open(path) as code:
                for line in code:
                    match = re.match(r'\s*(use|program|module)'
                        r'\s+(\w+)\s*(?:$|,)', line, re.I)

                    if match:
                        statement, name = match.groups()

                        if statement == 'use':
                            references[doto].add(name)

                        elif statement == 'module':
                            companions[name] = doto

                        elif statement == 'program':
                            components['%s/%s' % (args['bin'],
                                name.replace('_dot_', '.'))] = {doto}

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

for target in list(references.keys()):
    if target not in related:
        del references[target]

def join(these):
    return ' '.join(sorted(these))

programs = join(components)
adjuncts = join(related)

def listing(dependencies):
    return '\n'.join(target + ': ' + join(doto)
        for target, doto in sorted(dependencies.items()) if doto)

components = listing(components)
references = listing(references)

arguments = ''.join(' %s=%s' % (key, value)
    for key, value in sorted(args.items()) if value != '.')

content = '''

# generated by makemake.py{arguments}:

programs = {programs}

.PHONY: all clean cleaner

all: $(programs)

clean:
\trm -f $(needless) {adjuncts}

cleaner: clean
\trm -f $(programs)

$(programs):
\t$(FC) $(FFLAGS) -o $@ $^ $(LDLIBS)

{args[obj]}/%.o: {args[src]}/%.f90
\t$(FC) $(FFLAGS) -c $< -o $@

{components}

{references}
'''.format(**vars())

content = re.sub(r'(^|\s)\./', r'\1', content)

with open(filename, 'w') as makefile:
    makefile.write(preamble)
    makefile.write(content)

    if epilogue:
        makefile.write('''
# not generated by makemake.py:

{epilogue}
'''.format(**vars()))
