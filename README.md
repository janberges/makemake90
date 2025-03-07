# makemake90

Generate Makefiles for modular Fortran programs.

## Installation

Either from PyPI:

    python3 -m pip install makemake90

Or from GitHub:

    python3 -m pip install git+https://github.com/janberges/makemake90

## Synopsis

Generate Makefile for all `.f90` files in the current directory and its
subdirectories, optionally indicating special directories of your project:

    makemake90 src=src obj=build mod=build bin=bin

Customize Makefile preamble (before the line with `generated by makemake`):

    $EDITOR Makefile

Build your project:

    make FC=gfortran FFLAGS=-O3

Update Makefile after further work on project:

    makemake90

**Note:** Procedures that are not part of a module are only considered if the
code that uses them lists them in an `EXTERNAL` statement.
