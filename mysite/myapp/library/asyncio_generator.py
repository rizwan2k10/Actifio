#!/usr/bin/env python

# Author: rizwan
# Created: 8/1/18,3:04 PM
# filename: asyncio_generator

import subprocess
import sys
import threading
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed
import requests
import logging


@retry(retry=retry_if_exception_type(RuntimeError), stop=stop_after_delay(60), wait=wait_fixed(0.5))
def update_db(session_id, server_port, message):

    url_base = 'http://127.0.0.1:' + str(server_port) + '/update_log'
    param = {}
    param['message'] = message
    param['sessionid'] = session_id
    resp = requests.get(url_base, verify=False, params=param)
    logging.info("%s, %d" % (message, resp.status_code))
    if resp.status_code != 200:
        raise RuntimeError
    return message


class Threader:
    t = None

    def __init__(self):
        pass
        self.t = None

    def build_cmd(self, cmd):
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

    def stdoutprocess(self, session_id, server_port, o):
        while True:
            stdoutdata = o.stdout.readline()
            # stderrdata = o.stderr.readline()
            if stdoutdata:
                update_db(session_id=session_id, message=stdoutdata.decode("utf-8"), server_port=server_port)
            # if stderrdata:
            #     update_db(session_id=session_id, message=stdoutdata.decode("utf-8"))
            else:
                break

    def create_thread(self, cmd, session_id, server_port):
        popenobj = self.build_cmd(cmd)
        self.t = threading.Thread(target=self.stdoutprocess, args=(session_id, server_port, popenobj,))
        self.t.start()
        popenobj.wait()
        self.t.join()
        logging.info("Return code", popenobj.returncode)
