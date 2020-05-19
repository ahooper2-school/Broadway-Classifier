import urllib.request
import ssl
import os
from bs4 import BeautifulSoup # for HTML parsing

def create_theater_dir(theater_name):
    '''Create a directory for the theater images'''
    if not os.path.exists(theater_name):
        os.makedirs(theater_name)

def download_images_from_url(dir_name, url):
    '''Download all images from the specified page'''
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")

    imgTags = soup.findAll('img', {"class": "grid_image"})
    num_downloaded = 0
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        if imgUrl.lower().endswith('.jpg'):
            imgData = urllib.request.urlopen(imgUrl, context=context).read()
            filename = dir_name + '/' + imgUrl.split('/')[-1]
            output = open(filename,'wb')
            output.write(imgData)
            output.close()
            num_downloaded += 1
    return num_downloaded

def download_img_for_theater(theater_name):
    '''Dowload all images for the specified theater'''
    dir_name = theater_name.replace(" ", "")
    url_theater_name = urllib.parse.quote(theater_name)
    create_theater_dir(dir_name)

    downloaded_images_from_page = True
    page_num = 1
    while(downloaded_images_from_page):
        url = "https://aviewfrommyseat.com/venue/{venue}/?page={page_num}".format(venue = url_theater_name, page_num=page_num)
        print(">>> downloading page:", page_num)
        num_downloaded = download_images_from_url(dir_name, url)
        downloaded_images_from_page = num_downloaded > 0
        page_num += 1

theaters = open(os.path.abspath("../data/theaters.txt")).read().split('\n')

for theater in theaters:
    if len(theater) > 1:
        print("downloading for:", theater)
        download_img_for_theater(theater)
