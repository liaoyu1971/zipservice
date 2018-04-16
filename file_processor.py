import os
import zipfile
import time
import shutil
import logger

class file_processor:

    ## m_taskname = "task"
    m_log = None


    def __init__(self, task_name):
        ## m_taskname= task_name
        global m_log
        m_log = logger.logger(task_name)


    ### process files in specific dictory
    def process_dir(self, src_dir, des_dir_base, des_dir_list, bak_dir, zipfile_header):
        global m_log
        # validate src & des dir
        m_log.write_info("start process_dir srcdir:%s des_dir_base:%s " % (src_dir, des_dir_base))
        if not os.path.exists(src_dir):
            m_log.write_info("src dir %s not exist!" % src_dir)
            return

        filelist = self.get_filelist(src_dir, ".xml")
        m_log.write_info("file count in dir %s: %d" % (src_dir, len(filelist)))
        if len(filelist) == 0:
            return

        # zip files in src dirs
        src_dir_name = os.path.basename(src_dir)
        zipfile_name = zipfile_header + "_" + src_dir_name + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))+".zip"
        zipfile_fullname = src_dir + "\\" + zipfile_name
        m_log.write_info("zipfilename:" + zipfile_fullname)
        self.zip_dirfiles(src_dir, filelist, zipfile_fullname)

        # copy to all des sub dirs

        for cur_desdir in des_dir_list:
            # create des dirs if not exist
            if not os.path.exists(des_dir_base + "\\" +cur_desdir):
                os.mkdir(des_dir_base + "\\" +cur_desdir)
                m_log.write_info("des dir:" + des_dir_base + "\\" +cur_desdir + " created.")

            tmp_zipfilename = des_dir_base + "\\" +cur_desdir + "\\" + zipfile_name.replace(".zip", "._")
            des_zipfilename = des_dir_base + "\\" +cur_desdir + "\\" + zipfile_name
            shutil.copyfile(zipfile_fullname, tmp_zipfilename)
            os.rename(tmp_zipfilename, des_zipfilename)

        # delete src zip file
        os.remove(zipfile_fullname)

        # backup src files
        if not os.path.exists(bak_dir):
            os.makedirs(bak_dir)
        for filename in filelist:
            bak_filename = bak_dir + "\\" + os.path.basename(filename)
            shutil.move(filename, bak_filename)

        m_log.write_info("complete process_dir srcdir:%s des_dir_base:%s " % (src_dir, des_dir_base))

    ### get file list in a directory
    def get_filelist(self, dirname, fileext):
        global m_log
        filelist = []
        #Check input ...
        fulldirname = os.path.abspath(dirname)
        if not os.path.exists(fulldirname):
            return filelist

        if os.path.isfile(dirname):
            if fileext == "*" or os.path.splitext(dirname)[1]==fileext:
                filelist.append(dirname)
                dirname = os.path.dirname(dirname)
        else:
            #get all file in directory
            for root, dirlist, files in os.walk(dirname):
                for filename in files:
                    if fileext == "*" or os.path.splitext(filename)[1]==fileext:
                        filelist.append(os.path.join(root,filename))

        return filelist


    ### zip files in a directory
    def zip_dirfiles(self,dirname,filelist, zipfilename):
        global m_log
        #filelist = []
        #Check input ...
        if len(filelist) == 0:
            return
        fulldirname = os.path.abspath(dirname)
        fullzipfilename = os.path.abspath(zipfilename)
        m_log.write_info( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
        if not os.path.exists(fulldirname):
            print ("Dir/File %s is not exist, Press any key to quit..." % fulldirname)
            inputStr = raw_input()
            return
        if os.path.isdir(fullzipfilename):
            tmpbasename = os.path.basename(dirname)
            fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))
        if os.path.exists(fullzipfilename):
            print ("%s has already exist, are you sure to modify it ? [Y/N]" % fullzipfilename)
            while 1:
                inputStr = raw_input()
                if inputStr == "N" or inputStr == "n" :
                    return
                else:
                    if inputStr == "Y" or inputStr == "y" :
                        m_log.write_info("Continue to zip files...")
                        break

        #Start to zip file ...
        destZip = zipfile.ZipFile(fullzipfilename, "w")
        for eachfile in filelist:
            destfile = eachfile[len(dirname):]
            m_log.write_info("Zip file %s..." % destfile)
            destZip.write(eachfile, destfile)
        destZip.close()
        print ("Zip folder succeed!")



    ### zip files in a directory
    def zip_dir(self,dirname, zipfilename):
        global m_log
        filelist = []
        #Check input ...
        fulldirname = os.path.abspath(dirname)
        fullzipfilename = os.path.abspath(zipfilename)
        m_log.write_info( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
        if not os.path.exists(fulldirname):
            print ("Dir/File %s is not exist, Press any key to quit..." % fulldirname)
            inputStr = raw_input()
            return
        if os.path.isdir(fullzipfilename):
            tmpbasename = os.path.basename(dirname)
            fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))
        if os.path.exists(fullzipfilename):
            print ("%s has already exist, are you sure to modify it ? [Y/N]" % fullzipfilename)
            while 1:
                inputStr = raw_input()
                if inputStr == "N" or inputStr == "n" :
                    return
                else:
                    if inputStr == "Y" or inputStr == "y" :
                        m_log.write_info("Continue to zip files...")
                        break

        #Get file(s) to zip ...
        if os.path.isfile(dirname):
            filelist.append(dirname)
            dirname = os.path.dirname(dirname)
        else:
            #get all file in directory
            for root, dirlist, files in os.walk(dirname):
                for filename in files:
                    filelist.append(os.path.join(root,filename))

        #Start to zip file ...
        destZip = zipfile.ZipFile(fullzipfilename, "w")
        for eachfile in filelist:
            destfile = eachfile[len(dirname):]
            m_log.write_info("Zip file %s..." % destfile)
            destZip.write(eachfile, destfile)
        destZip.close()
        print ("Zip folder succeed!")
