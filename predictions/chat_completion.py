import os
from asknews_sdk import AskNewsSDK
from groq import Groq
from datetime import datetime, timedelta

GPT_MODEL= "llama3-70b-8192"
ASKNEWS_CLIENT_ID = os.environ.get('ASKNEWS_CLIENT_ID')
ASKNEWS_CLIENT_SECRET = os.environ.get('ASKNEWS_CLIENT_SECRET')

ask = AskNewsSDK(
        client_id=ASKNEWS_CLIENT_ID,
        client_secret=ASKNEWS_CLIENT_SECRET,
        scopes=["news"]
)

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def generate_prediction(input_text):
    # Call the OpenAI API to generate the story
    response = get_prediction(input_text)
    # Format and return the response
    return format_response(response)

def get_prediction(input_text):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    context = ask.news.search_news(input_text, method='kw', return_type='string', n_articles=10, categories=["Sports"], start_timestamp=int(start), end_timestamp=int(end)).as_string
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate in your predictions.  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a humorous prediction for the following matchup.  Include only relevant stats and odds for the game in question. Do not make up any details." + context + input_text},
        ],
        temperature=0.3, 
        max_tokens=1000
    )

    # Return the API response
    return response

def generate_recap(input_text):
    # Call the OpenAI API to generate the story
    response = get_recap(input_text)
    # Format and return the response
    return format_response(response)

def get_recap(input_text):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    context = ask.news.search_news(input_text, method='kw', return_type='string', n_articles=10, categories=["Sports"], start_timestamp=int(start), end_timestamp=int(end)).as_string
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate.  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a humorous recap for the following matchup.  Include only relevant stats and odds for the game in question do not make up any details." + context + input_text},
        ],
        temperature=0.3, 
        max_tokens=1000
    )

    # Return the API response
    return response

def generate_tweet(input_text):
    # Call the OpenAI API to generate the story
    response = get_tweet(input_text)
    # Format and return the response
    return format_response(response)

def get_tweet(input_text):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    #context = ask.news.search_news(input_text, method='kw', return_type='string', n_articles=10, categories=["Sports"], start_timestamp=int(start), end_timestamp=int(end)).as_string
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate.  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a 150 character humorous tweet summarizing the follwoing text.  Include only relevant stats and odds for the game in question do not make up any details. Use approprate hashtags and emojis. limit your reply to 150 characters." + " " + input_text},
        ],
        temperature=0.3, 
        max_tokens=200
    )

    # Return the API response
    return response


def format_response(response):
    # Extract the generated story from the response
    prediction = response.choices[0].message.content
    # Remove any unwanted text or formatting
    prediction = prediction.strip()
    # Return the formatted story
    return prediction
