import os
import zipfile
import sys
import time
import shutil


###zip masterdata
def zip_masterdata():
    print(" ----------- begin exec zip_masterdata ------------ ")
    # curdir = str.format("current dir:%s" % (os.getcwd()))
    # print(curdir)

    # config dirs
    srcdir = r"d:\ftpfiles\rt02\cvs"
    desdir = r"d:\ftpfiles\rt02\cvs_download"
    bakdir = r"d:\ftpfiles\rt02\cvs_bak\\" + time.strftime('%Y%m%d',time.localtime(time.time()))

    # validate src & des dir
    if os.path.exists(srcdir) == False:
        print(str.format("dir %s not exist!" % srcdir))
        return

    if os.path.exists(desdir) == False:
        print(str.format("dir %s not exist!" % desdir))
        return

    subsrcdirs = os.listdir(srcdir)


    # copy files for each dir
    for dir in subsrcdirs:

        src_subdir = srcdir + "\\" + dir
        des_subdir = desdir + "\\" + dir
        print("src sub dir: %s --> des sub dir: %s" % (src_subdir,des_subdir))

        # create des dirs if not exist
        if os.path.exists(des_subdir) == False:
            os.mkdir(des_subdir)
            print("des dir:" + des_subdir + " created.")

        # zip files in src dirs
        zipfile_name = "RT02_" + dir + "_" + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+".zip"
        zipfile_fullname = src_subdir + "\\" + zipfile_name
        print("zipfilename:" + zipfile_fullname)
        filelist = get_filelist(src_subdir,"xml")
        zip_dirfiles(src_subdir, filelist, zipfile_fullname)

        # move zip file to des directory
        tmp_zipfilename = des_subdir + "\\" + zipfile_name.replace(".zip","._")
        des_zipfilename = des_subdir + "\\" + zipfile_name

        shutil.copyfile(zipfile_fullname,tmp_zipfilename)
        os.rename(tmp_zipfilename,des_zipfilename)

        # delete src zip file
        os.remove(zipfile_fullname)

        # backup src files
        bak_subdir = bakdir + "\\" + dir
        if os.path.exists(bak_subdir) == False:
            os.makedirs(bak_subdir)
        for filename in filelist:
            bak_filename = bakdir + "\\" + dir + "\\" + os.path.basename(filename)
            shutil.move(filename,bak_filename)


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
