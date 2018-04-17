import logging
import os
import time


### encapsulate log file writting
class logger:

    def __init__(self, task_name):
        logdir = os.path.curdir + "//log"
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logfile = logdir + "//" + task_name + "_" +  time.strftime('%Y%m%d', time.localtime(time.time())) + '.log'
        logging.basicConfig(filename = logfile,
                            level= logging.INFO,
                            format='[%(asctime)s][%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='a')

    def write_info(self, msg):
        logging.info(msg)


    def write_error(self, msg):
        logging.error(msg)


if __name__ == "__main__":
    log = logger("test")
    log.write_log("just for test: success", True)
    log.write_log("just for test: error", False)
