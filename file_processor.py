import os
import zipfile
import time
import shutil
import logger

### process file operations
class file_processor:

    LOG = None

    def __init__(self, task_name):
        global LOG
        LOG = logger.logger(task_name)


    ### zip files in specific dictory
    def process_zip_dir(self, src_dir, des_dir_base, des_dir_list, bak_dir, zipfile_header):
        global LOG
        LOG.write_info("start process_zip_dir srcdir:%s --> des_dir_base:%s " % (src_dir, des_dir_base))

        # validate src & des dir
        if not os.path.exists(src_dir):
            LOG.write_info("src dir %s not exist!" % src_dir)
            return

        filelist = self.__get_filelist(src_dir, ".xml")
        LOG.write_info("file count in dir %s: %d" % (src_dir, len(filelist)))
        if len(filelist) == 0:
            return

        # zip files in src dirs
        src_dir_name = os.path.basename(src_dir)
        zipfile_name = zipfile_header + "_" + src_dir_name + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))+".zip"
        zipfile_fullname = src_dir + "/" + zipfile_name
        LOG.write_info("zipfilename:" + zipfile_fullname)
        self.__zip_dirfiles(src_dir, filelist, zipfile_fullname)

        # copy to all des sub dirs
        for cur_desdir in des_dir_list:
            # create des dirs if not exist
            if not os.path.exists(des_dir_base + "/" +cur_desdir):
                os.mkdir(des_dir_base + "/" +cur_desdir)
                LOG.write_info("des dir:" + des_dir_base + "/" +cur_desdir + " created.")

            tmp_zipfilename = des_dir_base + "/" +cur_desdir + "/" + zipfile_name.replace(".zip", "._")
            des_zipfilename = des_dir_base + "/" +cur_desdir + "/" + zipfile_name
            shutil.copyfile(zipfile_fullname, tmp_zipfilename)
            os.rename(tmp_zipfilename, des_zipfilename)

        # delete src zip file
        os.remove(zipfile_fullname)

        # backup src files
        if not os.path.exists(bak_dir):
            os.makedirs(bak_dir)
        for filename in filelist:
            bak_filename = bak_dir + "/" + os.path.basename(filename)
            shutil.move(filename, bak_filename)

        LOG.write_info("complete process_zip_dir srcdir:%s --> des_dir_base:%s " % (src_dir, des_dir_base))

    ### unzip files in specific dictory
    def process_unzip_dir(self, src_dir, des_dir, bak_dir):
        global LOG
        LOG.write_info("start process_unzip_dir srcdir:%s --> des_dir_base:%s " % (src_dir, des_dir))

        # validate src & des dir
        if not os.path.exists(src_dir):
            LOG.write_info("src dir %s not exist!" % src_dir)
            return
        if not os.path.exists(des_dir):
            LOG.write_info("des dir %s not exist!" % des_dir)
            return

        zipfilelist = self.__get_filelist(src_dir, ".zip")
        LOG.write_info("zipfile count in dir %s: %d" % (src_dir, len(zipfilelist)))
        if len(zipfilelist) == 0:
            return

        for zipfilename in zipfilelist:
            # unzip files
            self.__unzip_dir(zipfilename,des_dir )
            # bak zip file
            if not os.path.exists(bak_dir):
                os.makedirs(bak_dir)
            bak_zipfilename = bak_dir + "/" + os.path.basename(zipfilename)
            shutil.move(zipfilename, bak_zipfilename)

        LOG.write_info("complete process_unzip_dir srcdir:%s --> des_dir_base:%s " % (src_dir, des_dir))



    ### get file list in a directory
    def __get_filelist(self, dirname, fileext):
        global LOG
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
    def __zip_dirfiles(self,dirname,filelist, zipfilename):
        global LOG
        #filelist = []
        #Check input ...
        if len(filelist) == 0:
            return
        fulldirname = os.path.abspath(dirname)
        fullzipfilename = os.path.abspath(zipfilename)
        LOG.write_info( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
        if not os.path.exists(fulldirname):
            LOG.write_error("Dir/File %s is not exist, Press any key to quit..." % fulldirname)
            inputStr = raw_input()
            return
        if os.path.isdir(fullzipfilename):
            tmpbasename = os.path.basename(dirname)
            fullzipfilename = os.path.normpath(os.path.join(fullzipfilename, tmpbasename))

        '''
        #if os.path.exists(fullzipfilename):
            LOG.write_error("%s has already exist, are you sure to modify it ? [Y/N]" % fullzipfilename)
            while 1:
                inputStr = raw_input()
                if inputStr == "N" or inputStr == "n" :
                    return
                else:
                    if inputStr == "Y" or inputStr == "y" :
                        LOG.write_info("Continue to zip files...")
                        break
            '''


        #Start to zip file ...
        destZip = zipfile.ZipFile(fullzipfilename, "w")
        for eachfile in filelist:
            destfile = eachfile[len(dirname):]
            LOG.write_info("Zip file %s..." % destfile)
            destZip.write(eachfile, destfile)
        destZip.close()
        LOG.write_info("Zip folder succeed!")


    ### unzip file
    def __unzip_dir(self,zipfilename, unzipdirname):
        fullzipfilename = os.path.abspath(zipfilename)
        fullunzipdirname = os.path.abspath(unzipdirname)
        LOG.write_info("Start to unzip file %s to folder %s ..." % (zipfilename, unzipdirname))
        #Check input ...
        if not os.path.exists(fullzipfilename):
            LOG.write_error("zipfile %s is not exist" % fullzipfilename)
            return
        if not os.path.exists(fullunzipdirname):
            os.mkdir(fullunzipdirname)
        else:
            if os.path.isfile(fullunzipdirname):
                # print "File %s is exist, are you sure to delet it first ? [Y/N]" % fullunzipdirname
                LOG.write_info("File %s is exist,delete it " % fullunzipdirname)
                os.remove(fullunzipdirname)

        #Start extract files ...
        srcZip = zipfile.ZipFile(fullzipfilename, "r")
        for eachfile in srcZip.namelist():
            LOG.write_info("Unzip file %s ..." % eachfile)
            eachfilename = os.path.normpath(os.path.join(fullunzipdirname, os.path.basename(eachfile)))
            tmpfilename = os.path.splitext(eachfilename)[0]+"._"
            eachdirname = os.path.dirname(eachfilename)
            if not os.path.exists(eachdirname):
                os.makedirs(eachdirname)
            fd=open(tmpfilename, "wb")
            fd.write(srcZip.read(eachfile))
            fd.close()
            if os.path.exists(eachfilename):
                os.remove(eachfilename)
            os.rename(tmpfilename, eachfilename)
        srcZip.close()

        LOG.write_info("complete unzip file %s" % zipfilename)


    '''
    ### zip files in a directory
    def __zip_dir(self,dirname, zipfilename):
        global LOG
        filelist = []
        #Check input ...
        fulldirname = os.path.abspath(dirname)
        fullzipfilename = os.path.abspath(zipfilename)
        LOG.write_info( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
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
                        LOG.write_info("Continue to zip files...")
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
            LOG.write_info("Zip file %s..." % destfile)
            destZip.write(eachfile, destfile)
        destZip.close()
        print ("Zip folder succeed!")
    '''