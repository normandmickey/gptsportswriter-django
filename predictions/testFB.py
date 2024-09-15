import facebook as fb

api=""
gptsportswriterapi=fb.GraphAPI(api)
gptsportswriterapi.put_object("me","feed",message="Test post for GPTSportsWriter",link="https://www.gptsportswriter.com")
print("post is done")