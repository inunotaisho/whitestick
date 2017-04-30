import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

import os
import io
import time
import csv 
import re
from os.path import basename,splitext
from urlparse import urlsplit
from urllib import urlretrieve
import urlparse
from bs4 import BeautifulSoup
import urllib2

from google.cloud import vision

stringy='alt='
static_img_path='/media/sf_codes/tensorFlow_lastLayer/data'
saved_image_path = '/media/sf_codes/tensorFlow_lastLayer/saved_images'
os.environ["GCLOUD_PROJECT"] = "feisty-card-155322"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/westy/.config/gcloud/application_default_credentials.json'
wiki_url = "http://en.wikipedia.org/wiki/Main_Page"
twitter_url = 'https://twitter.com/search?vertical=default&q=joesphfcox&src=typd'
cityBmore_url ="http://www.baltimorecity.gov/"
hackathon_url = 'https://www.baltimorehackathon.com/'
bmorewiki_url = "https://en.wikipedia.org/wiki/Baltimore"
market_url = "http://www.marketwatch.com/"
# There is a copy of the credentials in the project home dir, linux needs the above path, but to run on another machine 
# then uncomment the following line
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/home/westy/.config/gcloud/application_default_credentials.json'

def scrape_images(url = wiki_url,output_dir=saved_image_path): 
    imageList = []
    print("Scraping images from %s" % url)
    soup = BeautifulSoup(urllib2.urlopen(url),'lxml')
    # for img in soup.select('a.image > img'):
    for img in soup.select('a.image > img'):
        img_url = urlparse.urljoin(url, img['src'])
        file_name = img['src'].split('/')[-1]
        urlretrieve(img_url, output_dir + '/'+ file_name)
        imageList.append(file_name)
    return imageList

def scrape_html(url):
    response = urllib2.urlopen(url)
    html = response.read()
    with open('html/file.html','wb') as f:
        f.write(html)
        f.close()
    return html

def insert_alts(html):
    soup = BeautifulSoup(html)
    for img in soup.findAll('img'):
        img['src'] = 'cid:' + splitext(basename(img['src']))[0]
    my_html_string = str(soup)

def gatherFiles(img_path=static_img_path):
    files = [file for file in os.listdir(saved_image_path) if not file.startswith(".")]
    return files

def detect_text(path):
    """Detects text in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    texts = image.detect_text()
    # print('Texts:')

    # for text in texts:
    #     print('\n"{}"'.format(text.description))

    #     vertices = (['({},{})'.format(bound.x_coordinate, bound.y_coordinate)
    #                 for bound in text.bounds.vertices])

    #     print('bounds: {}'.format(','.join(vertices)))
    return texts

def detect_entity(path):
    """Detects web annotations given an image."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    notes = image.detect_web()

    # if notes.web_entities:
    #     print ('\n{} Web entities found: '.format(len(notes.web_entities)))

    #     for entity in notes.web_entities:
    #         print('Score      : {}'.format(entity.score))
    #         print('Description: {}'.format(entity.description))
    return notes.web_entities

def detect_labels(path):
    """Detects labels in the file."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    labels = image.detect_labels()
    print('Labels:')

    # for label in labels
    return labels

def output(dict):
    for key,value in dict.iteritems():
        print(key,value)

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


if __name__=='__main__':
    # print( "Gathering the images to process from: %s" % bmorewiki_url)
    img_list = scrape_images(url = bmorewiki_url,output_dir = saved_image_path)
    print("%s image(s) were added to the dir %s" %(len(img_list),saved_image_path))
    content = scrape_html(url = bmorewiki_url)
    # print("Raw HTML file was added to html/final.html")

    files = gatherFiles(img_path =saved_image_path)
    # for i in files:
    #     print(i)
    holder = dict.fromkeys(files)
    # print("Detecting text inside the images via Google Vision API")
    # for key,value in holder.iteritems():
    #     #print(key)
    #     txts = detect_text(saved_image_path + '/' + str(key))
    #     #txts = detect_text(r'/media/sf_codes/tensorFlow_lastLayer/saved_images/220px-Race_and_ethnicity_2010-_Baltimore_%285559896701%29.png')
    #     max_length,longest_element = max([(len(x.description),x.description) for x in txts])
    #     holder[key] = [longest_element]
    # print("60 Second speed bump initiated so that this program does not exceed the 1 minute API call quota")
    # time.sleep(60)
    print("Detecting web element type via Google Vision API")
    notes = None
    for key,value in holder.iteritems():
        # print(key)
        while notes is None:
            try:
                notes = detect_entity(saved_image_path + '/' + str(key))
            except:
                pass
        # [print(x.score) for x in notes]
        max_prob, max_element = max([(x.score,x.description) for x in notes])

        # max_prob, max_element = max(notes, key= lambda x.score: x.description)
        # holder[key].append(max_element)
        holder[key] = max_element
        notes = None
    print("60 Second speed bump initiated so that this program does not exceed the 1 minute API call quota")
    time.sleep(60)

    count = 0
    for img in img_list:
        index = findnth(content,stringy,count)
        content = content[:index+len(stringy)+1] + holder[img] + content[index+len(stringy)+1:]
        count+=1
    with open('html/final.html','wb') as f:
        f.write(''.join(content))
        f.close()
    # print("Creating the output file")
    # with open('output/output.csv','wb') as f:
    #     w = csv.DictWriter(f, holder.keys())
    #     w.writeheader()
    #     w.writerow(holder)
    # output(holder)

