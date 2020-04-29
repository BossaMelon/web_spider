import threading

import requests


def getSegmentIndex(size, n=10):
    spos = []
    fpos = []
    persize = int(size / n)
    intsize = persize * n
    for i in range(0, intsize, persize):
        spos.append(i)
        fpos.append(i + persize - 1)
    if intsize < size:
        fpos[n - 1] = size

    return spos, fpos


def downloadFile(url, spos, fpos, file):
    try:
        header = {"Range": "bytes=%d-%d" % (spos, fpos)}
        res = requests.get(url, headers=header)
        file.seek(spos)
        file.write(res.content)
    except Exception as e:
        print(e)


def multiThreadDownload(url, file_path, file_size, thread_num=10):
    #     print(file_path)
    #     print(file_path.exists())
    if file_path.exists():
        file_path = file_path.with_name('_' + file_path.name)
    file_path.touch()
    spos, fpos = getSegmentIndex(file_size, thread_num)
    tmp = []
    with open(file_path, 'rb+') as fp:
        for i in range(0, thread_num):
            t = threading.Thread(target=downloadFile, args=(url, spos[i], fpos[i], fp))
            t.setDaemon(True)
            t.start()
            tmp.append(t)
        for i in tmp:
            i.join()
