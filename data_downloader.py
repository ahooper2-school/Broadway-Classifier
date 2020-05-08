import urllib.request
import ssl
import os
from bs4 import BeautifulSoup # for HTML parsing

def create_theater_dir(theater_name):
    '''Create a directory for the theater images'''
    if not os.path.exists(theater_name):
        os.makedirs(theater_name)

def download_images_from_url(dir_name, url):
    '''Download all images from hte specified page'''
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")

    imgTags = soup.findAll('img', {"class": "grid_image"})
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        if imgUrl.lower().endswith('.jpg'):
            imgData = urllib.request.urlopen(imgUrl, context=context).read()
            filename = dir_name + '/' + imgUrl.split('/')[-1]
            output = open(filename,'wb')
            output.write(imgData)
            output.close()
            print("> downloaded:", imgUrl)

def download_img_for_theater(theater_name):
    '''Dowload all images for the specified theater'''
    dir_name = theater_name.replace(" ", "")
    url_theater_name = theater_name.replace(" ", "+")
    create_theater_dir(dir_name)
    page_num = 1
    url = "https://aviewfrommyseat.com/venue/{venue}/?page={page_num}".format(venue = url_theater_name, page_num=page_num)
    download_images_from_url(dir_name, url)

theater_name = "Walter Kerr Theatre"
download_img_for_theater(theater_name)
