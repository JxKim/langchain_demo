def mineru_upload_file_demo():
    import requests
    import os
    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIyMzIwMDA5MSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3MDA4NTA1NSwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiMTg4MTA2NTI3MTEiLCJvcGVuSWQiOm51bGwsInV1aWQiOiI2NGEwNmJiNi03NDI2LTQ3OTctODU5ZC1mM2I1ZTQ3N2ZhYmQiLCJlbWFpbCI6IiIsImV4cCI6MTc3MTI5NDY1NX0.FL542YFMubP8oHeCq04PzqiQ_QSs8yI-m1UUWQ9u4fWi-6sm4XMwmziwjx7Be9JAQFZLhHTlaFKD2I38Hc-KrA"
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
    "files": [
        {"name":"NLP.pdf", "data_id": "abcd"}
    ],
    "model_version":"vlm"
    }
    file_path = [r"D:\PycharmProjects\lessons\demo_class\LangGraph_demo\langchain_demo\05_retrieval\assets\尚硅谷大模型技术之NLP1.0.2.pdf"]
    try:
        response = requests.post(url,headers=header,json=data)
        if response.status_code == 200:
            result = response.json()
            print('上传成功:{}'.format(result))
            batch_id = result['data']['batch_id']
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):
                    with open(file_path[i], 'rb') as f:
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} 上传成功")
                        else:
                            print(f"{urls[i]} 上传失败")
            else:
                print('apply upload url failed,reason:{}'.format(result.msg))
            return batch_id
        else:
            print(f"请求失败，状态码：{response.status_code}，响应内容：{response.text}")
    except Exception as err:
        print(err)

def check_batch_status(batch_id):
    """
    通过batch_id查询文件上传状态
    
    :param batch_id: Description
    """
    import requests
    import time
    import os 
    token = "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIyMzIwMDA5MSIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3MDA4NTA1NSwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiMTg4MTA2NTI3MTEiLCJvcGVuSWQiOm51bGwsInV1aWQiOiI2NGEwNmJiNi03NDI2LTQ3OTctODU5ZC1mM2I1ZTQ3N2ZhYmQiLCJlbWFpbCI6IiIsImV4cCI6MTc3MTI5NDY1NX0.FL542YFMubP8oHeCq04PzqiQ_QSs8yI-m1UUWQ9u4fWi-6sm4XMwmziwjx7Be9JAQFZLhHTlaFKD2I38Hc-KrA"
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    res = requests.get(url, headers=header)
    while res.json()["data"]['extract_result'][0]['state'] != 'done':
        print('当前状态为running，等待6秒后重试')
        time.sleep(6)
        res = requests.get(url, headers=header)
        print(res.status_code)
        print(res.json()["data"]['extract_result'][0]['state'],end="\n\n=========\n\n")
    print('提取结果为:',res.json()["data"]['extract_result'][0]['full_zip_url'])



# batch_id = mineru_upload_file_demo()
# print('当前的batch_id为：',batch_id)
check_batch_status("450e959e-65d1-4c64-a6a8-46e7a1ba2aab")

import nltk