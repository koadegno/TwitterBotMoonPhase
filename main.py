from os import environ
import tweepy
import os



API_KEY = environ['API_KEY']
API_SECRET_KEY = environ['API_SECRET_KEY']

ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']


def create_tweet():
	
	client = tweepy.Client(consumer_key=API_KEY,
                    consumer_secret=API_SECRET_KEY,
                    access_token=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET)

	tweet = ["Hello World" for i in range( 40)]
	mot = ""
	for i in range(len(tweet)):
		mot = mot+tweet[i]
	try:
		response = client.create_tweet(text=mot)
		print( response)
	except Exception as e:
		print(e)

create_tweet()