# Ximalaya Downloader

Download all/new tracks in a free album on Ximalaya.

## Dependency
* Python 3
* virtualenv (optional)
## Usage
Windows as an example
* (Optional) create a virtual env
```
virtualenv venv_ximalaya
venv_ximalaya\Scripts\activate
```
* Install modules
```
python -m pip install -r requirements.txt
```
* Initialize sqlite db
```
python initdb.py
```
* Try it with an album id
```
python main.py {albumId}
```




