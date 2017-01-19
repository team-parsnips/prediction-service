# -*- coding: utf-8 -*-
import scrapy
import json
import sys
from airbnbscrape.items import BnbtutorialItem
from airbnbscrape.predict import Predict

# QUERY = 'Portland-USA'

class BnbspiderSpider(scrapy.Spider):
	name = "airspider"
	allowed_domains = ["airbnb.com"]
	start_urls = ['http://airbnb.com/s/' + 'irvine--USA']
	QUERY = []

	def __init__(self, city='', country='', *args, **kwargs):
		super(BnbspiderSpider, self).__init__(*args, **kwargs)
		# self.QUERY = city + '--' + country

	def parse(self, response):
		#get the last page number on the page
		last_page_number = self.last_pagenumer_in_search(response)
		if last_page_number < 1:
			#abort the search if there are no results
			return
		else:
			page_urls = [response.url + '?page=' + str(pageNumber)
				# for pageNumber in range(1, last_page_number + 1)]
				for pageNumber in range(1,5)]
			for page_url in page_urls:
				yield scrapy.Request(page_url, callback=self.parse_listing_results_page)
	
	def last_pagenumer_in_search(self, response):
		try: # to get the last page number
			last_page_number = int(response
															.xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
															.extract()[0]
															.split('page=')[1]
														)
			return last_page_number
		
		except IndexError: #if there is no page number get the reason from the page
			reason = response.xpath('//p[@class="text-lead"]/text()').extract()
			#and if it contains the key words set last page equal to 0
			if reason and ('find any results that matched your criteria' in reason[0]):
				logging.log(logging.DEBUG, 'No results on page' + response.url)
				return 0
			else:
				#otherwise we can conclude that the page has results but that there is only one page
				return 1
		
	def parse_listing_results_page(self, response):
		for href in response.xpath('//a[@class="media-photo media-cover"]/@href').extract():
			#get all href of the specified kind and join them to be a valid url
			url = response.urljoin(href)
			#request the url and pass the response to final listings parsing function
			yield scrapy.Request(url, callback=self.parse_listing_contents)

	def parse_listing_contents(self, response):
		item = BnbtutorialItem()
		
		json_array = response.xpath('//meta[@id="_bootstrap-room_options"]/@content').extract()
		if json_array:
			airbnb_json_all = json.loads(json_array[0])
			airbnb_json = airbnb_json_all['airEventData']
			item['rev_count'] = airbnb_json['visible_review_count']
			item['amenities'] = airbnb_json['amenities']
			item['host_id'] = airbnb_json_all['hostId']
			item['hosting_id'] = airbnb_json['hosting_id']
			item['room_type'] = airbnb_json['room_type']
			item['price'] = airbnb_json['price']
			item['bed_type'] = airbnb_json['bed_type']
			item['person_capacity'] = airbnb_json['person_capacity']
			item['cancel_policy'] = airbnb_json['cancel_policy']
			item['rating_communication'] = airbnb_json['communication_rating']
			item['rating_cleanliness'] = airbnb_json['cleanliness_rating']
			item['rating_checkin'] = airbnb_json['checkin_rating']
			item['satisfaction_guest'] = airbnb_json['guest_satisfaction_overall']
			item['instant_book'] = airbnb_json['instant_book_possible']
			item['accuracy_rating'] = airbnb_json['accuracy_rating']
			item['response_time'] = airbnb_json['response_time_shown']
			item['response_rate'] = airbnb_json['response_rate_shown']   
			item['nightly_price'] = airbnb_json_all['nightly_price']
			item['url'] = response.url
		yield item
	
	def closed (self, reason):
		return
