import tweepy
import time
import config  # File where all keys are present

'''
Before we run the twitter api, twitter needs to know who is using this api, i.e. twitter needs authentication
For this tweepy has OAuth1UserHandler class which accepts app keys 
(consumer_key, consumer_secret, access_token, access_token_secret) and authenticates us to use the twitter api
'''
# ConsumerKey: API Key
# ConsumerSecret: API Key Secret


auth = tweepy.OAuth1UserHandler(
    config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret
)  # This returns an OAuth1UserHandler object which can be used to access the api

api = tweepy.API(auth)  # The OAuth1UserHandler Object generated from keys is passed to the API class.
# If authentication is successful then api object is returned

public_tweets = api.home_timeline()  # This returns tweets from your home timeline
for tweet in public_tweets:
    print(tweet.text)

user = api.verify_credentials()  # Returns the information about the user as an user class object.
print(user)
print(user.name)  # Prints the name of user
print(user.screen_name)  # prints the twitter handle
print(user.followers_count)  # prints the count of followers

# Following the people that follow us(Generous Bot)
'''
tweepy provides us a Cursor class that accepts the 'method to run over api','positional arguments to be passed to api',
'keyword arguments to be passed to api'
On this cursor object we can use .items() to get all the items. We can also provide a limit .items(limit).
Retrieve the items in each page/request
We can also use .pages(limit). Retrieve the page for each request
Cursor provides us an iterator object over the list of items returned
'''
print(tweepy.Cursor(api.get_followers).items())  # This returns an iterator object. When used in for loop, it will
# all the items as for loop automatically calls next()

for follower in tweepy.Cursor(api.get_followers).items():
    print(follower.name)

# For example we have a million followers and we are processing 250 followers per api hit. Then it will take a lot of
# hits. There will be millions of people who will be hitting api simultaneously, which will break the server.
# To avoid this twitter has set a limit on hits per minute. this s called rate limit and tweepy actually allows us
# to work with this rate limit

'''
To solve this we create a generator function which will accept the iterator object and loop over it and call next()
and yeild it until we encounter StopIteration
'''


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.TooManyRequests:
        time.sleep(1)
    except StopIteration:
        pass


for follower in limit_handler(tweepy.Cursor(api.get_followers).items()):
    if follower.name == 'Sangeeta kumari':
        follower.follow()  # Follows the user from the authenticated user account
'''
Working:
First we get the iterator object which is passed to the iterator object. Then the iterator enters the try block. At next
iterator enters the forever while loop, in which yield cursor.next() is executed which pauses the execution of the 
function and returns the value of the iterator to the for loop. Then the execution of the for loop is completed.
After that the control returns to the yield cursor.next() statement. Then we move to the next iteration of the while
loop during which again yield cursor.next(). The same process happens until yield cursor.next() returns StopIteration
exception which ends the code or the TooManyRequests exception which pauses the code for 1 sec

# It is important that a generator function has a loop. If it has a for loop then no need to handle StopIteration
exception. If it is a while loop then we need to handle StopIteration Exception

'''

# Narciscist Bot: A bot that loves your own tweet or loves the tweet based on certain keyword
search_string = 'python'
numberOfTweets = 2

for tweet in tweepy.Cursor(api.search_tweets, search_string).items(numberOfTweets):
    try:
        print(tweet.text)
        tweet.favorite()
        print('I liked that tweet')
    except tweepy.TweepyException as err:
        print(err)

for tweet in tweepy.Cursor(api.search_tweets, search_string).items(numberOfTweets):
    try:
        print(tweet.text)
        tweet.favorite()
        tweet.retweet()
        print('I retweeted that tweet')
    except tweepy.TweepyException as err:
        print(err)
