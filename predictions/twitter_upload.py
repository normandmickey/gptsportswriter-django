import tweepy, os, re

tweepy_auth = tweepy.OAuth1UserHandler(
    "{}".format(os.environ.get("TWITTER_API_KEY")),
    "{}".format(os.environ.get("TWITTER_API_SECRET")),
    "{}".format(os.environ.get("TWITTER_ACCESS_TOKEN")),
    "{}".format(os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")),
)
tweepy_api = tweepy.API(tweepy_auth)
post = tweepy_api.simple_upload("img.jpg")
text = str(post)
media_id = re.search("media_id=(.+?),", text).group(1)
payload = {"media": {"media_ids": ["{}".format(media_id)]}}
#os.remove("catpic.jpg")
print(payload)