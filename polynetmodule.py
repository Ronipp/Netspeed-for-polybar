#!/usr/bin/env python
import subprocess as sb
import time


def get_bytes(type):
    return int(sb.run(
        ['cat', '/sys/class/net/wlan0/statistics/%sx_bytes' % (type)],
        capture_output=True, text=True).stdout)


def get_state():
    if int(sb.run(
            ['cat', '/sys/class/net/wlan0/carrier'],
            capture_output=True, text=True).stdout) == 0:
        return False
    else:
        return True


def calcspeed():

    bytes_upf = get_bytes('t')
    bytes_downf = get_bytes('r')
    time.sleep(2)
    bytes_upl = get_bytes('t')
    bytes_downl = get_bytes('r')
    return (bytes_downl - bytes_downf) / 2, (bytes_upl - bytes_upf) / 2


def makehumanreadable(bytes):
    if bytes < 1024:
        return '%d B/s' % (bytes)
    elif 1024 <= bytes < 1048576:
        return '%4.1f KB/s' % (bytes/1024)
    else:
        return '%4.1f MB/s' % (bytes/1048576)


def sendspeed():
    downspeed, upspeed = calcspeed()
    down = makehumanreadable(downspeed)
    up = makehumanreadable(upspeed)
    with open('/tmp/netspeed.txt', 'w') as speedtxt:
        speedtxt.write(' %s  %s' % (down, up))
    sb.run(['polybar-msg', 'hook', 'wifi', '1'])


def setoffline():
    sb.run(['polybar-msg', 'hook', 'wifi', '2'])


if __name__ == '__main__':

    while True:
        print(get_state())
        if get_state():
            sendspeed()
        else:
            setoffline()
            time.sleep(2)
