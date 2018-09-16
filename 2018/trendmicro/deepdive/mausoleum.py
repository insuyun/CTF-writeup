# uncompyle6 version 3.2.3
# Python bytecode 3.7 (3394)
# Decompiled from: Python 2.7.15 (default, Jul 23 2018, 21:31:33)
# [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
# Embedded file name: mausoleum.py
# Size of source mod 2**32: 12 bytes
import random
feed = input('\n _ feed me something _ \n')
le = len(feed) - feed.count(' ')
feed = feed.lower()
if feed.isdigit():
    print("\n _ i don't understand numbers _ \n")
else:
    if le > 1:
        print('\n _ too much for me _\n')
    else:
        if le == 0:
            print('\n _ seems your keys are stuck. retry! _\n')
        else:
            if feed == 'f':
                print('TMCTF{')
            else:
                if feed == 'l':
                    print('the_s3cr3t_')
                else:
                    if feed == 'a':
                        print('i$_unE@rth3d')
                    else:
                        if feed == 'g':
                            print('}')
                        else:
                            print(random.randint(0, 999999))
