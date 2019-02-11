# MicroPython: https://docs.micropython.org
# Source: https://forum.micropython.org/viewtopic.php?f=16&t=2361&p=27050#p27050
#
# Brandon Gant
# 2019-02-12
#
# Usage:
#    import disk_free
#    disk_free.check()

import uos

def check():
    fs_stat = uos.statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    response = "File System Size {:,} - Free Space {:,}".format(fs_size, fs_free)
    return response

