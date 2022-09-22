from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType
from settings import *
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

class Parser:
	def __init__(self, url):
		print("Parser.__init__ executing")
		self.url = url
		self.pages = 3
		self.driver = self.init_driver()
		self.output_file_name = "data_16.csv"
		self.start_page = 9
		self.create_dataframe()
		self.driver.quit()

	def init_driver(self):
		myProxy = "121.1.41.162:111"

		proxy = Proxy({
			'proxyType': ProxyType.MANUAL,
			'httpProxy': myProxy,
			'ftpProxy': myProxy,
			'sslProxy': myProxy,
			'noProxy': ''  # set this value as desired
		})

		options = Options()
		# options.add_argument('--headless')
		driver = webdriver.Firefox(executable_path=BROWSER_DRIVER_PATH, options=options,
		                           firefox_binary=FIREFOX_PATH_BIN, proxy=proxy)
		return driver

	def get_item_by_data_attr(self, el, attr, attr_val):
		r = [item for item in el.find_all()
		        if ((f"data-{attr}" in item.attrs) and (item[f"data-{attr}"] == attr_val))]
		return r[0] if len(r) else None

	def get_items_by_data_attr(self, el, attr, attr_val):
		r = [item for item in el.find_all()
		        if ((f"data-{attr}" in item.attrs) and (item[f"data-{attr}"] == attr_val))]
		return r if len(r) else None

	def create_dataframe(self):
		data = self.parse()

		name = []
		salary = []
		company_name = []
		metro_station = []
		description_list_items = []
		description = []
		employment_mode = []
		experience = []
		company_address = []
		rating = []
		skills = []

		for flat in data:
			name.append(flat["name"])
			salary.append(flat["salary"])
			company_name.append(flat["company_name"])
			metro_station.append(flat["metro_station"])
			description_list_items.append(flat["description_list_items"])
			company_address.append(flat["company_address"])
			employment_mode.append(flat["employment_mode"])
			experience.append(flat["experience"])
			rating.append(flat["rating"])
			skills.append(flat["skills"])
			description.append(flat["description"])

		data = {'name': name,
		        'salary': salary,
				'company_name': company_name,
		        'metro_station': metro_station,
		        'description_list_items': description_list_items,
		        'company_address': company_address,
		        'rating': rating,
		        'skills': skills,
		        'description': description}

		df = pd.DataFrame(data)

		print(df)
		df.to_csv(self.output_file_name, encoding='utf-8', index=False)

	def parse(self):
		data = []
		for i in range(1, self.pages+1):
			print(f"{i}/{self.pages}")
			self.driver.get(f"{self.url}&page={self.start_page+i}")

			if i == 1:
				input("continue")
			time.sleep(3)

			soup = BeautifulSoup(self.driver.page_source, "html.parser")
			jobs = soup.find_all("div", class_="serp-item")
			print(len(jobs))

			for job in jobs:
				try:
					name = job.find("span", class_= "serp-item__name").text.strip()
					company_name = job.find("div", class_= "vacancy-serp-item__meta-info-company").text.strip()
					try:
						metro_station = job.find("span", class_= "metro-station").text.strip()
					except AttributeError:
						metro_station = ""

					# get job link
					link = self.get_item_by_data_attr(job, "qa", "vacancy-serp__vacancy-title")["href"]

					f = {"name":name, "company_name": company_name, "metro_station": metro_station, "link": link}
					print(f)
					data.append(f)
				except Exception as e:
					print("ignored:", e)

		print(data)
		return self.clean(data)

	def get_job_description(self, link):
		self.driver.get(link)
		soup = BeautifulSoup(self.driver.page_source, "html.parser")
		description_list_items = soup.find("p", class_="vacancy-description-list-item")
		try:
			dli = [item.text.strip() for item in description_list_items]
		except TypeError: # None type case
			dli = []

		try:
			employment_mode = self.get_item_by_data_attr(soup, "qa", "vacancy-view-employment-mode").text.strip()
		except AttributeError:
			employment_mode = ""
		try:
			experience = self.get_item_by_data_attr(soup, "qa", "vacancy-experience").text.strip()
		except AttributeError:
			experience = ""

		try:
			rating = soup.find("div", class_="_1GLZgRI___bloko-text").text.strip()
		except AttributeError:
			rating = None

		try:
			company_address = self.get_item_by_data_attr(soup, "qa", "vacancy-view-raw-address").text.strip()
		except:
			company_address = ""

		try:
			description = self.get_item_by_data_attr(soup, "qa", "vacancy-description").text.strip()
		except AttributeError:
			description = ""
		try:
			skills = [x.text.strip() for x in self.get_items_by_data_attr(soup, "qa", "bloko-tag bloko-tag_inline skills-element")]
			skills = ", ".join(skills)
		except TypeError:
			skills = ""

		try:
			salary = self.get_item_by_data_attr(soup, "qa", "vacancy-salary-compensation-type-net").text.strip()
		except:
			salary = ""



		return {"salary": salary, "description_list_items": dli, "rating": rating, "company_address": company_address,
		        "description": description, "skills": skills, "employment_mode": employment_mode,
		        "experience": experience}

	def clean(self, data):
		print(f"Total data length: {len(data)}")
		i = 1
		r = data
		for job in r:
			print(f"{len(data)}/{i}")
			job.update(self.get_job_description(job["link"]))
			i+=1
		return r


