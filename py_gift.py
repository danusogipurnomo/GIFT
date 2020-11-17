__author__ = 'Danu Sogi Purnomo'
__date__ = '20201117'
__description__ = 'This library is for crawl image in tweets'
__version__ = "0.0.2"

import os
import tweepy
import urllib
import json


class pyGIFT:
    def __init__(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.api = self.create_tweepy_object()

    def create_tweepy_object(self):
        filename = 'twitter-token.json'
        filepath = os.path.join(self.basepath, filename)
        with open(filepath) as json_file:
            twitter_token = json.load(json_file)
        try:
            auth = tweepy.OAuthHandler(twitter_token['consumer_key'], twitter_token['consumer_secret'])
            auth.set_access_token(twitter_token['access_token'], twitter_token['access_token_secret'])

            api = tweepy.API(auth)
        except Exception as e:
            print(e)
            api = None

        return api

    def search_image(self, max_tweet):
        path_file = os.path.dirname(__file__)
        os.system("mkdir " + self.user_screen_name)
        path_new = os.path.join(path_file, self.user_screen_name)
        flags = 1

        if isinstance(max_tweet, str):
            if max_tweet.lower().strip() == "all":
                max_tweet = self.user_statuses_count
            else:
                flags = 0
        elif isinstance(max_tweet, int):
            if max_tweet > self.user_statuses_count:
                max_tweet = self.user_statuses_count
            elif max_tweet <= 0:
                flags = 0

        if flags == 1:
            count = 0
            for status in tweepy.Cursor(self.api.user_timeline, screen_name=self.user_screen_name, include_entities=True).items(max_tweet):
                count += 1
                media = status.entities.get('media', [])
                if len(media) > 0:
                    media = media[0]['media_url']
                    filename = media.split('/')[-1]
                    urllib.request.urlretrieve(media, os.path.join(path_new, filename))
                    print ('Tweet ' + str(count) + ' Has An Image - ' + filename)
                else:
                    print ('Tweet ' + str(count) + ' Has No Image')
        else:
            print("Invalid argument of max_tweet")

    def main(self, username, max_tweet):
        if self.api:
            try:
                user = self.api.get_user(username)

                self.user_id = user.id_str
                self.user_screen_name = user.screen_name
                self.user_name = user.name
                self.user_statuses_count = user.statuses_count

                print("User ID          : ", self.user_id)
                print("Username         : ", self.user_screen_name)
                print("Name             : ", self.user_name)
                print("Statuses Count   : ", self.user_statuses_count)

                self.search_image(max_tweet)

            except Exception as error :
                print(error)


if __name__ == "__main__":
    obj = pyGIFT()
    obj.main("twitter", 300)

    # NOTES
    # Above example is to get images in 100 tweets of account "BillGates".
    # If you want to get all images in all tweets,
    # then change 100 into "all" (with quotation marks).
