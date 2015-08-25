#!/usr/bin/env python
#coding: utf-8
# author: Marcelo Criscuolo
# date: Sep, 22, 2013
"""A makefile generator

This script generates a makefile from a set of C files. It starts
from a given .c file and tracks down its dependencies, assuming that all .c
files have a corresponding .h file.
"""

import os.path
import re
import sys
from string import Template

LIBS = {'math': '-lm'}

HEADER_TEMPLATE = Template("""
### auto-generated
HEADERS = ${headers}
FILES = ${units}
LIBS= ${libs}
###
""")

DEFAULT_MAKEFILE = """
# makefile mainly based on: 
# http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
CC=gcc
CFLAGS=-g -I.
MAIN_TARGET=a.out
OBJ=$(patsubst %.c, %.o, $(FILES))

run: $(MAIN_TARGET)
	@echo
	./$(MAIN_TARGET)

%.o: %.c %.h $(HEADERS)
	$(CC) -c $(CFLAGS) -o $@ $<

%.o: %.c $(HEADERS)
	$(CC) -c $(CFLAGS) -o $@ $<

$(MAIN_TARGET): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean
clean:
	rm -f *.o $(MAIN_TARGET) makefile
"""

def harvest_deps(fname):
    with open(fname) as fin:
        text = fin.read()
    headers = set(re.findall(r'#include\s+"([^.]+).h"', text))
    units = set() 
    for h in headers:
        if os.path.exists(h + '.c'):
            units.add(h)
    headers = headers.difference(units)
    headers = [h + '.h' for h in headers]
    units = [u + '.c' for u in units]
    libs = [LIBS[h] for h in re.findall(r'#include\s*\<([^>]+).h\>', text) 
            if h in LIBS]
    return (headers, units, libs)


def track_deps(entry_file):
    agenda = [entry_file]
    headers = set()
    units = set()
    libs = set()
    while agenda:
        entry_file = agenda.pop()
        units.add(entry_file)
        dep_headers, next_units, dep_libs = harvest_deps(entry_file)
        if entry_file in next_units: # avoids cycles when x.c includes x.h
            next_units.remove(entry_file)
        agenda.extend(next_units)
        headers.update(dep_headers)
        libs.update(dep_libs)
    return (headers, units, libs)


def main():
    if len(sys.argv) < 2:
        print "usage: %s <entry_file.c>" % __file__
        sys.exit(1)
    entry_file = sys.argv[1]
    headers, units, libs = track_deps(entry_file)
    contents = (
            HEADER_TEMPLATE.substitute(
            headers=' '.join(headers), 
            units=' '.join(units),
            libs=' '.join(libs)) 
            + DEFAULT_MAKEFILE)
    with open('makefile', 'w') as fout:
        fout.write(contents)


if __name__ == '__main__':
    main()

