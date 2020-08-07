import os
import subprocess


def call_subprocess(cmd):
    cmd = cmd.split(" ")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)

    o, e = proc.communicate()
    output = o.decode('utf-8')
    error = e.decode('utf-8')
    return_code = str(proc.returncode)
    return output, error, return_code
