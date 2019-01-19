import argparse
import sys
import os
import urllib.request
from googlesearch import search
from googlesearch import search_images
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable
from urllib.parse import urlparse
import requests
import os.path
import math
from progress.spinner import PixelSpinner
from pySmartDL import SmartDL

movieTable = BeautifulTable()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


parser = argparse.ArgumentParser(description='Download Movie from commandline')
parser.add_argument('-n', action='store', dest='name',
                    help='name of movie', type=str, required='true')
parser.add_argument('-we', action='store', dest='websiteEnter',
                    help='(default is 1) if u choose higher it get slower but chance of finding a link increse', type=int, default=1)
parser.add_argument('-k', action='store', dest='kind',
                    help='movie / series Note:series is unavailble now', type=str, default='movie')
parser.add_argument('-gc', action='store', dest='getcover',
                    help='download cover (default is FALSE)', type=bool, default=0)
parser.add_argument('-q', action='store', dest='quality',
                    help='quality (480/720/1080)', type=str, default='')

argResult = parser.parse_args()
if argResult.kind == "movie":
    searchQuery = "دانلود فیلم"+argResult.name
    imgSearchQuery = "site:imdb.com official cover for movie "+argResult.name
elif argResult.kind == "series":
    searchQuery = "دانلود سریال "+argResult.name
    imgSearchQuery = "site:imdb.com official cover for series "+argResult.name

if argResult.quality:
    argResult.quality += "p"

opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
websitenumber = 1
linkNumber = 1
currentPath = os.path.dirname(os.path.realpath(__file__))
linksDicMovie = {}

movieTable.column_headers = ['id', 'website', 'link', 'space']

spinner = PixelSpinner('Searching ... ')
if argResult.kind == "movie":
    for url in search(searchQuery, num=1, start=0, stop=argResult.websiteEnter, lang='fa', only_standard=True):
        spinner.next()
        websiteUrlDetail = urlparse(url)
        try:
            requestToUrl = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as error:
            print("error : check you connection")

        soup = BeautifulSoup(requestToUrl, 'lxml')
        for link in soup.find_all('a', href=True):
            if link['href'].endswith('.mkv') or link['href'].endswith('.mp4'):
                if argResult.quality in link['href']:
                    dlLinkDetails = requests.get(link['href'], stream=True)
                    dlLinkSpace = int(
                        dlLinkDetails.headers.get('content-length'))
                    movieTable.append_row(
                        [linkNumber, websiteUrlDetail.netloc, link['href'], convert_size(dlLinkSpace)])
                    linksDicMovie.update({linkNumber: link['href']})
                    linkNumber += 1

    #get cover happen
    if argResult.getcover:
        print("")
        for url in search_images(imgSearchQuery, tld='com', lang='en', tbs='0', safe='off', num=1, start=0, stop=1, domains=None, only_standard=False):
            websiteUrlDetail = urlparse(url)
            try:
                requestToUrl = urllib.request.urlopen(url).read()
            except urllib.error.HTTPError as error:
                print("error : check you connection")
            
            soup = BeautifulSoup(requestToUrl,'lxml')
            for link in soup.find_all('img'):
                if link['src'].endswith('.jpg'):
                    print('Downloading cover ... ')
                    obj = SmartDL(link['src'],currentPath)
                    obj.start()
                    break

    print("")
    if not linksDicMovie:
        print("Nothing found ! Check your spelling and use higher -we .")
    else:
        print(movieTable)
        userSelectedLinkId = int(input("enter link id :"))
        filename = linksDicMovie[userSelectedLinkId].rsplit('/')[-1]
        print("preparing to download : "+linksDicMovie[userSelectedLinkId])
        print("wait a few ... ")
        if os.path.isfile(filename):
            print('file already exist')
        else:
            try:
                # set threads cuse its default is 5 and u have corei5 so it cant download and retrey  and fail
                obj = SmartDL(linksDicMovie[userSelectedLinkId], currentPath,threads=2)
                obj.start()
            except HashFailedException:
                print('💣 error occurred')
                print('hash failed')
                sys.exit()
            except CanceledException:
                print('bye bye ..')
                sys.exit()
            except HTTPError:
                print('server error .. u may use another site next time')
                sys.exit()
            except URLError:
                print('cant reach the url ! ')
                sys.exit()
            except IOError:
                print('Error occurred . Do have enough space?')
                sys.exit()

            dlMoviePath = obj.get_dest()
            if os.path.isfile(dlMoviePath):
                print("🎬 file saved in  "+dlMoviePath)
            else:
                print("something happend in when saveing file")


#
#   Movie Section Ended
#
elif argResult.kind == "series":
    for url in search(searchQuery, stop=20, lang='fa', only_standard=True):
        print(url)


#
#   Series Section Ended
#
else:
    print("error : specify the -k (movie/series)")


# TODO: error when searching for unbreakable
# TODO: download cover subtitle for movie
