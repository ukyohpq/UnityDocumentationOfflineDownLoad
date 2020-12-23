import string
import os
import urllib
import shutil
import threading
import time

url = "https://docs.unity3d.com/{0}/{1}"
lan = "cn"
version = "2020.2"
url = string.Formatter().format(url, lan, version)
print(url)

numTotal = 0
loadedLock = threading.RLock()
numDownloaded = 0


def downloadFile(remoteUrl:string, localUrl:string, fullPath:string):
    try:
        urllib.request.urlretrieve(remoteUrl, localUrl)
        print("download:" + localUrl)
    except Exception:
        shutil.copy(fullPath, localUrl)
        print("copy2:" + localUrl)
    global numDownloaded
    loadedLock.acquire()
    numDownloaded = numDownloaded + 1
    print("numDownloaded:{0}  numTotal:{1}".format(numDownloaded, numTotal))
    loadedLock.release()

def checkDir(path):
    list = os.listdir(path)
    for k in list:
        fullPath = path + "/" + k
        # print(fullPath)
        if os.path.isdir(fullPath):
            try:
                newPath = fullPath.replace("assets/en", "assets/" + lan)
                os.makedirs(newPath)
            except Exception:
                pass
            checkDir(path + "/" + k)
        else:
            localUrl = fullPath.replace("assets/en", "assets/" + lan)

            if os.path.exists(localUrl) and os.path.getsize(localUrl) > 0 :
                # print("exist:" + localUrl)
                continue
            suffix4 = fullPath[-4:]
            if suffix4 == ".zip" or suffix4 == ".pdf" or suffix4 == ".png" or suffix4 == ".jpg" or suffix4 == ".gif":
                # print(fullPath, localUrl)
                print("copy1:" + localUrl)
                # t = threading.Thread(target=shutil.copy, args=(fullPath, localUrl))
                # t.start()
                shutil.copy(fullPath, localUrl)
            else:
                remoteUrl = url + fullPath.replace("assets/en", "")
                global numTotal
                numTotal = numTotal + 1
                t = threading.Thread(target=downloadFile, args=(remoteUrl, localUrl, fullPath))
                t.start()
                # try:
                #     remoteUrl = url + fullPath.replace("assets/en", "")
                #     urllib.request.urlretrieve(remoteUrl, localUrl)
                #     print("download:" + localUrl)
                #     # pass
                # except Exception:
                #     # pass
                #     shutil.copy(fullPath, localUrl)
                #     print("copy2:" + localUrl)


checkDir("assets/en")
# while numDownloaded < numTotal:
#     print("numDownloaded:{0}  numTotal:{1}".format(numDownloaded, numTotal))
#     time.sleep(1)
print("download over.")

