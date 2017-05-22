'''
Bare-bones timing functions
'''

import time

now = None
def tick():
    global now
    now = time.clock()
    
def tock(*s):
    global now
    if s:
        print(time.clock()-now, s[0])
    else:
        print(time.clock()-now)
    tick()
