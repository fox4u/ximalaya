
import sys

from album import handleAlbum

if __name__ == '__main__':
    try:
        albumId = sys.argv[1]
        handleAlbum(albumId)
    except Exception as e:
        print(sys.argv)
        print(e)