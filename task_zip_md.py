import os
import time
import file_processor
import logger


m_log = logger.logger("zip_md")

###zip masterdata
def execute():
    global m_log

    m_log.write_info(" ----------- begin exec zip_masterdata ------------ ")

    # config
    srcdir = r"d:\ftpfiles\rt02\cvs"
    desdir = r"d:\ftpfiles\rt02\cvs_download"
    bakdir = r"d:\ftpfiles\rt02\cvs_bak\\" + time.strftime('%Y%m%d', time.localtime(time.time()))
    dispatch_dir_list = ["DC10", "DC11"]
    special_src_dir = r"d:\ftpfiles\rt02"
    special_dir_list = ["organization"]


    # validate src & des dir
    if not os.path.exists(srcdir):
        m_log.write_error("src dir %s not exist!" % srcdir)
        return

    if not os.path.exists(desdir):
        m_log.write_error("des dir %s not exist!" % desdir)
        return

    processor = file_processor.file_processor('zip_md')
    subsrcdirs = os.listdir(srcdir)


    # process files for each store directories
    for cur_dir in subsrcdirs:
        src_subdir = srcdir + "\\" + cur_dir
        ## des_subdir = desdir + "\\" + cur_dir
        bak_subdir = bakdir + "\\" + cur_dir

        ## des_subdir_list = []
        if cur_dir in dispatch_dir_list:
            des_subdir_list = os.listdir(desdir)
        else:
            des_subdir_list = [cur_dir]

        processor.process_dir(src_subdir, desdir, des_subdir_list, bak_subdir,'RT02' )

    # process files in special directories
    for spe_dir_name in special_dir_list:
        spe_dir_full  = special_src_dir + "\\" + spe_dir_name
        if not os.path.exists(spe_dir_full):
            m_log.write_info("special directory %s not exist!" % spe_dir_full)
            continue

        des_subdir_list = os.listdir(desdir)
        bak_subdir = bakdir + "\\" + spe_dir_name
        processor.process_dir(spe_dir_full, desdir, des_subdir_list, bak_subdir,"RT02" )

    m_log.write_info(" ----------- complete exec zip_masterdata ------------ ")

    return



if __name__ == "__main__":
    print('exec task.py')
    execute()
