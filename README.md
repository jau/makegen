makegen
=======

A Makefile generator

*makegen* generates a makefile from a set of C files. It starts
from a given .c file and tracks down its dependencies, assuming that all .c
files have a corresponding .h file.

To this point, it's also able to call gcc with -lm if it detects an `#include <math.h>`
in any of the C files.


Vim
---
This script was created to work with Vim.

By including the following lines in your `~/.vim/ftplugin/c.vim`, you can run a project 
by simply pressing F5 when the file containing `main()` is open.

        map <F5> :!makegen % && make<CR>
        imap <F5> :!makegen % && make<CR>

