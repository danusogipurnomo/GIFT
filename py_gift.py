__author__ = 'Danu Sogi Purnomo'
__date__ = '20161231'
__description__ = 'This library is for crawl image in tweets'
__version__ = "1.0"

import os
import tweepy
import urllib
import json

class pyGIFT:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def search_image(self, max_tweet):
        path_file = os.path.dirname(__file__)
        os.system("mkdir " + self.user_screen_name)
        path_new = os.path.join(path_file, self.user_screen_name)
        flags = 1

        if (isinstance(max_tweet, str)):
            if (max_tweet.lower().strip() == "all"):
                max_tweet = self.user_statuses_count
            else:
                flags = 0
        elif (isinstance(max_tweet, int)):
            if (max_tweet > self.user_statuses_count):
                max_tweet = self.user_statuses_count
            elif (max_tweet <= 0):
                flags=0

        if (flags == 1):
            count = 0
            for status in tweepy.Cursor(self.api.user_timeline, screen_name=self.user_screen_name, include_entities=True).items(max_tweet):
                count += 1
                media = status.entities.get('media', [])
                if (len(media) > 0):
                    media = media[0]['media_url']
                    filename = media.split('/')[-1]
                    urllib.urlretrieve(media, os.path.join(path_new, filename))
                    print 'Tweet ' + str(count) + ' Has An Image - ' + filename
                else:
                    print 'Tweet ' + str(count) + ' Has No Image'
        else:
            print "Invalid argument of max_tweet"

    def main(self, username, max_tweet):
        try :
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)

            self.api = tweepy.API(auth)
            user = self.api.get_user(username)

            self.user_id = user.id_str
            self.user_screen_name = user.screen_name
            self.user_name = user.name
            self.user_statuses_count = user.statuses_count

            print "User ID          : ", self.user_id
            print "Username         : ", self.user_screen_name
            print "Name             : ", self.user_name
            print "Statuses Count   : ", self.user_statuses_count

            self.search_image(max_tweet)

        except Exception as error :
            print error.message[0]["message"]



if __name__ == "__main__":
    # Authentication details. To  obtain these visit dev.twitter.com
    consumer_key            = 'your consumer_key'
    consumer_secret         = 'your consumer_secret'
    access_token            = 'your access_token'
    access_token_secret     = 'your access_token_secret'

    obj = pyGIFT(consumer_key, consumer_secret, access_token, access_token_secret)
    obj.main("BillGates", 100)

    # NOTES
    # Above example is to get images in 100 tweets of account "BillGates".
    # If you want to get all images in all tweets,
    # then change 100 into "all" (with quotation marks).