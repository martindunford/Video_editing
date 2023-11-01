#! /usr/local/bin/python3

import sys
import os
import requests as r
import wget
import argparse
from setup_logger import *


def main():
    from datetime import datetime
from tqdm import tqdm
import requests
import re
import os

banner = r'''
  ___ ___  __   ___    _           ___                  _              _         
 | __| _ ) \ \ / (_)__| |___ ___  |   \ _____ __ ___ _ | |___  __ _ __| |___ _ _ 
 | _|| _ \  \ V /| / _` / -_) _ \ | |) / _ \ V  V / ' \| / _ \/ _` / _` / -_) '_|
 |_| |___/   \_/ |_\__,_\___\___/ |___/\___/\_/\_/|_||_|_\___/\__,_\__,_\___|_|  
                                                            [Sameera Madushan]
'''

print(banner)


def download_video(quality):
    """Download the video in HD or SD quality"""
    print(f"\nDownloading the video in {quality} quality... \n")
    video_url = re.search(rf'{quality.lower()}_src:"(.+?)"', html).group(1)
    file_size_request = requests.get(video_url, stream=True)
    file_size = int(file_size_request.headers['Content-Length'])
    block_size = 1024
    filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
    t = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
    with open(filename + '.mp4', 'wb') as f:
        for data in file_size_request.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    print("\nVideo downloaded successfully.")

def doit(qlist):
    try:
        if len(qlist) == 2:
            if 0 in qlist and 1 in qlist:
                _input_1 = str(input("\nPress 'A' to download the video in HD quality.\nPress 'B' to download the video in SD quality.\n: ")).upper()
                if _input_1 == 'A':
                    download_video("HD")

                if _input_1 == 'B':
                    download_video("SD")

        if len(qlist) == 2:
            if 1 in qlist and 2 in qlist:
                _input_2 = str(input("\nOops! The video is not available in HD quality. Would you like to download it? ('Y' or 'N'): ")).upper()
                if _input_2 == 'Y':
                    download_video("SD")
                if _input_2 == 'N':
                    exit()

        if len(qlist) == 2:
            if 0 in qlist and 3 in qlist:
                _input_2 = str(input("\nOops! The video is not available in SD quality. Would you like to download it? ('Y' or 'N'): \n")).upper()
                if _input_2 == 'Y':
                    download_video("HD")
                if _input_2 == 'N':
                    exit()
    except(KeyboardInterrupt):
        print("\nProgramme Interrupted")

def main():
    try:
        while True:
            url = input("\nEnter the URL of Facebook video: ")
            x = re.match(r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', url)

            if x:
                html = requests.get(url).content.decode('utf-8')
                open('dunf.html','w+').write(html)
            else:
                print("\nNot related with Facebook domain.")
                exit()

            _qualityhd = re.search('hd_src:"https', html)
            _qualitysd = re.search('sd_src:"https', html)
            _hd = re.search('hd_src:null', html)
            _sd = re.search('sd_src:null', html)

            qlist = []
            _thelist = [_qualityhd, _qualitysd, _hd, _sd]
            for id,val in enumerate(_thelist):
                if val != None:
                    qlist.append(id)

            print (qlist)
            doit(qlist)
            again = input("\nWanna download another video? (Y or N): ").upper()
            if again == str("Y"):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner)
                continue
            else:
                break

    except KeyboardInterrupt:
        print("\nProgramme Interrupted")


def main_old():
    parser = argparse.ArgumentParser(description='This does cool stuff man!')

    parser.add_argument('--debug', action="store_true", help='Run in debug mode')

    parser.add_argument('-U','--ut_plsql_testrun', nargs='?', const='all',
                        help='0 or 1 parmeter, defaults to "all" if 0')

    args = parser.parse_args()
    if args.debug:
        coloredlogs.set_level('DEBUG1')


    filedir = os.path.expanduser('~/Downloads')
    try:
        LINK = "https://www.facebook.com/hoteldoolin.ireland/videos/365623505477343"
        html = r.get(LINK)
    except r.ConnectionError as e:
        logger.info("Error in connecting")
    except r.Timeout as e:
        logger.info("Timeout")
    except r.RequestException as e:
        logger.info("Invalid URL")
    except (KeyboardInterrupt, SystemExit):
        logger.info("System has quit")
        sys.exit(1)
    except TypeError:
        logger.info("Video seems to be private ")
    else:
        logger.info("\n")
        logger.info("Video Quality:Normal " )
        logger.info("[+] Starting Download")
        wget.download(LINK,filedir)
        logger.info("\n")
        logger.info("Video downloaded")



if __name__ == '__main__':
    main()
