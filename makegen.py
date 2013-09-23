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

TEMPLATE = Template("""
### auto-generated
HEADERS = ${headers}
FILES = ${units}
LIBS= ${libs}
###
""")
TAIL = """
# makefile mainly based on: 
# http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
CC=gcc
CFLAGS=-I.
MAIN_TARGET=a.out
OBJ=$(patsubst %.c, %.o, $(FILES))

run: rebuild $(MAIN_TARGET)
	@echo
	./$(MAIN_TARGET)

%.o: %.c %.h $(HEADERS)
	$(CC) -c $(CFLAGS) -o $@ $<

%.o: %.c $(HEADERS)
	$(CC) -c $(CFLAGS) -o $@ $<

$(MAIN_TARGET): $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: rebuild
rebuild:
	rm -f $(MAIN_TARGET)

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
    libs = [LIBS[h] for h in re.findall(r'#include\s+\<([^>]+).h\>', text) 
            if h in LIBS]
    return (headers, units, libs)

def main():
    if len(sys.argv) < 2:
        print "usage: %s <entry_file.c>" % __file__
        sys.exit(1)
    entry_file = sys.argv[1]
    headers, units, libs = harvest_deps(entry_file)
    units = [entry_file] + units
    contents = (
        TEMPLATE.substitute(
            headers=' '.join(headers), 
            units=' '.join(units),
            libs=' '.join(libs)) + 
        TAIL)
    with open('makefile', 'w') as fout:
        fout.write(contents)


if __name__ == '__main__':
    main()

