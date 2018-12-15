#Crawler for "www.mydala.com"
'''
    Below Code will fetch Offer by, Offer title , Offer description, merchant
    tc*,Validity,Address of seller, Offer Timings,Contact and all these details
    will be saved in result.csv
'''

from __future__ import print_function
import urllib2
import urlparse
import mechanize
import re
import cookielib
import requests
from urlparse import urlsplit
from urlparse import urljoin
from lxml import html
from bs4 import BeautifulSoup
import csv

#-----------------------------------Lists----------------------------------------#

url = 'http://www.mydala.com'
urls = [url]    #List containg temp Urls
visited = []    #List containing visited Url
temp_ot=[]      #Temporary list for offer title
temp_odes=[]    #Temporary list for offer description
deals=[]        #List containing all deals
omer=[]         #List containing all offers merchant
otitle=[]       #List containing all offers description
oloc=[]         #List containing all offers locations
odetail=[]      #Detailed description of all offers regarding validity,time,deals
depth = 0
root = url
zipped=[]       #Contain Zip of Offer By, Offer Promo


'''
    Code is limited to search deals and offer within Delhi region only.
    It can be made dynamic by replacing 'delhi' by list of cities fetched.
    Program will only search for Delhi for now
'''

#=========================================[[[[[[   SPIDER   ]]]]]]======================================#

# create lists for the urls in que and visited urls
def crawl(url,max_height,pages):
    index=1
    while len(urls)>0 and depth != max_height:
        try:
            br.open(urls[0])
            urls.pop(0)
            for link in br.links():
                newurl =  urlparse.urljoin(link.base_url,link.url)
                #print (newurl)
                if link.url.find('delhi')>=0 and newurl not in visited and depth != max_height :
                    visited.append(newurl)
                    urls.append(newurl)    
                    print("PAGE :"+str(index)+".1 "+newurl)
                    ot=offersMerchant(newurl)
                    temp_ot.append(ot)
                    odes=offersDesc(newurl)
                    temp_odes.append(odes)
                    print("Writing to csv....................")
                    write()
                    crawl_det(newurl)
                    temp_ot.pop(0)
                    temp_odes.pop(0)                
                    pages_to_be_looked(pages,index,newurl)
                    max_height-=1
                    index+=1
        except:
            print ("error")
            urls.pop(0)

        max_height-=1
        print (*visited,sep='\n')
        print('CSV Made')
        return visited

#Search for a number of pages for a given url
def pages_to_be_looked(pages,index,newurl):
    pages=pages+1
    page=2
    i=index
    while pages>page:
        url1=newurl+'?page='+str(page)+'-c'
        visited.append(url1);
        print("PAGE :"+str(i)+"."+str(page)+" "+url1)
        page+=1
        ot=offersMerchant(newurl)
        temp_ot.append(ot)
        odes=offersDesc(newurl)
        temp_odes.append(odes)
        write()
        print("Writing to csv....................")
        crawl_det(url1)
        temp_ot.pop(0)
        temp_odes.pop(0)                

#Crawl for pages that contain deals information 
def crawl_det(newurl):
    
    br.open(newurl)
    for link in br.links():
        newurl =  urlparse.urljoin(link.base_url,link.url)
        if link.url.find('deals')>=0 and newurl not in visited:
            deals.append(newurl)
            visited.append(newurl)
            offersDetail(newurl)
            offersLocation(newurl)
        else:
            pass
    print("Completed Pass.........................................")
#=========================================[[[[[[   SPIDER CLOSE   ]]]]]]=================================#

#*********************************************************************************************************

#=========================================[[[[[[   WRITER    ]]]]]]======================================#


#-----------------------------Writer Code for writing Offer Merchant and Offer Merchant------------------#

def write():
    if len(omer) != len(otitle):
        print ('list length mismatch')
    else:
        with open('result.csv', 'a') as outcsv:
            i=0
            k=len(omer[0])
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            while i<k:
                writer.writerow(*zipped_fl(i))
                i+=1
            for item in zipped:
                #Write item to outcsv
                writer.writerow(*zipped)

#----------Writer Code for writing Offer Description(Validity,Time,T&C..) and Offer Location---------------#
def write_loc(*zipped):
    with open('result.csv', 'a') as outcsv:
        writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for item in zipped:
            writer.writerow(*zipped)

def zipped_fl(i):
    zipped =[[ott[i], odess[i]]for ott,odess in zip(temp_ot,temp_odes)]
    return zipped

