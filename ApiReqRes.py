from urllib import request
import urllib
from urllib.request import urlopen
req = request.Request('http://127.0.0.1:5000/student/riya')

# try:
res = urlopen(req)
print(res.read())
# except urllib.error.HTTPError as e:
#     print(e.code , e.read())  
 