import requests, sys, time, os
from urllib.parse import urlparse

clear = lambda: print("\033c", end="", flush=True)

def downloadFile(url, directory, id) :
  with open(directory + '/' + id + '.zip', 'wb') as f:
    start = time.time()
    r = requests.get(url, stream=True)
    total_length = r.headers.get('content-length')
    dl = 0
    if total_length is None:
      f.write(r.content)
    else:
      for chunk in r.iter_content(8192):
        dl += len(chunk)
        f.write(chunk)
        done = int(80 * dl / int(total_length))
        clear()
        sys.stdout.write("\r[%s%s] %s KbPS" % ('=' * done, ' ' * (80-done), round((dl//(time.time() - start)) / 1000, 1)))
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

json_data = {
    'shortUrl': id,
}

requests.options("https://eu-central-1.transferxl.com/api/v2/download/getToken")
response = requests.post('https://eu-central-1.transferxl.com/api/v2/download/getToken', headers=headers, json=json_data)

downloadFile(f"https://eu-central-1.transferxl.com/api/v2/download/TransferXL-{id}?downloadToken={response.json()['downloadToken']}", os.getcwd(), id)
