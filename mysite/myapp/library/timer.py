#!/usr/bin/python


import datetime
import time
import logging

class timer():
    def __init__(self):
        for i in range(0, 20):
            logging.info(datetime.time.microsecond)
            time.sleep(2)

    def time(self):
        return datetime.datetime.strptime('6/13/18','%m/%d/%y')