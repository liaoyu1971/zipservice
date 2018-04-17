import os
import time
import file_processor
import logger

### config
SRCDIR = r"d:\ftpfiles\rt21\download"
DESDIR = r"d:\ftpfiles\rt21\zip_download"
BAKDIR = r"d:\ftpfiles\rt21\bak_download\\" + time.strftime('%Y%m%d', time.localtime(time.time()))
LOG = logger.logger("zip_pidown")

### execute task
def execute():
    global LOG, SRCDIR, DESDIR, BAKDIR

    LOG.write_info(" ----------- begin exec zip_pidown ------------ ")

    # validate src & des dir
    if not os.path.exists(SRCDIR):
        LOG.write_error("src dir %s not exist!" % SRCDIR)
        return

    if not os.path.exists(DESDIR):
        LOG.write_error("des dir %s not exist!" % DESDIR)
        return

    processor = file_processor.file_processor('zip_pidown')
    subsrcdirs = os.listdir(SRCDIR)

    # process files for each store directories
    for cur_dir in subsrcdirs:
        src_subdir = SRCDIR + "\\" + cur_dir
        ## des_subdir = DESDIR + "\\" + cur_dir
        bak_subdir = BAKDIR + "\\" + cur_dir

        ## des_subdir_list = []
        des_subdir_list = [cur_dir]
        processor.process_zip_dir(src_subdir, DESDIR, des_subdir_list, bak_subdir, 'RT21' )

    LOG.write_info(" ----------- complete exec zip_pidown ------------ ")

    return



if __name__ == "__main__":
    execute()
