import requests
import time
'''
查询京东昨天的有效订单
'''
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
	'Cookie': 'store.o2o.jd.com1=37FEFTC5JXFQSGFUJLHWPPDPDGVGJR6BCMWDOGCIIOYVICXLKIDKQ5LDCHYANUNRDXVZCWZSAFTBIP2TGQMVADFF4AGRHZFMSNYEH6VDUJZK7TQZK22JATPIHYPCMJHP2426II3E6OOI6UGDKHVJBKHNW6KSSPTJWHN7RUIUUB7HZIPGOTTDAANNVBI2GXPJEADCFVGZ3VPYSXPZTGMQHNDL3V2PPDCPA3LBGDOGWMNJ362W2SXCVNK3K6THT4NCGQW4NV7SZ4TX32D2XQA7PIX46M',
}
yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))
# yesterday = '2018-05-01'
params = {
	'shopIdListStr':	11728789,
	'cityType': '',
	'dateType':	'day',
	'calendarDate':	yesterday,
	'calDt':	yesterday,
	'endDate':	yesterday,
	'timeRangeType':	1,
	'dateDay':	yesterday,
	'roleType':	2,
	'venderId':	320695,
}
url = 'https://dc-store.jd.com/operation/queryData'
response = requests.get(url, headers=headers, params=params).json()
data = {}
data['calendarDate'] = response['calendarDate']
data['validOrderCount'] = response['validOrderCount']
data['validOrderCountRelativeRatio'] = float(response['validOrderCountRelativeRatio']) / 100
if time.time() - time.mktime(time.strptime(data['calendarDate'], '%Y-%m-%d')) > 2*24*60*60:
	print('数据还未更新，等下再来试试！')
else:
	print(data)
	print(str(data['validOrderCount']) + '\t' + str(data['validOrderCountRelativeRatio']))