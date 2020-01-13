#Author: Stefan Alexandru Obada
#Company: Learnisa
#Scope: Crawl edX courses
from scrapy import Spider
from selenium import webdriver
from scrapy.http import Request
from scrapy.selector import Selector
from coursedata.items import Course
import re

class EdxSpider(Spider):
	name = 'edx'
	allowed_domains = ['www.edx.org/']

	def start_requests(self):
		self.driver = webdriver.Chrome('C:\ProgramData\Anaconda3\Lib\webdrivers\chromedriver')

		with open("edx_urls.txt", "r") as f:
			for url in f:
				if(url[-2] == '0'):
					url = url[:-2]
				yield Request(url = url[:-1], callback = self.parse_course)
				
	def parse_course(self, response):
		self.driver.get(response.url)
		response = Selector(text = self.driver.page_source)
		
		course = Course()
		
		################# DONE
		course['url'] = self.driver.current_url
		################# DONE
		try:
			course['name'] = response.xpath('//*[@class="text-size-heading"]/text()').extract_first().strip()
		except:
			course['name'] = ""
		#################
		try:
			course['language'] = response.xpath('//*[@data-field="language"]//*[@lang]/text()').extract_first()
		except:
			course['language'] = ""
		################# DONE
		try:
			course['hours_per_week'] = response.xpath('//*[@data-field="effort"]/span/text()').extract()[-1]
		except:
			course['hours_per_week'] = ""
		###############DONE
		try:
			if ('Certificate' in response.xpath('//*[@data-field="price"]/span/text()').extract()[-1]):
				course['has_certificates'] = "TRUE"
			else:
				course['has_certificates'] = "FALSE"
		except:
			course['has_certificates'] = ""
		################# DONE
		try:
			course['categories'] = response.xpath('//*[@class = "crumb"]/a//text()').extract()[-1]
		except:
			course['categories'] = ""
		################# DONE
		try:
			course['educator'] = ', '.join(response.xpath('//*[@class="instructor-name"]/text()').extract())
		except:
			course['educator'] = ""
		################# DONE
		try:
			course['organisation_name'] = response.xpath('//*[@data-field="school"]//a/text()').extract_first()
		except:
			course['organisation_name'] = ""
		###### DONE
		try:
			
			if (response.xpath('//*[@class="starts-today"]')):
				course['runs_start_date'] = "NOW"
			elif (response.xpath('//*[@class="course-start"]')):
				course['runs_start_date'] = response.xpath('//*[@class="course-start"]/span/text()').extract_first().rsplit('on ')[-1]
			else:
				course['runs_start_date'] = ""
		except:
			course['runs_start_date'] = ""
		
		################# DONE
		try:
			course['runs_duration_in_weeks'] = re.sub('[^0-9]',"",response.xpath('//*[@data-field = "length"]/span/text()').extract()[-1])
		except:
			course['runs_duration_in_weeks'] = ""
		########
		course['open_for_enrolment'] = 'TRUE'
		################# DONE
		try:
			course['price'] = re.sub('[^0-9,$£]', '', response.xpath('//*[@data-field = "price"]/span/text()').extract()[-1])
		except:
			course['price'] = ""
		#################
		course['industry'] = ""
		################# #######################
		try:
			course['level'] = response.xpath('//*[@data-field = "level"]/span/text()')[-1].extract().strip()
		except:
			course['level'] = ""
		################# DONE
		course['provider'] = "edX"
		################# DONE
		course['skills'] = ""
		################# DONE
		try:
			course['syllabus'] = ', '.join(response.xpath('//*[contains(@class, "syllabus")]//text()').extract()[4:]).strip()
		except:
			course['syllabus'] = ""
		################# DONE
		course['job_title'] = ""
		################# DONE
		course['subject'] = ""
		################# DONE
		course['field_of_study'] = ""
		################# DONE
		try:
			course['about_the_course'] = ' '.join([text.strip() for text in response.xpath('//*[contains(@class, "course-description")]//text()').extract()])
		except:
			course['about_the_course'] = ""
		################# DONE
		try:
			course['description'] = ' '.join([text.strip() for text in response.xpath('//*[contains(@class, "course-intro")]//text()').extract()])
		except:
			course['description'] = ""
		################# DONE
		course['certificate'] = ""
		################# DONE
		course['rating'] = ""
			
		yield course