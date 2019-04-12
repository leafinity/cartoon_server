import argparse
import requests
 

parser = argparse.ArgumentParser()

parser.add_argument("--testfile", help="path to test image file")
parser.add_argument("--hostname", help="server hostname")

args = parser.parse_args()

files = {'file': open(args.testfile,'rb')}

url = ''
if args.hostname[:4] != 'http':
    url += 'http://'
url += args.hostname 
if args.hostname[-1] != '/':
    url += '/'

url += 'sync_cartoon_transform/hosoda'

print(url)

r = requests.post(url, files=files)
if r.status_code == 200:
    with open('test_recieved_jupyter.jpg', 'wb') as f:
        f.write(r.content)
else:
    print(r.status_code)