import time

import lzstring
import requests
import json

SEARCH_URL = 'https://www3.wipo.int/madrid/monitor/jsp/select.jsp'

PAGE_SIZE = 100

date_from = '2018-03-01'
date_to = '2019-04-02'
irn_array = []

PARAMS_TEMPLATE = {
    "p":
        {"search":
            {
                "sq":
                    [{
                        "te": "[%(from_date)sT00:00:00Z TO %(to_date)sT23:59:59Z]",
                        "fi": "RD",
                        "dt": "[%(from_date)s TO %(to_date)s]",
                        "co": "AND"
                    }]
            },
            "rows": "%(page_size)s",
            "start": "%(page)s00",
            "facets": ["DS"]
        },
    "s": {
        "set": {
            "rows": 100,
            "display": "grid"}},
    "type": "madrid",
    "la": "en",
    "qi": "%(qi)s"
}


# 11-rjTy7CiEHtutaR7TQMJ8wgA/yn+fiAVGhSfFY1k6KmM= 1  12 pgs
# 1-mrI0qk/nhwL1f6rDA+11Z0f1DnPGUg0WM95NYsTJ+y4=
# 0-InH8MsgquH5/i1+uU6ciCPawQwGEuFJ+3NLdvToeBYA=


def get_result_page(from_date, to_date, page, qi):
    params = json.dumps(PARAMS_TEMPLATE) % {
        "from_date": from_date,
        "to_date": to_date,
        "page": str(page),
        "page_size": PAGE_SIZE,
        "qi": qi
    }
    print(str(page) + '00')
    enc = lzstring.LZString()
    qz = enc.compressToBase64(params)
    r = requests.post(SEARCH_URL, data={'qz': qz})
    result = json.loads(r.content)
    # print("request: " + params)
    print(r.content)
    return result


def get_num_pages(content):
    total_tms = content['response']['numFound']
    # print(total_tms)
    num_of_pages = total_tms / PAGE_SIZE
    return num_of_pages


def process_result(content):
    # print(len(content['response']['docs']))
    for trademark in content['response']['docs']:
        irn_array.append(trademark['IRN'])


# проверяем есть ли в ответе 'qk', если есть, то меняем qi в запросе и подставляем цифру
def get_query_id(content):
    try:
        return "4-" + content['qk']
    except:
        return content['qi']


search_result = get_result_page(date_from, date_to, 0, "11-rjTy7CiEHtutaR7TQMJ8wgA/yn+fiAVGhSfFY1k6KmM=")
pages = int(get_num_pages(search_result)) + 1
process_result(search_result)
qi = "1-rjTy7CiEHtutaR7TQMJ8wgA/yn+fiAVGhSfFY1k6KmM="
# get_query_id(search_result)
print(qi)

for i in range(1, pages):
    search_result = get_result_page(date_from, date_to, i, qi)
    process_result(search_result)
    qi = get_query_id(search_result)
    # ниже qi подобранные для конкретной даты(аж 21 страницу можно спарсить), довольно бесполезное занятие,
    # т.к. меняем дату и все рушится
    # if 10 < i < 17:
    #     qi = "1-oVdUzZZEGK5WlXFPy6Edzyq/xj0pTdX8/aJwd5L57yA="
    # elif i > 16:
    #     qi = "1-8eN+RsIOXE+0Z4hyjlBgJXurkUU9GWlv30+C+047gXU="
    print(qi)

f = open("irns.txt", "w+")
for num in irn_array:
    f.write(num + "\n")
f.close()

# qi1 4-kOfCdOo7WWX2wXC+PmxutpwjyuRGjKAWYwbRmgRm+TI=
# qk1 hvu5hWtlK1mgcZncxTYKM3r2YRUAZEuzOrvH8L31UtY=
# qi2 4-hvu5hWtlK1mgcZncxTYKM3r2YRUAZEuzOrvH8L31UtY=
# qk2
