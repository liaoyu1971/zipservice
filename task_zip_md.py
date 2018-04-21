import os
import time
import file_processor
import logger
import configparser

### config


### linux test2
SRCDIR = "/FTPLIST/RT02/cvs"
DESDIR = "/FTPLIST/RT02/cvs_download"
BAKDIR = "/FTPLIST/RT02/cvs_bak/" + time.strftime('%Y%m%d', time.localtime(time.time()))
DISPATCH_DIR_LIST = ["organization", "display"]
SPECIAL_SRC_DIR = "/FTPLIST/RT02"

'''
### linux test1
SRCDIR = "/home/liaoyu/ftpfiles/RT02/CVS"
DESDIR = "/home/liaoyu/ftpfiles/RT02/CVS_Download"
BAKDIR = "/home/liaoyu/ftpfiles/RT02/CVS_bak/" + time.strftime('%Y%m%d', time.localtime(time.time()))
DISPATCH_DIR_LIST = ["DC10", "DC11"]
SPECIAL_SRC_DIR = "/home/liaoyu/ftpfiles/RT02"
'''
'''
### windows
SRCDIR = r"d:/ftpfiles/rt02/cvs"
DESDIR = r"d:/ftpfiles/rt02/cvs_download"
BAKDIR = r"d:/ftpfiles/rt02/cvs_bak/" + time.strftime('%Y%m%d', time.localtime(time.time()))
DISPATCH_DIR_LIST = ["DC10", "DC11"]
SPECIAL_SRC_DIR = r"d:/ftpfiles/rt02"
'''


SPECIAL_DIR_LIST = ["organization"]
LOG = logger.logger("zip_md")
TASK_NAME = "task_zip_md"



### read config
def readconfig():
    global TASK_NAME, LOG, SRCDIR, DESDIR, BAKDIR, DISPATCH_DIR_LIST,SPECIAL_SRC_DIR,SPECIAL_DIR_LIST
    cf = configparser.ConfigParser()
    cf.read("task.conf")
    SRCDIR = cf.get(TASK_NAME, "SRCDIR")
    DESDIR = cf.get(TASK_NAME, "DESDIR")
    BAKDIR = cf.get(TASK_NAME, "BAKDIR") + "/" + time.strftime('%Y%m%d', time.localtime(time.time()))
    DISPATCH_DIR_LIST = cf.get(TASK_NAME, "DISPATCH_DIR_LIST").split(",")
    SPECIAL_SRC_DIR = cf.get(TASK_NAME, "SPECIAL_SRC_DIR")
    SPECIAL_DIR_LIST = cf.get(TASK_NAME, "SPECIAL_DIR_LIST").split(",")


### exec task
def execute():
    global LOG, SRCDIR, DESDIR, BAKDIR, DISPATCH_DIR_LIST,SPECIAL_SRC_DIR,SPECIAL_DIR_LIST

    LOG.write_info(" ----------- begin exec zip_masterdata ------------ ")

    # validate src & des dir
    if not os.path.exists(SRCDIR):
        LOG.write_error("src dir %s not exist!" % SRCDIR)
        return

    if not os.path.exists(DESDIR):
        LOG.write_error("des dir %s not exist!" % DESDIR)
        return

    processor = file_processor.file_processor('zip_md')
    subsrcdirs = os.listdir(SRCDIR)

    # process files for each store directories
    for cur_dir in subsrcdirs:
        src_subdir = SRCDIR + "/" + cur_dir
        ## des_subdir = DESDIR + "/" + cur_dir
        bak_subdir = BAKDIR + "/" + cur_dir

        ## des_subdir_list = []
        if cur_dir in DISPATCH_DIR_LIST:
            des_subdir_list = os.listdir(DESDIR)
        else:
            des_subdir_list = [cur_dir]

        processor.process_zip_dir(src_subdir, DESDIR, des_subdir_list, bak_subdir,'RT02' )

    # process files in special directories
    for spe_dir_name in SPECIAL_DIR_LIST:
        spe_dir_full  = SPECIAL_SRC_DIR + "/" + spe_dir_name
        if not os.path.exists(spe_dir_full):
            LOG.write_info("special directory %s not exist!" % spe_dir_full)
            continue

        des_subdir_list = os.listdir(DESDIR)
        bak_subdir = BAKDIR + "/" + spe_dir_name
        processor.process_zip_dir(spe_dir_full, DESDIR, des_subdir_list, bak_subdir,"RT02" )

    LOG.write_info(" ----------- complete exec zip_masterdata ------------ ")

    return



if __name__ == "__main__":
    readconfig()
    execute()
