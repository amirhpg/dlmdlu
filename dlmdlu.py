import argparse
import sys
import os
import urllib.request
from googlesearch import search
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable
from urllib.parse import urlparse
import requests
import os.path
import math
from progress.spinner import LineSpinner


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
parser.add_argument('-k', action='store', dest='kind',
                    help='movie / series Note:series is unavailble now', type=str, default='movie')
parser.add_argument('-q', action='store', dest='quality',
                    help='quality (480/720/1080)', type=str, default='')

argResult = parser.parse_args()
searchQuery = "دانلود فیلم"+argResult.name

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

if argResult.kind == "movie":
    spinner = LineSpinner('Listing Links ')
    for url in search(searchQuery, num=4, start=0, stop=4, lang='fa', only_standard=True):
        spinner.next()
        websiteUrlDetail = urlparse(url)
        websitenumber += 1
        try:
            requestToUrl = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as error:
            print("error : check you connection")

        soup = BeautifulSoup(requestToUrl, 'lxml')
        for link in soup.find_all('a', href=True):
            if link['href'].endswith('.mkv'):
                if argResult.quality in link['href']:
                    dlLinkDetails = requests.get(link['href'], stream=True)
                    dlLinkSpace = int(
                        dlLinkDetails.headers.get('content-length'))
                    movieTable.append_row(
                        [linkNumber, websiteUrlDetail.netloc, link['href'], convert_size(dlLinkSpace)])
                    linksDicMovie.update({linkNumber: link['href']})
                    linkNumber += 1
                    #  TODO: download link  get input now

    print(movieTable)
    userSelectedLinkId = int(input("enter link id :"))
    filename = linksDicMovie[userSelectedLinkId].rsplit('/')[-1]
    print("preparing to download : "+linksDicMovie[userSelectedLinkId])
    print("checking if file already exit")
    if os.path.isfile(filename):
        print('file already exist')
    else:
        print('downloading')


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