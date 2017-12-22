# Import the necessary methods from tweepy library
import matplotlib
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import csv

# Variables that contains the user credentials to access Twitter API
access_token = "940848390346301440-yWuVt6HaE23oQ7zfAivKhwoafhei7PY"
access_token_secret = "qjn8NhHAOPNrtYZTa9OI6V48J7i8jn0YUoZotlJ5lnY4C"
consumer_key = "T8CqkMlbjFysouzVQiiPjbU6K"
consumer_secret = "0Disftjr2DWOZFbXru1kgg9twbGkUN4EXnrV59X92sdAzwxz8D"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()

        # Create new file and write row headers
        self.csvname = 'tweets.csv'

        with open(self.csvname, 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(
                ['Tweet', 'Hashtag', 'UserLocation', 'DateCreated'])

    def on_status(self, status):
        if status.retweeted:
            return
        if status.favorite_count is None:
            return
        if status.lang.find('en') < 0:
            return
        if status.entities.get('hashtags') != []:
            self.get_tweets(status)

    def get_tweets(self, status):
        # Save a few parameters into a csv file
        location = status.user.location
        text = status.text
        created = status.created_at
        hashtag = status.entities.get('hashtags')

        print('Tweet arrived ! /n', status.text)

        with open(self.csvname, 'a') as f:
            csvfile = csv.writer(f)
            csvfile.writerow([text, hashtag, location, created])

    def on_error(self, status_code):
        print(status_code)
        return False


if __name__ == '__main__':
    # This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Get current twitter trends
    api = API(auth)
    trends = api.trends_place(1)
    # grab the trends
    trends = trends[0]['trends']
    trendsName = [t['name'] for t in trends]
    print(trendsName)

    stream = Stream(auth, l)
    stream.filter(track=trends)
    # stream.filter(locations=[-180, -90, 180, 90], async=True) ## Get feeds from all over the world
