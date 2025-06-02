import os, requests
from asknews_sdk import AskNewsSDK
from groq import Groq
from datetime import datetime, timedelta
from openai import OpenAI
from duckduckgo_search import DDGS
openAI_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ddgs = DDGS()

GPT_MODEL= "llama-3.3-70b-versatile"
GPT_MODEL2= "meta-llama/llama-4-maverick-17b-128e-instruct"
TWEET_MODEL="llama-3.3-70b-versatile"
OPENAI_GPT_MODEL = "gpt-4o"
#OPENAI_GPT_MODEL = "o3-mini"
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

def search_internet(query):
    try:
        results = ddgs.text(query, max_results=5)
        # Filter out irrelevant results
        filtered_results = [result for result in results if 'body' in result]
        return filtered_results
    except Exception as e:
        print(f"Error searching internet: {e}")
        return []
    
def generate_odds(input_text, guaranteedWords, gameId, sportKey):
    # Call the OpenAI API to generate the story
    #sport = "baseball_mlb"
    #print(sportKey)
    odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    #print(oddsJson)
    response = get_odds(input_text, oddsJson)
    # Format and return the response
    return format_response(response)

def generate_prediction(input_text, guaranteedWords, gameId, sportKey):
    # Call the OpenAI API to generate the story
    #sport = "baseball_mlb"
    #print(sportKey)
    odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    #print(oddsJson)
    response = get_prediction(input_text, guaranteedWords, oddsJson)
    # Format and return the response
    return format_response(response)

def get_odds(input_text, oddsJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    context = ""
    try: 
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        #print(str(newsArticles))
        #context = str(newsArticles)
        search_results = search_internet(input_text)
        context = "\n".join([result['body'] for result in search_results])
        print(context)
    except:
        context = ""
     
  
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL2,
            messages=[
                {"role": "system", "content": system_prompt},
                #{"role": "user", "content": "Write a humorous, sarcastic prediction for the following matchup.  Include only relevant stats and odds for the game in question note any injiries or significant players. You must pick a best bet based on the context provided take into account that underdogs win about 41 percent of the time in baseball and hockey, 35 percent in football and 25 percent in baskeball. Do not make up any details." + context + str(oddsJson) + " " + input_text},
                {"role": "user", "content": "Write a brief report summarizing the following odds and articles and make a prediction.  Include links to references. Format your response in HTML, links should open in new window. " + context + " " + str(oddsJson) + " " + input_text},
            ],
            temperature=0, 
            max_tokens=1000
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "write a brief report summarizing the following odds and articles and make a prediction. Include links to references. Format your response in HTML, links should open in new window. " + context + " " + str(oddsJson) + " " + input_text},  
            ],
            temperature=0.1, 
            max_tokens=1000
        )
        #print("gpt4o")

    # Return the API response
    return response


