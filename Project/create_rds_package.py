from shutil import copy, move
import os
import zipfile
import datetime
import sys
import platform

IsWindows = False
if platform.system() == "Windows":
    IsWindows = True

def rmAll(topName):
    for root, dirs, files in os.walk(topName, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(topName)

def copyAllFile(fpath):
    for file in os.listdir(fpath):
        fp = os.path.join(fpath, file)
        if not os.path.isdir(fp):
            if not (".zip" in file) or file == "scene.zip.default":
                copy(fp, ".")
        elif IsWindows and file != "data" and file != "pdb64" and file != "lib" and file != ".git":
            copyDirFile(fpath, file)
        elif not IsWindows and file != "data" and file != "pdb64" and file != ".git":
            copyDirFile(fpath, file)

def copyDirFile(fpath, fkey):
    os.mkdir(fkey)
    os.chdir(fkey)
    try:
        ppath = os.path.join("../",fpath,fkey)
        copyAllFile(os.path.join("../",fpath,fkey))
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)
    os.chdir("..")

def run(rdshome:str, Version:str):
    cur_dir = os.getcwd()
    print(f"rdshome:{rdshome}")
    os.chdir(rdshome)
    if os.path.exists("data"):
        rmAll("data")

    os.mkdir("data")
    os.chdir("data")
    os.mkdir("rdscore")
    os.chdir("rdscore")

    try:
        copyAllFile("../../")
    except IOError as e:
        print("Unable to copy file. %s" % e)
        exit(1)
    except:
        print("Unexpected error:", sys.exc_info())
        exit(1)

    os.chdir("..")
    os.chdir("..")

    ts = datetime.datetime.now().strftime('%m%d_%H%M%S')
    if IsWindows:
        output_file = f"rdscore-{Version}-windows-{ts}-QS.zip"
    else:
        output_file = f"rdscore-{Version}-linux-{ts}-QS.zip"
    with zipfile.ZipFile(output_file, "w",zipfile.ZIP_DEFLATED) as zipobj:
        for root, dirs, files in os.walk("data", topdown=False):
            for name in files:
                print(os.path.join(root,name))
                zipobj.write(os.path.join(root, name))
    rmAll("data")
    move(output_file, cur_dir)
    print("output: ", output_file)


if __name__ == "__main__":
    Version = "v0.1.9.240426_dyb_test_checkCleanOrderFormat_v1"
    run(r"C:\Core_SDK\windows_0415\0.1.9.240413v2\bin\release\win64", Version)
    # run("G:/SEER/Code/C++/RDSCore_0131_win/0.1.9.240124/bin/release/win64", Version)