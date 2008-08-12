import os
import sys
import pycurl


DEBUG = 0

VERSION = '0.1.1'

PANEL_TOP = 0
PANEL_BOT = 1

STAT_Q = 0
STAT_D = 1
STAT_C = 2
STAT_S = 3
STAT_Z = 4
STAT_X = 5
STAT_E = -1


STAT_QUEUEING = 'Queueing'
STAT_DOWNLOADING = 'Downloading'
STAT_DONE = 'Completed'
STAT_COMPLETING = 'Completing'
STAT_STOPPED = 'Stopped'
STAT_EXIST = 'File exists'
STAT_ERROR = 'Error'


downloadStatus = {}
downloadStatus[STAT_Q] = STAT_QUEUEING
downloadStatus[STAT_D] = STAT_DOWNLOADING
downloadStatus[STAT_C] = STAT_COMPLETING
downloadStatus[STAT_S] = STAT_STOPPED
downloadStatus[STAT_E] = STAT_ERROR
downloadStatus[STAT_X] = STAT_EXIST
downloadStatus[STAT_Z] = STAT_DONE


FILEID_COL = 0
FILENAME_COL = 1
FILESTATUS_COL = 2
FILESPEED_COL = 3
FILESIZE_COL = 4
FILECOMP_COL = 5
PERCENT_COL = 6
RETRY_COL = 7
FILEURL_COL = 8
FILEERROR_COL = 9

FILENAME_COL_SIZE = 300
FILESTATUS_COL_SIZE = 130
FILEURL_COL_SIZE = 500
FILEERROR_COL_SIZE = 400



TYPE_FILE = 'F'
TYPE_DIR = 'D'


EXIST = 1
EXIST_R = 2
EXIST_W = 3
NO_EXIST = 0

CONTENT_TYPE = 'Content-Type'
CONTENT_LENGTH = 'Content-Length'
CONTENT_DISPO = 'Content-Disposition'
ACCEPT_RANGE = 'Accept-Ranges'
TEXTHTML = 'text/html'
OCTET = 'application/octet-stream'
SET_COOKIE = 'Set-Cookie:'

RAPIDSHARE = 'rapidshare.com'
RAPIDSHARE_LINK = RAPIDSHARE + '/files/'
RAPIDSHARE_FOLDER = RAPIDSHARE + '/users/'
UNKNOWN_TYPE = 'UNKNOW'

RAPIDSHARE_STYLE = 'font-size: 12pt;'
RAPIDSHARE_TARGET = '_blank'

FOLDER_TMP_NAME = 'RapidShare_Link_List'

HTTP_PRE = 'http://'
HTTPS_PRE = 'https://'

CURRENT_ID = 1

RUNNING_PATH = os.path.realpath(os.path.dirname(sys.argv[0]))
USER_HOME = '~'
USER_DIR = os.path.expanduser(USER_HOME)
LRG_DIR = '.lrg'
CONFIG_DIR = os.path.join(USER_DIR, LRG_DIR)
CONFIG_FILE = os.path.join(CONFIG_DIR, 'lrg.conf')
COOKIE_FILE = os.path.join(CONFIG_DIR, 'lrg.cookies')
QUEUEINGLIST_FILE = os.path.join(CONFIG_DIR, 'queue_lrg.save') 
DOWNLOADEDLIST_FILE = os.path.join(CONFIG_DIR, 'load_lrg.save')
SETTINGS_FILE = os.path.join(CONFIG_DIR, 'settings.save')
DOWNLOAD_DIR = os.path.join(CONFIG_DIR, 'Downloads')
REL_LOGOFILE = os.path.join('gui','images','tux.png')
LOGOFILE = os.path.join(RUNNING_PATH, REL_LOGOFILE)
TMP_DIR = os.path.join(DOWNLOAD_DIR, '.tmp')
TMP_EXT = '.part'

RAPIDSHARE_USERNAME = ''
RAPIDSHARE_PASSWORD = ''

PROXY = False
PROXYADDR = 'http://10.1.200.16'
PROXYPORT = 3128

BLK_SIZE = 1024
CHUNK_SIZE = BLK_SIZE * 32
MAX_CONN_PER_FILE = 3
MAX_CONC_DOWNLOAD = 5
RESUME_SIZE = 0

MAX_CONNECTION_TIMEOUT = 300
MAX_TRANSFER_TIMEOUT = 600
MAX_RETRY = 10

REPORT_SIZE = BLK_SIZE * 16
#REPORT_DELAY = 500 * MAX_CONC_DOWNLOAD
REPORT_DELAY = 1000


CURL_DLFILE = 0
CURL_DLPART = 1

PROXY_HTTP = 'HTTP'
PROXY_SOCKS4 = 'SOCKS4'
PROXY_SOCKS5 = 'SOCKS5'

proxyTypeList = [PROXY_HTTP, PROXY_SOCKS4, PROXY_SOCKS5]

proxyTypeCurlList = {}
proxyTypeCurlList[PROXY_HTTP] = pycurl.PROXYTYPE_HTTP
proxyTypeCurlList[PROXY_SOCKS4] = pycurl.PROXYTYPE_SOCKS4
proxyTypeCurlList[PROXY_SOCKS5] = pycurl.PROXYTYPE_SOCKS5

proxyTypeValueList = {}
proxyTypeValueList[pycurl.PROXYTYPE_HTTP] = PROXY_HTTP
proxyTypeValueList[pycurl.PROXYTYPE_SOCKS4] = PROXY_SOCKS4
proxyTypeValueList[pycurl.PROXYTYPE_SOCKS5] = PROXY_SOCKS5

errorList = []
errorList.append('The file could not be found.  Please check the download link.')
errorList.append('An error has occured')
errorList.append('This file is suspected to contain illegal content and has been blocked.')
errorList.append('Your Premium Account has not been found')
errorList.append('Invalid login')
errorList.append('Invalid password')
errorList.append('The Account has been found, but the password is incorrect.')

E_FILEEXIST_CODE = 0
E_FILEEXIST_MSG = 'Destination file exists'
E_FILEMOVE_CODE = 1


MSG_INVALID_USERNAME = 'Invalid account'
