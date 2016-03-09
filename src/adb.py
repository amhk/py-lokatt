import logging
import os
import random
import select
import shlex
import string
import struct
import subprocess
import time

logger = logging.getLogger(__name__)


class LogcatEntry(object):
    def __init__(self, pid, tid, sec, nsec, level, tag, text):
        def _wash(s):
            s = ''.join(ch if ch in string.printable else repr(ch) for ch in s)
            s = s.replace('\n', repr('\n'))
            s = s.replace('\t', repr('\t'))
            return s

        self.pid = pid
        self.tid = tid
        self.sec = sec
        self.nsec = nsec
        self.level = level
        self.tag = _wash(tag)
        self.text = _wash(text)


class Device(object):
    def __init__(self, path=None):
        logger.debug('Device.ctor path={}'.format(path))
        if path is None:
            # -B instead of --binary, since the latter is a recent alias of -B
            # TODO: accept adb options -d, -e, -s serial
            self._cmd = 'adb exec-out "logcat -B 2>/dev/null"'
        else:
            if not os.access(path, os.R_OK):
                raise Exception('cannot open file for reading: {}'.format(path))
            self._cmd = 'cat {}'.format(path)

    def entries(self):
        dev_null = open('/dev/null', 'w')
        proc = subprocess.Popen(shlex.split(self._cmd), stdout=subprocess.PIPE, stderr=dev_null)
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
        dev_null.close()


def logcat_worker(callback, path=None, lambd=None):
    dev = Device(path)
    for entry in dev.entries():
        callback(entry)
        if lambd is not None:
            delay = random.expovariate(lambd)
            time.sleep(delay)
