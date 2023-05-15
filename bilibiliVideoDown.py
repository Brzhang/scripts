# *** author:Brook zhang
# !/usr/bin/python
# -*- coding: utf-8 -*-
# use: python bilibiliVideoDown.py url [count]
import os
import sys
import re
import random
import requests
import json
from tqdm import tqdm

class BilibiliDownloader():
    def __init__(self, s_url, dst_path):
        self.url = s_url
        self.dst_path = dst_path
        self.header = {
            'Range': 'bytes=0-',
            'referer': self.url,
            'origin': 'https://www.bilibili.com/',
            'cookie':''
        }

    def Bl_download(self):
        html = requests.get(self.url, headers=self.header).text
        json_data = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        video_name = re.findall('<title.*?>(.*?)</title>', html)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        '''if len(str(video_name)) > 20:
            video_name = video_name[:20]'''
        video_name = re.sub('[\s]', '', video_name)
        video_name = re.sub('^.', '', video_name)
        video_name = re.sub('/', '', video_name)
        video = json.loads(json_data)['data']['dash']['video'][0]['baseUrl']
        self.download(video, self.dst_path+video_name+'.flv')
        print("[bilibili]: {} video download completed.".format(video_name))
        audio = json.loads(json_data)['data']['dash']['audio'][0]['baseUrl']
        self.download(audio, self.dst_path + video_name + '.mp3')
        print("[bilibili]: {} audio download completed.".format(video_name))


    def download(self,url,rel_path):
        r = requests.get(url, headers=self.header, stream=True)
        file_size = int(r.headers['content-length'])
        
        if os.path.exists(rel_path):
            first_byte = os.path.getsize(rel_path)  # (3)
        else:
            first_byte = 0
        if first_byte >= file_size: # (4)
            return True

        #header = {"Range": f"bytes={first_byte}-{file_size}"}
        
        size = 0
    
        pbar = tqdm(total=file_size, initial=0, unit='B', unit_scale=True, desc=rel_path)
        with open(rel_path, 'wb')as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    size += len(chunk)
                    f.write(chunk)
                    pbar.update(8192)
        pbar.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You must enter the url')
        exit(1)
    video_url = sys.argv[1]
    if len(sys.argv) > 2:
        video_count = int(sys.argv[2])
    else:
        video_count = 1
    path = './'
    if video_count > 1:
        for i in range(video_count):
            BilibiliDownloader(video_url+'?p='+str(i+1), path).Bl_download()
    else:
        BilibiliDownloader(video_url, path).Bl_download()
