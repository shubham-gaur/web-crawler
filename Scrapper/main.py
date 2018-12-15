import urllib
import re
import mechanize
from bs4 import BeautifulSoup
import urlparse
import cookielib
from urlparse import urlsplit
from lxml import html
import requests
#import PublicSuffixList

url = "http://www.mydala.com"

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.set_handle_redirect(True)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
page = br.open(url, timeout=5)

htmlcontent = page.read()
soup = BeautifulSoup(htmlcontent,'lxml')

newurlArray = []

#for link in br.links(text_regex=re.compile('^((?!offers).)*$')):
for link in br.links():
    if link.url.find('offer')>=0:
        newurl = urlparse.urljoin(link.base_url, link.url)
        if newurl not in newurlArray:
            newurlArray.append(newurl)
            print newurl
            page = requests.get(url=newurl)
            tree = html.fromstring(page.content)
            #This will create offer titles:
            title = tree.xpath('//span[@class="font-bold darkgrey-txt"]/text()')
            #This will create a list offer description
            desc = tree.xpath('//p[@class="text-13 darkgrey-txt margin-top-spacing-51"]/text()')
            print title