def get_prediction(input_text, guaranteedWords, oddsJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    context = ""
    try: 
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
        newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        context = ""
        for article in newsArticles:
            context += article.summary
    except:
        context = ""
    
     
  
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and sarcastic but very accurate and confident in your predictions.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                #{"role": "user", "content": "Write a humorous, sarcastic prediction for the following matchup.  Include only relevant stats and odds for the game in question note any injiries or significant players. You must pick a best bet based on the context provided take into account that underdogs win about 41 percent of the time in baseball and hockey, 35 percent in football and 25 percent in baskeball. Do not make up any details." + context + str(oddsJson) + " " + input_text},
                {"role": "user", "content": "Write a humorous, prediction for the following matchup.  Include only relevant stats and odds for the game in question note any injuries or significant players. You must pick a best bet based on the context provided, odds and statistics. Do not make up any details." + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a humorous prediction for the following matchup.  Give your best bet based on the context provided.  Include only relevant stats and odds for the game in question. Do not make up any details." + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
        #print("gpt4o")

    # Return the API response
    return response

def generate_prop(input_text, guaranteedWords, gameId, sportKey):
    # Call the OpenAI API to generate the story
    #sport = "baseball_mlb"
    #print(sportKey)
    odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    #print(oddsJson)
    response = get_prop(input_text, guaranteedWords, oddsJson)
    # Format and return the response
    return format_response(response)

def get_prop(input_text, guaranteedWords, oddsJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    #context = ask.news.search_news("player prop bets for " + input_text, method='kw', return_type='string', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_string
    context = ask.news.search_news("player prop bets for " + input_text, method='kw', return_type='string', n_articles=3, categories=["Sports"], premium=True).as_string
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate in your predictions.  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a humorous prediction for the following matchup.   Include only relevant stats and odds for the game in question. Do not make up any details.  Mentions any player prop bets found in the context." + context + str(oddsJson) + " " + input_text},
        ],
        temperature=0.3, 
        max_tokens=1000
    )

    # Return the API response
    return response

def generate_parlay(input_text, gameId, sportKey):
    # Call the OpenAI API to generate the story
    #print(sportKey)
    odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    response = get_parlay(input_text, oddsJson)
    # Format and return the response
    return format_response(response)

def get_parlay(input_text, oddsJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    input_text = "Same Game Parlays for " + input_text
    #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
    newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
    context = ""
    for article in newsArticles:
        context += article.summary
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate in your predictions.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Find the best same game parlay bet for the following match.  Include only relevant stats and odds for the game in question. Do not make up any details." + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Find the best same game parlay bet for the following match.  Include only relevant stats and odds for the game in question. Do not make up any details." + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
        #print("gpt4o")


     # Return the API response
    return response

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
    newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=5, categories=["Sports"], premium=True).as_dicts
    for article in newsArticles:
        context += article.summary
        print(article.summary)
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty and accurate.  """
    # Make the API call
    #print(context)
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a summary of the following articles. Be funny and sarcastic. " + context + input_text},
            ],
            temperature=0.3, 
            max_tokens=2000
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a summary of the following articles. Be funny and sarcastic. " + context + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
        #print("gpt4o")
        # Return the API response
    return response

def generate_videoText(input_text):
    # Call the OpenAI API to generate the story
    #print("input text: " + input_text)
    response = get_news(input_text, "string_guarantee")
    # Format and return the response
    return format_response(response)

def get_videoText(input_text):
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate in your predictions.  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Rewrite the following article in a humorous way, keep it under 100 words.  Start out by telling the listener to smash the like and subscribe buttons in a funny way that's related to the sport mentioned." + input_text},
        ],
        temperature=0.3, 
        max_tokens=200
    )


    # Return the API response
    return response


def generate_recap(input_text, string_guarantee, gameId, sportKey):
    # Call the OpenAI API to generate the story
    scores = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/scores/?daysFrom=2&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    scoresJson = scores.json()
    #print(scoresJson)
    response = get_recap(input_text, string_guarantee, scoresJson)
    # Format and return the response
    return format_response(response)

def get_recap(input_text, string_guarantee, scoresJson):
    start = (datetime.now() - timedelta(hours=12)).timestamp()
    end = datetime.now().timestamp()
    #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end), string_guarantee=string_guarantee).as_dicts
    newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
    context = ""
    for article in newsArticles:
        context += article.summary
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a humorous recap for the following matchup.  Include only relevant stats and odds for the game in question do not make up any details." + context + str(scoresJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a humorous recap for the following matchup.  Include only relevant stats and odds for the game in question do not make up any details." + context + str(scoresJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )


    # Return the API response
    return response

def generate_tweet(input_text):
    #print(input_text)
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
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate and write like a sports betting bro.  """
    # Make the API call
    #response = groq_client.chat.completions.create(
    response = openAI_client.chat.completions.create(
        #model=TWEET_MODEL,
        model=OPENAI_GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a funny, sarcastic tweet summarizing the following text. Use funny but approprate hashtags, emojis and tags. Limit your resonse to 150 characters" + " " + input_text},
        ],
        temperature=0.3, 
        max_tokens=200
    )

    # Return the API response
    #print(response)
    return response


def format_response(response):
    # Extract the generated story from the response
    prediction = response.choices[0].message.content
    # Remove any unwanted text or formatting
    prediction = prediction.strip()
    # Return the formatted story
    #print(prediction)
    return prediction

def generate_slide_content(topic):
    prompt = f"""
Create a PowerPoint presentation on the topic: "{topic}".
Structure output exactly like this:

Slide 1 Title: <title>
Slide 1 Content: <bullet1>\n<bullet2>\n<bullet3>

Slide 2 Title: ...
..."""
    response = openAI_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    #return response['choices'][0]['message']['content']
    return response.choices[0].message.content
