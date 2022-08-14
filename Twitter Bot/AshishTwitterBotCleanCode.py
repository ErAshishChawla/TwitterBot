import tweepy
import config
import time
import re


class InvalidInput(Exception):
    pass


###########################################################################################################
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.TooManyRequests:
        time.sleep(1)
    except StopIteration:
        pass


def my_details(me):
    print(f'Hi My name is {me.name} and my twitter handle is {me.screen_name}')


def like_tweets(api, tweets_to_like, keyword):
    for tweet in limit_handler(tweepy.Cursor(api.search_tweets, keyword).items(tweets_to_like)):
        tweet.favourite()
        print(f'''
username : @{tweet.user.screen_name}
Tweet you liked:
{tweet.text}
''')


def retweet_tweets(api, tweets_to_retweets, keyword):
    for tweet in limit_handler(tweepy.Cursor(api.search_tweets, keyword).items(tweets_to_retweets)):
        tweet.retweet()
        print(f'''
username : @{tweet.user.screen_name}
Tweet you retweeted:
{tweet.text}
''')


def follow_users(api, count_to_follow, username_for_followers_list=None):
    for follower in limit_handler(
            tweepy.Cursor(api.get_followers, screen_name=username_for_followers_list).items(count_to_follow)):
        follower.follow()
        print(f'You followed @{follower.screen_name}')


##############################################################################################

def print_bot_console():
    print('The following operations can be performed:')
    print('1. Follow people from someones twitter handle.')
    print('2. Follow people who follow you.')
    print('3. Like a tweet based on some word.')
    print('4. Retweet a tweet based on some word.')
    print('')


def to_continue_program():
    to_continue = input('Do you want to run the bot again(Yes/No)?')
    if to_continue == 'yes':
        return main(0)
    elif to_continue.lower() == 'no':
        print('Program ended successfully')
        return 0
    else:
        print('Invalid Input')
        return to_continue_program()


def twitter_bot(api, pattern_for_console_input):
    regex_for_number = r"[\d]"
    pattern_for_number = re.compile(regex_for_number)
    print_bot_console()
    user_response = input('Please enter SRNo of the option you want to execute: ')
    if pattern_for_console_input.fullmatch(user_response):
        if user_response == '1':
            print('')
            print('Executing Option 1')
            user_twitter_handle = input('Please enter the twitter username(without @): ')
            user_details = api.get_user(screen_name=user_twitter_handle)
            users_count = input('Number of users you want to follow: ')
            if pattern_for_number.fullmatch(users_count):
                print(f'@{user_details.screen_name} user found!')
                follow_users(api, int(users_count), username_for_followers_list=user_twitter_handle)
            else:
                raise InvalidInput()

        elif user_response == '2':
            print('')
            print('Executing Option 2')
            users_count = input('Number of users you want to follow back: ')
            if pattern_for_number.fullmatch(users_count):
                follow_users(api, int(users_count))
            else:
                raise InvalidInput()

        elif user_response == '3':
            print('')
            print('Executing Option 3')
            search_keyword = input('Enter the keyword for which tweet is to be liked: ')
            tweet_count = input('Enter number of tweets to be liked')
            if pattern_for_number.fullmatch(tweet_count):
                like_tweets(api, int(tweet_count), search_keyword)
            else:
                raise InvalidInput()
        else:
            print('')
            print('Executing Option 3')
            search_keyword = input('Enter the keyword for which tweet is to be retweeted: ')
            tweet_count = input('Enter number of tweets to be retweeted')
            if pattern_for_number.fullmatch(tweet_count):
                retweet_tweets(api, int(tweet_count), search_keyword)
            else:
                raise InvalidInput()
    else:
        print("Control is here")
        raise InvalidInput()


def main(complete_execution=1):
    try:
        regex_for_console_input = r"[1-4]{1}$"
        pattern_for_console_input = re.compile(regex_for_console_input)
        err_response = 0

        auth = tweepy.OAuth1UserHandler(config.consumer_key, config.consumer_secret, config.access_token,
                                        config.access_token_secret)

        api = tweepy.API(auth)
        if complete_execution == 1:
            # Checking if we logged in by printing user details
            my_details(api.verify_credentials())
            print("Welcome to the twitter bot!!!")

        twitter_bot(api, pattern_for_console_input)

    except AttributeError as err:
        print(f'{err.upper()}! Please try again')
        err_response = 1

    except tweepy.errors.Unauthorized as err:
        print(f'{err.upper()}! Please try again')
        err_response = 1

    except tweepy.errors.NotFound:
        print(f'You entered invalid twitter handle or username! Please try again')
        err_response = 1

    except InvalidInput:
        print('Invalid Input! Please try again')
        err_response = 1
    finally:
        if err_response == 1:
            print('')
            main(0)
        else:
            to_continue_program()


if __name__ == '__main__':
    main(1)
