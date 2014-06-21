# -*- coding: utf8 -*-
from videodownloader import *

url = "http://www.ttmeiju.com/meiju/Conan.html"

soup = htmlReader(url)

for item in soup.find_all("a", title=u"磁力链"):
    ep_name = item.parent.previous_sibling.previous_sibling.string
    magnet = item["href"]
    print ep_name
    print magnet
