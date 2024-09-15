import facebook as fb

api="EAAK2IMS7Bb8BO9tZCRehUBRP0p0X2oJ0XqXPFPZBMRnqIpO3f4GtzBSuiulzt96ibJvZAY0UqXUyoR9XQ2zLkLRNLmUUuN9012oHB6qQvg1ZCxZAUl8jhl8irLp92jzKGcAIjV3HPx5kFqxRyuH4U3NZAL4xCqddGLJqw15IjFe2ZAYNCZAi3bIuzyXO8EpBskqIMvl0shv8ZCveDVMgqERYV"
gptsportswriterapi=fb.GraphAPI(api)
gptsportswriterapi.put_object("me","feed",message="Test post for GPTSportsWriter",link="https://www.gptsportswriter.com")
print("post is done")