"""This script can backup either one file or one directory

attention:
U can only provide an relative path,but the script will use an abspath to perform backup!
So,when you extract the backups back to files,you may got a very long path!Don't be annoyed!
Re-organizing them patiently as you wish!
bugs:
1.If the latest incremental backup in this week is lost,then,before
the next full-backup,there may be a data-lost!
2.There is no exception catch for "no privilege operate a file or directory"
"""
import sys
import os
import shutil
import tarfile
import hashlib
import time
from datetime import datetime, timedelta

MONSTR = (datetime.now() - timedelta(days=time.localtime().tm_wday)).strftime("%Y%m%d")
NOWSTR = datetime.now().strftime("%Y%m%d")
# PREBACKUP = os.path.abspath(sys.argv[1].strip()).replace('\\', '/')
# BACKUPDIR = os.path.abspath(sys.argv[2].strip()).replace('\\', '/')
PREBACKUP = os.path.abspath("test_tar".strip()).replace('\\', '/')
BACKUPDIR = os.path.abspath("backup".strip()).replace('\\', '/')


def ls_r(pdir):
    """
    Recursive lookup the directory and pick out all files,exclude the directories and links!
    :param pdir: A directory's path,either abs or relative
    :return: a list of all files in this directory
    """
    fullpath = []
    if not os.path.isdir(pdir):
        if os.path.isfile(pdir):
            fullpath.append(pdir)
            return fullpath
    for dpath, folders, files in os.walk(pdir):
        # if there isn't any link file,can do this step like ---> fullpath=[fpath + "/" +i for i in files]
        for i in files:
            filepath = dpath + "/" + i
            if os.path.isfile(filepath):
                fullpath.append(os.path.abspath(filepath).replace('\\', '/'))
    return fullpath


def md5sum(pfile):
    """
    compute the md5 checksum for specified file
    :param pfile: The file is needed to be generated the md5 checksum!
    :return: The md5sum for contents of the file
    """
    if not os.path.isfile(pfile):
        print("\033[41;1mThis is not a file!\033[0m")
        return "FAIL"
    with open(pfile, "rb") as f1:
        checksum_md5 = hashlib.md5()
        while 1:
            data = f1.read(4096)
            if not data:
                break
            checksum_md5.update(data)
        return checksum_md5.hexdigest()


def md5file(bkdir, pdir, md5fname):
    """
    Generating a file like following form:
    file's abspath,md5sum

    :param bkdir:The directory for backups
    :param pdir: The directory or file needs to be backuped
    :param md5fname: Specify a name for md5file
    :return: the abspath of generated md5file
    """
    with open("%s/%s" % (bkdir, md5fname), "w", encoding="utf-8") as f1:
        for i in ls_r(pdir):
            f1.write(i + "," + md5sum(i) + "\n")
    return os.path.abspath("backup/%s" % md5fname)


def fullbackup(bkdir, pdir):
    """
    function for full-backup
    :param bkdir:
    :param pdir:
    :return:
    """
    fullbk = tarfile.open("%s/%s_full_%s.tar.gz" % (bkdir, pdir.split('/')[-1], MONSTR), "w:gz")
    fullbk.add(pdir)
    fullbk.close()
    # md5file(pdir,"md5_%s.txt" % MONSTR)
    md5fname = "%s_md5file.md5c" % pdir.split('/')[-1]
    md5file(bkdir, pdir, md5fname)
    return "Full Backup SUCCESS!"


def incrbackup(bkdir, pdir):
    """
    function for incre-backup
    :param bkdir:
    :param pdir:
    :return:
    """
    oldf = "%s/%s_md5file.md5c" % (bkdir, pdir.split('/')[-1])
    newf = "%s/%s_md5_%s.md5c" % (bkdir, pdir.split('/')[-1], NOWSTR)
    md5file(bkdir, pdir, "md5_%s.md5c" % NOWSTR)
    with open(oldf, "r", encoding="utf-8") as f1:
        with open(newf, "r", encoding="utf-8") as f2:
            incrlist = list(set(f2.readlines()) - set(f1.readlines()))
    if incrlist:
        incrbk = tarfile.open("%s/%s_incr_%s.tar.gz" % (bkdir, pdir.split('/')[-1], NOWSTR), "w:gz")
        for i in incrlist:
            incrbk.add(i.split(",")[0])
        incrbk.close()
        shutil.move(newf, oldf)
    else:
        os.remove(newf)
        return "No file changes!"
    return "Incremental backup SUCCESS!"


def backup_everyday(bkdir, pdir):
    """
    Function for determing whether performing a full-backup or a incre-backup
    :param bkdir:
    :param pdir:
    :return:
    """
    md5fname = "%s/%s_md5file.md5c" % (bkdir, pdir.split('/')[-1])

    #The bkdir and pdir must be exists!
    if not os.path.exists(bkdir):
        return "\033[31;1mPlease enter an exists directory for backup!\033[0m"
    elif not os.path.exists(pdir):
        return "\033[31;1mPlease enter an exists directory or file to backup!\033[0m"
    if datetime.now().weekday() == 0:
        print(fullbackup(pdir))
    else:
        if not os.path.exists("%s/%s_full_%s.tar.gz" % (bkdir, pdir.split('/')[-1], MONSTR)):
            print("Full backup of this week has lost!Backup full again:", end=" ")
            print(fullbackup(bkdir, pdir))
        # If md5file has been removed,then,for safe,re-backup full again
        elif not os.path.exists(md5fname):
            print("Md5file of this week has lost!Backup full again:", end=" ")
            print(fullbackup(bkdir, pdir))
        else:
            print(incrbackup(bkdir, pdir))
    return "BACKUP COMPLETE!"


if __name__ == '__main__':
    print(backup_everyday(BACKUPDIR, PREBACKUP))