Parser('https://hh.ru/search/vacancy?area=1&professional_role=96&search_field=name&search_field=company_name&search_field=description&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82')
# Parser('https://realty.yandex.ru/moskva/kupit/kvartira/')
# Parser('https://realty.yandex.ru/moskva_i_moskovskaya_oblast/kupit/kvartira/?subLocality=193391&subLocality=193283&subLocality=193292&subLocality=193380&subLocality=193296&subLocality=193305&subLocality=193362&subLocality=193288&subLocality=193394&subLocality=193358&subLocality=12447&subLocality=193363&subLocality=193367&subLocality=193313&subLocality=12444&subLocality=12425&subLocality=193393&subLocality=193278&subLocality=193347&subLocality=12435&subLocality=193282&subLocality=193377&subLocality=193346&subLocality=193349&subLocality=193350&subLocality=193371&subLocality=193285&subLocality=193392&subLocality=193374&subLocality=193340&subLocality=17394073&subLocality=193341&subLocality=193345&subLocality=193293&subLocality=12431&subLocality=12434&subLocality=193388&subLocality=193348&subLocality=193351&subLocality=193378&subLocality=193357&subLocality=193364&subLocality=12453&subLocality=12452&subLocality=12449&subLocality=193384&subLocality=193385&subLocality=193281&subLocality=193297&subLocality=193299&subLocality=193304&subLocality=193289&subLocality=12450&subLocality=193355&subLocality=193356&subLocality=193361&subLocality=193284&subLocality=12440&subLocality=12443&subLocality=193336&subLocality=193337')


# Average MAE score:
# 1921015.6195226917
# (4162, 19)
# Average MAE score (only zones 3 and 4):
# 636187.3277310925

# Average MAE score:
# 1493205.7910798122
# (4164, 19)
# Average MAE score (only zones 3 and 4):
# 514120.81032412965

# Average MAE score:
# 1493205.7910798122
# (4164, 19)
# Average MAE score (only zones 3 and 4):
# 514120.81032412965
# (2224, 19)
# Average MAE score (only zones 1 and 2):
# 960988.7438202248
# import random
# import pandas as pd
#
# data = pd.read_csv("data_extended_2.csv")
# print(data.longitude)
# s = ""
# for i in range(350):
# 	idx = random.randint(1, 6500)
# 	s += f"{data.iloc[idx].longitude}%2C{data.iloc[idx].latitude}~"
# print(f"https://yandex.ru/maps/?pt={s}"[:-1])