#=========================================[[[[[[   WRITER CLOSE    ]]]]]]=====================================#
#*************************************************************************************************************#

#----------Function Definition to find Offer Merchant, Offer Title, Offer Description(Validity,Time,T&C..) and Offer Location---------------#

def offersMerchant(newurl):
    page = requests.get(url=newurl)
    tree = html.fromstring(page.content)
    #This will create offer titles:
    if newurl.find('deals')>=0:
        pass
    else:
        title = tree.xpath('//span[@class="font-bold darkgrey-txt"]/text()')
    print("\nOFFER BY\n")
    omer.append(title)
    print(*title,sep='\n')
    return title
    

def offersDesc(newurl):
    page = requests.get(url=newurl)
    tree = html.fromstring(page.content)
    #This will create a list offer description
    desc = tree.xpath('//p[@class="text-13 darkgrey-txt margin-top-spacing-51"]/text()')
    print("\nOFFERS\n")
    otitle.append(desc)
    print(*desc,sep='\n')
    return desc
                    

def offersDetail(newurl):
    page = requests.get(url=newurl)
    tree = html.fromstring(page.content)
    offerDet = tree.xpath('//ul[@class="deal-terms-highlights-list"]/li/text()')
    print("\nFething Offer details....\n")
    odetail.append(offerDet)
    print("Writing to csv....................")
    write_loc(offerDet)
    #To show the fetched content remove '#'
    #print(*odetail,sep='\n')
    return offerDet
    

def offersLocation(newurl):
    page = requests.get(url=newurl)
    tree = html.fromstring(page.content)
    loc = tree.xpath('//div[@class="deal-location-details text-12 darkgrey-txt"]/text()')
    print("\nFething Offer location....\n")
    #To fetch more than one retail address use 'if':-
    '''if len(loc)>4:
        i=0
        while i<4:
            k=2
            a=loc.pop(i+k)
            c=loc.pop(i).strip()
            loc.append(c+a)
            i+=2
            k+=2
    else:'''
    if len(loc)>0:
        a=loc.pop(3)
        c=loc.pop(1).strip()
        while(len(loc)>0):
            loc.pop(0)
        loc.append(c+a)
        oloc.append(loc)
        print("Writing to csv....................")
        write_loc(oloc)
        #To show the fetched content remove '#'
        #print(*oloc,sep='\n')
        return loc
    else:
        return loc

#Search a specific item for any number of pages on (www.mydala.com)
#----------------Not Tested
def search_pages(pages,search):
    page=1
    i=index
    newurl='http://www.mydala.com/delhi/search?'
    print(newurl)
    while pages>=page:
        url1=newurl+'?page='+str(page)+'&q='+str(search)
        print(url1)
        page+=1
        crawl(url1,1,pages)

#--------------Not completed
def offersImg(newurl):
    page = requests.get(url=newurl)
    tree = html.fromstring(page.content)
    img = tree.xpath('//div/a[@class="pager-active"]/@src/text()')
    #img = re.search('@src="([^"]+)"',text)
    print("\nFething Offer Img Url....\n")
    print (img)
    

'''Cities can be fetched to and saved in a list to pass later on in crawling function.
This will provide offers and details in all the cities of set generated'''
#---------------Not Completed    
def city(url):
    page = requests.get(url=url)
    tree = html.fromstring(page.content)
    #This will create offer titles:
    city = tree.xpath('//div[@class="select-text display-block margin-bottom-spacing-10 auto-margin"]/text()')
    #<option selected="" value="delhi|27">Delhi NCR</option>
    print("CITIES")
    print(*city,sep='\n')



#===============================+++++++++[ MAIN ]+++++++++++++==============================#


if __name__ == "__main__":

    # the a mechanize browser object
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    br.set_handle_redirect(True)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0')]

    print("Max Height defines number of links to be traversed on a page.")
    a =input("Max Height : ")
    print("Max Depth defines number of subsequent pages of a link.")
    b=input("Max Depth : ")
    print("\n")
    print("++++++++++++++++++Starting to crawl+++++++++++++++++++\n")
    #TEST FUNCTIONS
    crawl(url,a,b)
    #pages_to_be_looked(5,1,url)
    #city(url)
    #offersLocation(url)
    #write()
    #not working offersImg(url)


#++++++++++++++++++++++++++++++++[[[[[[  END   ]]]]]+++++++++++++++++++++++++++++++++#
