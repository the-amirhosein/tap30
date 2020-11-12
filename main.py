import requests
import json
from datetime import date
import time
import schedule
from termcolor import colored


def request():
    headers = {
        'Connection': 'keep-alive',
        'x-authorization': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjozODc1NzkzLCJyb2xlIjoiUEFTU0VOR0VSIiwiY2l0eSI6IlRFSFJBTiJ9LCJpYXQiOjE2MDQ5NDQyNzYsImF1ZCI6ImRvcm9zaGtlOmFwcCIsImlzcyI6ImRvcm9zaGtlOnNlcnZlciIsInN1YiI6ImRvcm9zaGtlOnRva2VuIn0.XJas-AjEjzSdltqq4pyX9yg03Vy0zXU5RcXslUCD2SOqQ-niX6pmxu2PSXqJDiTOIlVJN1yZdcA6BBHwDHo7dA',
        'x-agent': 'v2.1|passenger|WEBAPP|3.10.3||5.0',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36',
        'content-type': 'application/json',
        'Accept': '*/*',
        'Origin': 'https://app.tapsi.cab',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.tapsi.cab/',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
    }

    data = '{"origin":{"latitude":35.64403719765346,"longitude":51.36890864474185},"destinations":[{"latitude":35.76591873168945,"longitude":51.39497375488281}],"initiatedVia":"WEB"}'

    # try:
    response = requests.post('https://tap33.me/api/v2.3/ride/preview', headers=headers, data=data)

    data = json.loads(response.content)
    data = data["data"]
    for catg in data['categories']:
        if catg['key'] == 'NORMAL':
            for service in catg['services']:
                if service['key'] == 'NORMAL':
                    price = service['prices']
                    print(colored(str(time.strftime("%H:%M:%S", time.localtime())), 'yellow'),
                          colored(str(price[0]['passengerShare']), 'green'))
                    write_in_file(price[0]['passengerShare'])
# except:
#     print(colored('something wrong', 'red'))
#     write_in_file('something wrong')


def write_in_file(price):
    fi = open("tap30.csv", 'a')
    fi.write(str(price) + ' , ' + str(date.today()) + ' , ' + str(time.strftime("%H:%M:%S", time.localtime())))
    fi.write('\n')
    fi.close()


if __name__ == '__main__':
    print(time.strftime("%H:%M:%S", time.localtime()))
    schedule.every(1).minutes.do(request)

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
