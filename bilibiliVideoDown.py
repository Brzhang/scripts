# *** author:Brook zhang
# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import random
import requests
import json

path = './'

class BilibiliDownloader():
    def __init__(self, s_url):
        self.url = s_url
        self.header = {
            'Range': 'bytes=0-',
            'referer': self.url,
            'origin': 'https://www.bilibili.com/',
            # 'cookie':'',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def Bl_download(self):
        html = requests.get(self.url, headers=self.header).text
        json_data = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        video_name=re.findall(',"title":"(.*?)","', html)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video = json.loads(json_data)['data']['dash']['video'][0]['baseUrl']
        self.download(video,path+video_name+'.flv')
        print("[bilibili]: {} video download completed.".format(video_name))
        audio = json.loads(json_data)['data']['dash']['audio'][0]['baseUrl']
        self.download(audio, path + video_name + '.mp3')
        print("[bilibili]: {} audio download completed.".format(video_name))


    def download(self,url,rel_path):
        r = requests.get(url, headers=self.header)
        with open(rel_path, 'wb')as f:
            f.write(r.content)
            print("writing file......")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must enter the url')
        exit(1)
    video_url = sys.argv[1]
    BilibiliDownloader(video_url).Bl_download()
