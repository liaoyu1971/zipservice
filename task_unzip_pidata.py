import os
import time
import file_processor
import logger

### config
SRCDIR = r"d:\ftpfiles\rt21\zip_upload"
DESDIR = r"d:\ftpfiles\rt21\upload"
BAKDIR = r"d:\ftpfiles\rt21\bak_zipupload\\" + time.strftime('%Y%m%d', time.localtime(time.time()))
LOG = logger.logger("upzip_pidata")

### execute task
def execute():
    global LOG, SRCDIR, DESDIR, BAKDIR

    LOG.write_info(" ----------- begin exec upzip_pidata ------------ ")

    # validate src & des dir
    if not os.path.exists(SRCDIR):
        LOG.write_error("src dir %s not exist!" % SRCDIR)
        return

    if not os.path.exists(DESDIR):
        LOG.write_error("des dir %s not exist!" % DESDIR)
        return

    processor = file_processor.file_processor('upzip_pidata')
    processor.process_unzip_dir(SRCDIR, DESDIR, BAKDIR)

    LOG.write_info(" ----------- complete exec upzip_pidata ------------ ")

    return



if __name__ == "__main__":
    execute()
