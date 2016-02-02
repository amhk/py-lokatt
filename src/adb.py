import os
import select
import shlex
import struct
import subprocess


class LogcatEntry(object):
    def __init__(self, pid, tid, sec, nsec, level, tag, text):
        self.pid = pid
        self.tid = tid
        self.sec = sec
        self.nsec = nsec
        self.level = level
        self.tag = tag
        self.text = text


class Device(object):
    def __init__(self, arg=''):
        if len(arg) > 0 and arg[0] != '-':  # file path
            if not os.access(arg, os.R_OK):
                raise Exception('cannot open file for reading: {}'.format(arg))
            self._cmd = 'cat {}'.format(arg)
        else:
            # -B instead of --binary, since the latter is a recent alias of -B
            self._cmd = 'adb {} exec-out "logcat -B 2>/dev/null"'.format(arg)

    def entries(self):
        proc = subprocess.Popen(shlex.split(self._cmd), stdout=subprocess.PIPE)
        while select.select([proc.stdout], [], []):
            x = proc.stdout.read(2 * 2)
            if len(x) == 0:  # end of stream
                return
            payload_size, header_size = struct.unpack('<HH', x)

            if header_size == 0:  # logger_entry_v1
                x = proc.stdout.read(4 * 4)
                pid, tid, sec, nsec = struct.unpack('<llll', x)
            elif header_size == 4 * 6:  # logger_entry_v2 or v3
                x = proc.stdout.read(4 * 5)
                pid, tid, sec, nsec, _ = struct.unpack('<llllL', x)
            elif header_size == 4 * 7:  # logger_entry_v4
                x = proc.stdout.read(4 * 6)
                pid, tid, sec, nsec, _1, _2 = struct.unpack('<lLLLLL', x)
            else:
                raise Exception('unexpected logger_entry header size={}'.
                                format(header_size))

            x = proc.stdout.read(payload_size)
            level = struct.unpack('<B', x[0])[0]
            null = x.find('\x00')
            tag = x[1:null]
            text = x[null + 1:-1].strip()

            yield LogcatEntry(pid, tid, sec, nsec, level, tag, text)


def logcat_worker(callback):
    dev = Device()
    for entry in dev.entries():
        callback(entry)
