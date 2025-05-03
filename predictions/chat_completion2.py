import os, requests
from asknews_sdk import AskNewsSDK
from groq import Groq
from datetime import datetime, timedelta
from openai import OpenAI
openAI_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#GPT_MODEL=  "llama-3.3-70b-versatile"
GPT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
TWEET_MODEL="llama-3.3-70b-versatile"
#OPENAI_GPT_MODEL = "gpt-4o"
OPENAI_GPT_MODEL = "o3-mini"
ASKNEWS_CLIENT_ID = os.environ.get('ASKNEWS_CLIENT_ID')
ASKNEWS_CLIENT_SECRET = os.environ.get('ASKNEWS_CLIENT_SECRET')
ODDSAPI_API_KEY = os.environ.get('ODDSAPI_API_KEY')

ask = AskNewsSDK(
        client_id=ASKNEWS_CLIENT_ID,
        client_secret=ASKNEWS_CLIENT_SECRET,
        scopes=["news"]
)

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def generate_news(input_text, string_guarantee):
    # Call the OpenAI API to generate the story
    #print("input text: " + input_text)
    response = get_news(input_text, string_guarantee)
    # Format and return the response
    return format_response(response)

def get_news(input_text, string_guarantee):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    print("top News input: " + str(input_text))
    print("top News string guarantee: " + str(string_guarantee))
    context=""
    #newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end), string_guarantee=string_guarantee).as_dicts
    newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=3, categories=["Finance"], premium=True).as_dicts
    for article in newsArticles:
        context += article.summary
        #print(article.summary)
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a stock market analyst. You are intelligent and accurate in your predictions.  """
    # Make the API call
    #print(context)
    response = groq_client.chat.completions.create(
    model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a summary of the following context include details from the articles.  Limit your response to only the stock mentioned in the question.  Give your recommendation to buy sell or hold the stock in question. " + context + input_text},
        ],
        temperature=0.3, 
        max_tokens=2000
    )
    #response = openAI_client.chat.completions.create(
    #model=OPENAI_GPT_MODEL,
    #    messages=[
    #        {"role": "system", "content": system_prompt},
    #        {"role": "user", "content": "Write a summary of the following context include details from the articles. Limit your response to only the stock mentioned in the question. Give your recommendation to buy sell or hold the stock in question.  " + context + input_text},
    #    ],
    #)
    return response



def format_response(response):
    # Extract the generated story from the response
    prediction = response.choices[0].message.content
    # Remove any unwanted text or formatting
    prediction = prediction.strip()
    # Return the formatted story
    return prediction

print(generate_news("paychex stock trend", "payx"))