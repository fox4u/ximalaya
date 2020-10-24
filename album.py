import requests, wget, os
from time import sleep
from db import getLastTrackIdx, updateTrackInfoList, getDownloadList, setDownloadDone, isTrackExist

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
    index = lastTrackIdx
    trackHandleCount = 0
    allTrackList = []
    while True:
        res = requests.get(trackListUrl%(albumId, pageNum), headers=headers)

        if res.status_code == 200 and res.headers['content-type'] == 'application/json':
            resData = res.json()
            if pageNum == 1:
                trackTotalCount = resData['data']['trackTotalCount']
                print('trackTotalCount:', trackTotalCount)
            
            trackList = resData['data']['tracks']
            if isinstance(trackList, list) and len(trackList) > 0:
                for track in trackList:
                    trackId = track['trackId']
                    trackTotalCount = trackTotalCount + 1
                    if not isTrackExist(albumId, trackId):
                        item = {
                            'albumId': albumId,
                            'trackId': trackId, 
                            'title': track['title']
                        }
                        # print(item)
                        allTrackList.insert(0, item)
            else:
                break
        else:
            break

        if trackTotalCount >= trackTotalCount:
            break
        
        pageNum = pageNum + 1
        sleep(1)
    
    for item in allTrackList:
        index = index + 1
        item['index'] = index

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
