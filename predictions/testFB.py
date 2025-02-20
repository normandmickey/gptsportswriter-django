import os
import facebook as fb
from dotenv import load_dotenv

load_dotenv(override=True)
FACEBOOK_ACCESS_TOKEN=os.environ.get("FACEBOOK_ACCESS_TOKEN")

api=""
print(FACEBOOK_ACCESS_TOKEN)
gptsportswriterapi=fb.GraphAPI(FACEBOOK_ACCESS_TOKEN)
gptsportswriterapi.put_object("me","feed",message="Test post for GPTSportsWriter",link="https://www.gptsportswriter.com")
print("post is done")