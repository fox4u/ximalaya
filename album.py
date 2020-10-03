import requests, wget, os
from time import sleep
from db import getLastTrackIdx, updateTrackInfoList, getDownloadList, setDownloadDone

trackListUrl = 'https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=%s&pageNum=%d'
trackAudioUrl = 'https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1'
headers = {'user-agent': 'ximalaya/0.0.1'}

DOWNLOADDIR = 'download/'

def handleAlbum(albumId: str):
    allTrackList = getAlbumTrackList(albumId)
    allTrackAudioList = getTrackAudioTupleList(allTrackList)
    print(allTrackAudioList)
    updateTrackInfoList(allTrackAudioList)
    handleDownload(albumId)

def getTrackInfoTupleWithUrl(trackInfo: dict):
    trackId = trackInfo['trackId']

    if trackId != None:
        res = requests.get(trackAudioUrl%(trackId), headers=headers)

        if res.status_code == 200 and res.headers['content-type'] == 'application/json':
            resData = res.json()
            trackInfo['url'] = resData['data']['src'] if resData['data'] and resData['data']['src'] else ''

    print(trackInfo)    
    sleep(2)
    return (trackInfo['albumId'], str(trackInfo['trackId']), trackInfo['index'], trackInfo['title'], trackInfo['url'])

def getTrackAudioTupleList(trackInfoList: list):
    return list(map(getTrackInfoTupleWithUrl, trackInfoList))

def getAlbumTrackList(albumId: str):
    pageNum = 1
    lastTrackIdx = getLastTrackIdx(albumId)    
    allTrackList = []
    while True:
        loopEnd = False
        res = requests.get(trackListUrl%(albumId, pageNum), headers=headers)

        if res.status_code == 200 and res.headers['content-type'] == 'application/json':
            resData = res.json()
            if pageNum == 1:
                trackTotalCount = resData['data']['trackTotalCount']
            
            trackList = resData['data']['tracks']
            if isinstance(trackList, list) and len(trackList) > 0:
                for track in trackList:
                    index = track['index']

                    if index <= lastTrackIdx:
                        loopEnd = True
                        break

                    item = {
                        'albumId': albumId,
                        'index': index, 
                        'trackId': track['trackId'], 
                        'title': track['title']
                    }
                    # print(item)
                    allTrackList.append(item)
            else:
                break
        else:
            break

        if loopEnd:
            break

        pageNum = pageNum + 1
        sleep(1)
    
    print(trackTotalCount, len(allTrackList))
    return allTrackList


def handleDownload(albumId: str):
    downloadList = getDownloadList(albumId)
    if len(downloadList) > 0:
        folder = DOWNLOADDIR + albumId
        createDirIfNotExist(folder)
        for item in downloadList:
            filename = folder + '/' + str(item[0]) + '-' + item[1] + '.m4a'
            try:
                print('\ndownloading...' + item[1])
                wget.download(item[2], out=filename)
                setDownloadDone(albumId, item[0])
            except Exception as e:
                print(e)

def createDirIfNotExist(folder: str):
    if not os.path.exists(folder):
        os.makedirs(folder)
