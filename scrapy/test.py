import re
url = 'https://www.dytt789.com/Zuixinmeiju/XSZRDJJ/'
# url = 'https://www.dytt789.com/Dianshiju/'

pattern = r'https://www.dytt789.com/(\w+)/(\w+)/'
deny = r'https://www.dytt789.com/(\w+)/$'

match = re.compile(deny).match(url)
if match:
    print(match[0])
else:
    print("not match")
