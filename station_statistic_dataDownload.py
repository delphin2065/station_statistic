import pandas as pd
import requests as re
import json
def data():
    url = '	https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/8ae4cabf6973990e0169947ed32454b9'
    res = re.get(url)
    res = json.loads(res.text)
    n = len(res)
    lst = []
    for i in range(n):
        dic_d = {}
        for key, value in res[i].items():
            dic_d[key] = value
        lst.append(dic_d)
    
    df = pd.DataFrame(lst)
    df['trnOpDate'] = pd.to_datetime(df['trnOpDate']).dt.date
    df = df.sort_values(['trnOpDate', 'staCode'])
    df.rename(columns={'trnOpDate': '日期', 'staCode': '站別碼', 'gateInComingCnt':'入站人數', 'gateOutGoingCnt':'出站人數'}, inplace=True)
    df['入站人數'] = df['入站人數'].astype(int)
    df['出站人數'] = df['出站人數'].astype(int)

    return df

