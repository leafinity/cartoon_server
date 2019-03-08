import time
import json
import requests

url = 'http://127.0.0.1:5000/'
files = {'file': open('test.jpg','rb')}

r = requests.post(url + 'cartoon_transform/shinkai', files=files)
if r.status_code == 200:
    task_id = r.text
    print(task_id)
else:
    print(r.status_code)
    exit()

for i in range(30):
    r = requests.get(url + 'cartoon_transform/check_status/%s' % task_id)
    if r.status_code == 200:
        finished = json.loads(r.text)['finished']

        if not finished:
            time.sleep(5)
            print('task hasn\'t been finished')
        else:
            print('>>> task finished')
            r = requests.get(url + 'cartoon_transform/download_image/%s' % task_id)
            with open('test_recieved.jpg', 'wb') as f:
                f.write(r.content)
            break
    else:
        print('something wrong')
        break
else:
    print(r.status_code)