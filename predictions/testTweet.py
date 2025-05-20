import tweepy, os
from dotenv import load_dotenv

load_dotenv(override=True)

consumer_key=os.environ.get('TWITTER_API_KEY')
consumer_secret=os.environ.get('TWITTER_API_SECRET')
access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
access_token=os.environ.get('TWITTER_ACCESS_TOKEN')

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret,
    wait_on_rate_limit=False

)

# Create Tweet

# The app and the corresponding credentials must have the Write permission

# Check the App permissions section of the Settings tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps

# Make sure to reauthorize your app / regenerate your access token and secret 
# after setting the Write permission

# Example 1: Create a regular Tweet
response = client.create_tweet(
    text="Test 04082025"
)
print(f"https://twitter.com/user/status/{response.data['id']}")
