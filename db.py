import sqlite3

conn = sqlite3.connect('ximalaya.db')

c = conn.cursor()

def getLastTrackIdx(albumId : str):
    c.execute("select max(trackIndex) from track where albumId = '%s'" % albumId)
    res = c.fetchone()
    return 0 if res == None or res[0] == None else res[0]


def updateTrackInfoList(trackInfoTupleList: list):
    c.executemany('INSERT INTO track(albumId, trackId, trackIndex, title, url) VALUES (?,?,?,?,?)', trackInfoTupleList)
    conn.commit()


def getDownloadList(albumId : str):
    c.execute("select trackIndex, title, url from track where albumId='%s' and done = 0 order by trackIndex asc" % albumId)
    res = c.fetchall()
    return res

def setDownloadDone(albumId : str, trackIndex: int):
    c.execute("update track set done=1 where albumId=%s and trackIndex=%d" % (albumId, trackIndex))
    conn.commit()


