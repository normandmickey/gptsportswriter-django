import facebook as fb

api="EAAK2IMS7Bb8BO4K78mzmgi5sFSolTZCJnINjeA2LPSJJrPPyk1Al1TOtdW5hdWoaVc9zywATgPmw2RewAUjigXLKS7KpqdZBVWP8XHlR3yrvZApwrnQW36fZCL3cIb3v1681EF6uElO0ipkUU3b5HbIC5MTlloxlEjGKsPAaHvDqS1CALOz1F0Fxw66nK59flg9ev2V6yfnmUL0VZCr77"
gptsportswriterapi=fb.GraphAPI(api)
gptsportswriterapi.put_object("me","feed",message="Test post for GPTSportsWriter",link="https://www.gptsportswriter.com")
print("post is done")