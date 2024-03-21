import requests, sys, time, os
from urllib.parse import urlparse

clear = lambda: print("\033c", end="", flush=True)

def downloadFile(url, directory, id, response_pending_json) :
  with open(directory + '/' + id + '.zip', 'wb') as f:
    start = time.time()
    r = requests.get(url, stream=True)
    total_length = r.headers.get('content-length')
    dl = 0
    if total_length is None:
      f.write(r.content)
    else:
      for chunk in r.iter_content(16384):
        dl += len(chunk)
        f.write(chunk)
        done = int(8000 * dl / int(total_length))
        clear()
        sys.stdout.write(response_pending_json)
        print('')
        sys.stdout.write("\r[%s%s] %s  %s KbPS" % ('=' * int(done / 100), ' ' * (80-int(done / 100)), f"{round(done / 80, 1)} %", round((dl//(time.time() - start)) / 1000, 1)))
        print('')
  return (time.time() - start)

link = input("Download link: ")

id = urlparse(link).path.rsplit("/", 2)[-2]

headers = {
    'Accept': '*/*',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Logging-id': 'cc7755',
    'Origin': 'https://www.transferxl.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-TXL-GOOGLE': '{}',
    'sec-ch-ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

headers_pending = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Logging-id': '108e66',
    'X-TXL-GOOGLE': '{}',
    'Origin': 'https://www.transferxl.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

json_data = {
    'shortUrl': id,
}

params_pending = {
    'perFilePendingStatus': 'true',
    'shortUrl': '08vkvQ7f635p8v',
}

print("Getting token")
requests.options("https://eu-central-1.transferxl.com/api/v2/download/getToken")
response = requests.post('https://eu-central-1.transferxl.com/api/v2/download/getToken', headers=headers, json=json_data)
print("Getting metadata")
response_pending = requests.get('https://eu-central-1.transferxl.com/api/v2/history/download', params=params_pending, headers=headers_pending)
print("Starting download")
downloadFile(f"https://eu-central-1.transferxl.com/api/v2/download/TransferXL-{id}?downloadToken={response.json()['downloadToken']}", os.getcwd(), id, f"{response_pending.json()['id']}.zip / Uploaded by {response_pending.json()['from']}")
