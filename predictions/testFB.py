import facebook as fb

api="EAAK2IMS7Bb8BOzFdpku70OYqlZCm9fn9CMaQNpBUYJOAuPWeoSi32FWobhHobp3fc3iLOFeKyv8dZCTuhPXHIPIfCe0m1RD08XM2XvYAG3T9LUvckOz6UZCQBtlSgb9TmyqM3AULM7l6MgSbhaL7KB1cvdsk2KQAYNjIM1y8J9hzGb7q1JDQkKMmg8lXOow0ZCGv2LlE0ml2AXZAoV8T9"

gptsportswriterapi=fb.GraphAPI(api)
gptsportswriterapi.put_object("me","feed",message="Test post for GPTSportsWriter",link="https://www.gptsportswriter.com")
print("post is done")