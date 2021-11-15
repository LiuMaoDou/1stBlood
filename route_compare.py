import pandas as pd
import ipaddress
import multiprocessing
import time
from pathlib import Path
import os
import re


# csvFile = r'.\input\input.csv'
# pdResult = pd.read_csv(csvFile)


def collect_to_df():
    """
    获取文件夹下的txt文档，提取路由，排序，放入df
    :return:
    """
    host = re.compile(r'<(.*?)>')
    route = re.compile(r'(\d+\.\d+\.\d+\.\d+/\d+)')

    p = Path('.')
    # list(p.glob('**/*.txt'))
    dic = {}

    for file in list(p.glob('**/*.txt')):
        lst = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                if host.search(line):
                    hostname = host.search(line).group(1)
                    dic[hostname] = lst

                if route.search(line):
                    dic[hostname].append(route.search(line).group(1))

    pd.DataFrame({key: pd.Series(value) for key, value in dic.items()}).to_excel(r'./output/allRoutes.xlsx')
    return pd.DataFrame({key: pd.Series(value) for key, value in dic.items()})


def compare(sNet, pdResult):
    for dNet in pdResult.columns.tolist():
        if sNet == dNet:
            continue

        rows = pdResult.shape[0]
        lst = []
        j = 1
        count = 0

        for ip1 in pdResult[sNet]:
            if ip1 == "NA":
                break

            if pdResult[dNet][0] == "NA":
                break

            i = 0
            print(dNet + "---" + str(j))
            j += 1
            for row in range(count, rows):
                ip2 = pdResult[dNet][row]
                if ip2 == "NA":
                    break
                else:
                    if ipaddress.IPv4Network(ip1).overlaps(ipaddress.IPv4Network(ip2)):
                        lst.append([sNet, dNet, ip1, ip2])
                        # print(lst)
                        count = row - i
                        i += 1

                    else:
                        if i > 0:
                            break

        df = pd.DataFrame(lst, columns=['Overlapped ' + sNet, 'Overlapped ' + dNet, 'Overlapped ' + sNet + '1 Subnets',
                                        'Overlapped ' + dNet + " Subnets"])
        df.to_excel(r'./output/(' + sNet + '-' + dNet + ")-output.xlsx")


if __name__ == "__main__":
    print("...Starting...")
    now1 = time.time()
    cpus = multiprocessing.cpu_count() - 1
    pool = multiprocessing.Pool(processes=cpus)

    pdResult = collect_to_df()
    pdResult.fillna('NA', inplace=True)
    columns = pdResult.columns.tolist()

    [pool.apply_async(compare, args=(i, pdResult,)) for i in columns]
    pool.close()
    pool.join()

    now2 = time.time()
    now3 = (now2 - now1)
    now4 = (now2 - now1)/60
    print("------------------Finished------------------")
    print("...用时{} Secs...".format(round(now3, 2)))
    print("...用时{} Mins...".format(round(now4, 2)))
