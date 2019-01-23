import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 引入配置文件
from conf import *

try:
	driver = webdriver.Chrome()
	# 浏览器窗口最大化,查询按钮在非全屏的状态下被隐藏
	driver.maximize_window()
	driver.implicitly_wait(15)  # 隐性等待，最长等12秒
	driver.get('https://store.jd.com/menu')
	driver.add_cookie({'name':'shop.o2o.jd.com1', 'value': COOKIE, 'domain': '.jd.com'})
	driver.get('https://store.jd.com/menu')
	sleep(1)
	driver.switch_to_alert().accept();
	sleep(1)
	driver.switch_to_alert().accept();
	# 点击商家商品管理
	driver.find_element_by_xpath("//span[text()='商品管理']").click()
	sleep(1)
	driver.find_element_by_xpath("//a[text()='商家商品管理']").click()

	driver.switch_to.frame(0)
	driver.switch_to.frame(1)
	num = 1
	# 一级标签
	tag = ['果蔬蛋类', '肉类家禽']
	sleep(1)
	for value in tag:
		driver.find_element_by_xpath("//option[text()='" + value + "']").click()
		sleep(1)
		optCount = len(driver.find_elements_by_xpath("//select[@name='shopCategoryLevel2']/option"))
		for j in range(1, optCount):
			# 二级标签
			driver.find_element_by_xpath("//select[@name='shopCategoryLevel2']/option[" + str(j+1) + "]").click()
			sleep(1)
			# 点击查询
			driver.find_element_by_xpath("//input[@value='查询']").click()
			while True:
				sleep(2)
				# 计算一页商品数目
				tr = driver.find_elements_by_xpath("//div[@id='productGrid']/table/tbody/tr")
				if len(tr) == 1:
					if len(driver.find_elements_by_xpath("//div[@id='productGrid']/table/tbody/tr/td")) == 1:
						break
				for i in range(len(tr)):
					# 得到商品图片下载地址
					element = driver.find_element_by_xpath("//div[@id='productGrid']/table/tbody/tr[" + str(i+1) + "]/td[2]/div/div[1]/img")
					src = element.get_attribute('src')
					# 得到商品名称
					element = driver.find_element_by_xpath("//div[@id='productGrid']/table/tbody/tr[" + str(i+1) + "]/td[2]/div/div[2]/p")
					title = element.text
					title = title.split('约')
					title = title[0].strip()
					print(str(num) + ',', title + ',', src)
					# 打开图片并保存为文件
					response = requests.get(src)
					f = open('pic/' + title + '.jpg', 'wb')
					f.write(response.content)
					f.close()
					num += 1
				nextPage = driver.find_element_by_xpath("//*[text()='下一页'][1]")
				nextPage.click()
				if nextPage.get_attribute('class') == 'disabled':
					break
	sleep(10)
except Exception as err:
	print(err)
finally:
	driver.quit()
	print('Finish!!!')