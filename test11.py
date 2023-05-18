import requests

headers = {'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'}
url = 'http://zxcs.me/'

res = requests.get(url = url, headers= headers)

ress = res.text

print(ress)