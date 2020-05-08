import urllib.request
import ssl
import os
from bs4 import BeautifulSoup # for HTML parsing

def create_theater_dir(theater_name):
    if not os.path.exists(theater_name):
        os.makedirs(theater_name)

def download_images_from_url(theater_name, url):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    html = response.read()
    soup = BeautifulSoup(html, features="html.parser")

    imgTags = soup.findAll('img', {"class": "grid_image"})
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        if imgUrl.lower().endswith('.jpg'):
            imgData = urllib.request.urlopen(imgUrl, context=context).read()
            filename = theater_name + '/' + imgUrl.split('/')[-1]
            output = open(filename,'wb')
            output.write(imgData)
            output.close()
            print("> downloaded:", imgUrl)

venue_name = 'WalterKerrTheatre'
create_theater_dir(venue_name)

venue = 'Walter+Kerr+Theatre'
page_num = 1
url = "https://aviewfrommyseat.com/venue/{venue}/?page={page_num}".format(venue = venue, page_num=page_num)
download_images_from_url(venue_name, url)
