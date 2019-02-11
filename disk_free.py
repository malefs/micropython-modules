# Usage:
#    import disk_free
#    disk_free.value()

import uos

def value():
    fs_stat = uos.statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    response = "File System Size {:,} - Free Space {:,}".format(fs_size, fs_free)
    return print(response)

