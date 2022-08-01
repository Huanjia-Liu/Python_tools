from urllib.request import urlopen
from urllib.request import urlretrieve
import time
import urllib
from lxml import etree
import pymysql

class PictureSpider:

    start_url = "https://hdwallpapers.in"
    path = "/home/loserleo/Pictures/background"

    def get_pictures(self,url):
        response = urlopen(url).read()
        selector = etree.HTML(response)
        links = selector.xpath("//*[@class='wall']/div/a/@href")
        for link in links:
            html = self.start_url+link
            self.html_detail(html)

    def html_detail(self,url):
        response = urlopen(url).read()
        selector = etree.HTML(response)
        link = selector.xpath("//*[@class='overview']/a/@href")
        link = self.start_url+link[0]
        self.download_picture(link)

    def download_picture(self,imageLink):
        imageName = imageLink[32:]
        print("processing files %s"%imageName[1:])
        path = self.path+imageName
        try:
            urlretrieve(imageLink,path)
            time.sleep(1)
        except:
            print("error picture")


    def check_msq(self,string_name):
        db = pymysql.connect("localhost","root","liuhuanjia@.","picture")
        cursor = db.cursor()
        sql = "INSERT INTO background (id, picture_name) VALUES (%s, %s)"

        print(cursor.execute("SELECT MAX(id) FROM `background`;"))
        data = cursor.fetchone()
        print ("Database version: %s" % data)
        db.close()


myspider = PictureSpider()
#print(myspider.start_url)
#myspider.get_pictures(myspider.start_url)
myspider.check_msq("asdfadf")