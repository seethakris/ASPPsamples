# Import the necessary methods from tweepy library
import matplotlib

matplotlib.use('TkAgg')
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import csv

# Variables that contains the user credentials to access Twitter API
access_token = "ENTERHERE"
access_token_secret = "ENTERHERE"
consumer_key = "ENTERHERE"
consumer_secret = "ENTERHERE"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()

        # Create new file and write row headers
        self.csvname = 'twitterfeed.csv'
        with open(self.csvname, 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(
                ['Tweet', 'Hashtag', 'UserLocation', 'LocationX', 'LocationY',
                 'DateCreated', 'NumberofRetweets'])

    def on_status(self, status):
        if status.retweeted:
            return
        if status.favorite_count is None:
            return
        if status.lang.find('en') < 0:
            return

        if status.coordinates is not None and status.entities.get('hashtags') != []:
            x = status.coordinates['coordinates'][0]
            y = status.coordinates['coordinates'][1]

            # Save a few parameters into a csv file
            location = status.user.location
            text = status.text
            created = status.created_at
            retweets = status.retweet_count
            hashtag = status.entities.get('hashtags')

            print('Tweet arrived ! /n', status.text)

            with open(self.csvname, 'a') as f:
                csvfile = csv.writer(f)
                csvfile.writerow([text, hashtag, location, x, y, created, retweets])

    def on_error(self, status_code):
        print(status_code)
        return False


if __name__ == '__main__':
    # This handles Twitter authentification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # stream.filter(track=["trump", "clinton", "hillary clinton", "donald trump"])  ## Get feeds from all over the world
    stream.filter(locations=[-180, -90, 180, 90], async=True)
