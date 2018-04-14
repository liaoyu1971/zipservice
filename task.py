import os
import zipfile
import sys
import time
import shutil


###zip masterdata
def zip_masterdata():
    print(" ----------- begin exec zip_masterdata ------------ ")

    # config
    srcdir = r"d:\ftpfiles\rt02\cvs"
    desdir = r"d:\ftpfiles\rt02\cvs_download"
    bakdir = r"d:\ftpfiles\rt02\cvs_bak\\" + time.strftime('%Y%m%d', time.localtime(time.time()))
    dispatch_dir_list = ["DC10", "DC11"]
    special_src_dir = r"d:\ftpfiles\rt02"
    special_dir_list = ["organization"]


    # validate src & des dir
    if not os.path.exists(srcdir):
        print("src dir %s not exist!" % srcdir)
        return

    if not os.path.exists(desdir):
        print("des dir %s not exist!" % desdir)
        return

    subsrcdirs = os.listdir(srcdir)


    # process files for each store directories
    for cur_dir in subsrcdirs:
        src_subdir = srcdir + "\\" + cur_dir
        des_subdir = desdir + "\\" + cur_dir
        bak_subdir = bakdir + "\\" + cur_dir

        des_subdir_list = []
        if cur_dir in dispatch_dir_list:
            des_subdir_list = os.listdir(desdir)
        else:
            des_subdir_list = [cur_dir]

        process_dir(src_subdir, desdir, des_subdir_list, bak_subdir,'RT02')
        '''

        print("src sub dir: %s --> des sub dir: %s" % (src_subdir, des_subdir))

        filelist = get_filelist(src_subdir, ".xml")
        print("file count in dir %s: %d" % (src_subdir, len(filelist)))
        if len(filelist) == 0:
            continue

        # zip files in src dirs
        zipfile_name = "RT02_" + cur_dir + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))+".zip"
        zipfile_fullname = src_subdir + "\\" + zipfile_name
        print("zipfilename:" + zipfile_fullname)

        zip_dirfiles(src_subdir, filelist, zipfile_fullname)

        # process dispatch dir
        if cur_dir in dispatch_dir_list:
            # copy to all des sub dirs
            subdes_dirs = os.listdir(desdir)
            for cur_desdir in subdes_dirs:
                tmp_zipfilename = desdir + "\\" +cur_desdir + "\\" + zipfile_name.replace(".zip", "._")
                des_zipfilename = desdir + "\\" +cur_desdir + "\\" + zipfile_name
                shutil.copyfile(zipfile_fullname, tmp_zipfilename)
                os.rename(tmp_zipfilename, des_zipfilename)

        else:
            # create des dirs if not exist
            if not os.path.exists(des_subdir):
                os.mkdir(des_subdir)
                print("des dir:" + des_subdir + " created.")

            # move zip file to des directory
            tmp_zipfilename = des_subdir + "\\" + zipfile_name.replace(".zip", "._")
            des_zipfilename = des_subdir + "\\" + zipfile_name

            shutil.copyfile(zipfile_fullname, tmp_zipfilename)
            os.rename(tmp_zipfilename, des_zipfilename)

        # delete src zip file
        os.remove(zipfile_fullname)

        # backup src files
        bak_subdir = bakdir + "\\" + cur_dir
        if not os.path.exists(bak_subdir):
            os.makedirs(bak_subdir)

        for filename in filelist:
            bak_filename = bakdir + "\\" + cur_dir + "\\" + os.path.basename(filename)
            shutil.move(filename, bak_filename)



    '''
    # process files in special directories
    for spe_dir_name in special_dir_list:
        spe_dir_full  = special_src_dir + "\\" + spe_dir_name
        if not os.path.exists(spe_dir_full):
            print("special directory %s not exist!" % spe_dir_full)
            continue

        des_subdir_list = os.listdir(desdir)
        bak_subdir = bakdir + "\\" + spe_dir_name
        process_dir(spe_dir_full, desdir, des_subdir_list, bak_subdir,"RT02")
    return



### process files in specific dictory
def process_dir(src_dir, des_dir_base, des_dir_list, bak_dir, zipfile_header):
    # validate src & des dir
    print("start process_dir srcdir:%s des_dir_base:%s " % (src_dir, des_dir_base))
    if not os.path.exists(src_dir):
        print("src dir %s not exist!" % src_dir)
        return

    filelist = get_filelist(src_dir, ".xml")
    print("file count in dir %s: %d" % (src_dir, len(filelist)))
    if len(filelist) == 0:
        return

    # zip files in src dirs
    src_dir_name = os.path.basename(src_dir)
    zipfile_name = zipfile_header + "_" + src_dir_name + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))+".zip"
    zipfile_fullname = src_dir + "\\" + zipfile_name
    print("zipfilename:" + zipfile_fullname)
    zip_dirfiles(src_dir, filelist, zipfile_fullname)

    # copy to all des sub dirs

    for cur_desdir in des_dir_list:
        # create des dirs if not exist
        if not os.path.exists(des_dir_base + "\\" +cur_desdir):
            os.mkdir(des_dir_base + "\\" +cur_desdir)
            print("des dir:" + des_dir_base + "\\" +cur_desdir + " created.")

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

    print("complete process_dir srcdir:%s des_dir_base:%s " % (src_dir, des_dir_base))

### get file list in a directory
def get_filelist(dirname,fileext):
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
def zip_dirfiles(dirname,filelist, zipfilename):
    #filelist = []
    #Check input ...
    if len(filelist) == 0:
        return
    fulldirname = os.path.abspath(dirname)
    fullzipfilename = os.path.abspath(zipfilename)
    print( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
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
                    print("Continue to zip files...")
                    break

    #Start to zip file ...
    destZip = zipfile.ZipFile(fullzipfilename, "w")
    for eachfile in filelist:
        destfile = eachfile[len(dirname):]
        print("Zip file %s..." % destfile)
        destZip.write(eachfile, destfile)
    destZip.close()
    print ("Zip folder succeed!")



### zip files in a directory
def zip_dir(dirname, zipfilename):
    filelist = []
    #Check input ...
    fulldirname = os.path.abspath(dirname)
    fullzipfilename = os.path.abspath(zipfilename)
    print( "Start to zip %s to %s ..." % (fulldirname, fullzipfilename))
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
                    print("Continue to zip files...")
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
        print("Zip file %s..." % destfile)
        destZip.write(eachfile, destfile)
    destZip.close()
    print ("Zip folder succeed!")





if __name__ == "__main__":
    print('exec task.py')
    zip_masterdata()
