# -*- coding: UTF-8 -*-
import sys
import urllib

reload(sys)
sys.setdefaultencoding("utf-8")

key = 'gear+360'
t = urllib.quote(key)
print t