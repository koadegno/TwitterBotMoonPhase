import datetime
from multiprocessing import connection
from os import environ
from httplib2 import Response
import requests
import tweepy
import MoonPhase
import os
import time


HASHTAG = "#Moon #Lunar #MoonPhases #MoonPhase #MoonHour #TwitterNatureCommunity #night #ORB "
API_KEY = environ['API_KEY']
API_SECRET_KEY = environ['API_SECRET_KEY']

ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

def init_object(api_key,api_secret_key,acces_token,acces_secret_token):
	client = tweepy.Client(consumer_key=api_key,
                    consumer_secret=api_secret_key,
                    access_token=acces_token,
                    access_token_secret=acces_secret_token,return_type=Response)
	year = datetime.datetime.today().year
	moon_object = MoonPhase.MoonPhase(year)
	return client, moon_object

def create_tweet():
	client, moon_object = init_object(API_KEY,API_SECRET_KEY,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

	phase_of_day_txt = moon_object.moon_phase_of_the_day(in_txt=True) + HASHTAG

	print(phase_of_day_txt)
	try:
		response = client.create_tweet(text=phase_of_day_txt)
		print( response)
	except Exception as e:
		if isinstance(e,tweepy.BadRequest): # 400 HTTP ERROR CODE
			print("yo")
			print("too long" in e.api_messages[0])
		elif isinstance(e, requests.exceptions.ConnectionError): # when you do not have connection 
			print("erreur de connection")



create_tweet()