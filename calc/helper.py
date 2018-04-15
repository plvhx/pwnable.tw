#! /usr/bin/python

import gdb

gdb.execute('run')
gdb.execute('set $eip = 0x0804947b')
gdb.execute('c')
