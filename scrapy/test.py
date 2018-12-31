import re
# url = 'https://www.dytt789.com/Zuixinmeiju/XSZRDJJ/'
# # url = 'https://www.dytt789.com/Dianshiju/'

# pattern = r'https://www.dytt789.com/(\w+)/(\w+)/'
# deny = r'https://www.dytt789.com/(\w+)/$'

# match = re.compile(deny).match(url)
# if match:
#     print(match[0])
# else:
#     print("not match")
url = 'http://www.minnano-av.com/actress355788.html'

pattern = r'http://www.minnano-av.com/actress(\d+).html'
deny = r'https://www.dytt789.com/(\w+)/$'

match = re.match(pattern, url)
if match:
    print(match[0])
else:
    print("not match")

print(
    url.replace('http://www.minnano-av.com/actress', '').replace('.html', ''))
