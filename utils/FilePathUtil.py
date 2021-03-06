#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/5/16 14:36
'''
import os
import shutil


currentFile = os.getcwd()
proDir = currentFile[:currentFile.find("mitmproxy_client") + len("mitmproxy_client")]


def getProjectRootDir():
    return proDir


def get_full_dir(path, *paths):
    return os.path.join(proDir, path, *paths)


def move_files_by_time(source, destination, start, end):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)
    files = []
    if os.path.isdir(source):
        lists = os.listdir(source)
        for fn in lists:
            timestrap = str(fn).split('.')[0]
            suffix = fn.split('.')[1]
            replace = timestrap.replace('mmexport', '')
            getmtime = int(replace)
            if start <= getmtime <= end:
                sourcefile = os.path.join(source, fn)
                files.append(sourcefile)
                name = f'{getmtime}.{suffix}'
                # print(f"【move_files_by_time().={name}】")
                desfile = os.path.join(destination, name)
                shutil.copyfile(sourcefile, desfile)
                # Logger.println(f"【move_files_by_time().sourcefile={sourcefile}】")
                # Logger.println(f"【move_files_by_time().desfile={desfile}】")
        return files
    else:
        return files


def get_files_by_dir(source):
    files = []
    if os.path.isdir(source):
        lists = os.listdir(source)
        for fn in lists:
            sourcefile = os.path.join(source, fn)
            files.append(sourcefile)
        # Logger.println(f"【get_files_by_dir().files={files}】")
        return files
    else:
        return files


def get_lastmodify_file(test_report, reverse=False):
    if os.path.isdir(test_report):
        lists = os.listdir(test_report)
        lists.sort(key=lambda fn: os.path.getmtime(test_report + os.path.sep + fn), reverse=reverse)
        if len(lists) > 0:
            return get_lastmodify_file(os.path.join(test_report, lists[-1]), reverse=reverse)
        else:
            return test_report
    else:
        return test_report

# 打开文件夹
def startfile(filename):
    try:
        os.startfile(filename)
    except:
        os.subprocess.Popen(['xdg-open', filename])




if __name__ == '__main__':
    full_dir = get_full_dir('wxfriend', 'pic', 'WeiXin')
    des_dir = get_full_dir('wxfriend', 'pic', 'WeiXinCopy','content_md5')
    move_files_by_time(full_dir, des_dir, int('1607509768864'), int('1607509790533'))
    full_dir = get_full_dir('wxfriend', 'pic', 'WeiXinCopy', '1be904df39b2fc933fd71c24a06caac9')
    get_files_by_dir(full_dir)