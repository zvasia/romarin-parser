import lzstring
import requests
import json

SEARCH_URL = 'https://www3.wipo.int/madrid/monitor/jsp/select.jsp'

from_date = '2019-03-01'
to_date = '2019-03-02'
page = '0'
rows = '100'

PARAMS = '{"p":{"search":{"sq":[{"te":"[' + from_date + 'T00:00:00Z TO ' + to_date + 'T23:59:59Z]",' \
         '"fi":"RD","dt":"[' + from_date + ' TO ' + to_date + ']","co":"AND"}]},"start":' + page + '00,' \
         '"rows":' + rows + ',"facets":["DS"]},' \
         '"type":"madrid","la":"en","qi":"0-rjTy7CiEHtutaR7TQMJ8wgA/yn+fiAVGhSfFY1k6KmM="}'
enc = lzstring.LZString()
qz = enc.compressToBase64(PARAMS)

r = requests.post(SEARCH_URL, data={'qz': qz})
search_result = json.loads(r.content)
total_tms = search_result['response']['numFound']
pages = total_tms/int(rows)
print(total_tms)
irn_array = []


while int(page) < pages:
    for trademark in search_result['response']['docs']:
        irn_array.append(trademark['IRN'])
    page = str(int(page) + 1)
    PARAMS = '{"p":{"search":{"sq":[{"te":"[' + from_date + 'T00:00:00Z TO ' + to_date + 'T23:59:59Z]",' \
                '"fi":"RD","dt":"[' + from_date + ' TO ' + to_date + ']","co":"AND"}]},"start":' + page + '00,' \
                '"rows":' + rows + ',"facets":["DS"]},' \
                '"type":"madrid","la":"en","qi":"0-rjTy7CiEHtutaR7TQMJ8wgA/yn+fiAVGhSfFY1k6KmM="}'

    qz = enc.compressToBase64(PARAMS)
    r = requests.post(SEARCH_URL, data={'qz': qz})
    search_result = json.loads(r.content)

f = open("irns.txt", "w+")
for i in range(len(irn_array)):
     f.write(irn_array[i] + "\n")

f.close()

