import os, requests
from asknews_sdk import AskNewsSDK
from groq import Groq
from datetime import datetime, timedelta
from openai import OpenAI
from duckduckgo_search import DDGS
from balldontlie import BalldontlieAPI
from .models import Predictions
#from google import genai

openAI_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ddgs = DDGS()

bdl_api = BalldontlieAPI(api_key=os.environ.get("BDL_API_KEY"))
#print(bdl_api.mlb.teams.list())

#gi_client = genai.Client(api_key=os.environ.get("GI_API_KEY"))

#GPT_MODEL= "meta-llama/llama-4-scout-17b-16e-instruct"
GPT_MODEL2= "llama-3.1-8b-instant"
#GPT_MODEL="deepseek-r1-distill-llama-70b"
GPT_MODEL="qwen/qwen3-32b"
RESULT_MODEL= "llama-3.3-70b-versatile"
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
    scoreJson = ""
    oddsJson = ""
    try:
        odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
        oddsJson = odds.json()
    except:
        oddsJson = ""
    print(oddsJson)

    try: 
        score = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/scores/?apiKey={ODDSAPI_API_KEY}&eventIds={gameId}&daysFrom=3")
        scoreJson = score.json()
    except:
        scoreJson = ""
    #print(scoreJson)
    #print(oddsJson)
    response = get_odds(input_text, oddsJson, scoreJson)
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

def get_odds(input_text, oddsJson, scoreJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    context = ""
    #try: 
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        #print(str(newsArticles))
        #context = str(newsArticles)
        #search_results = search_internet(input_text)
        #context = "\n".join([result['body'] for result in search_results])
        #print(context)
    #    context = ""
    #except:
     #   context = ""
     
  
    # Construct the system prompt. Feel free to experiment with different prompts.
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL2,
            messages=[
                {"role": "system", "content": system_prompt},
                #{"role": "user", "content": "Write a humorous, sarcastic prediction for the following matchup.  Include only relevant stats and odds for the game in question note any injiries or significant players. You must pick a best bet based on the context provided take into account that underdogs win about 41 percent of the time in baseball and hockey, 35 percent in football and 25 percent in baskeball. Do not make up any details." + context + str(oddsJson) + " " + input_text},
                {"role": "user", "content": "Write a brief report summarizing the following odds, report the score and last update date and time if available. Do not make up any facts just use those presented to you.   " + context + " " + str(oddsJson) + " Current Score: " + str(scoreJson) + " " + input_text},
            ],
            temperature=0, 
            max_tokens=500,
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "write a brief report summarizing the following odds, report the score and last update date and time if available.  Do not make up any facts just use those presented to you.  " + context + " " + str(oddsJson) + " Current Score: " + str(scoreJson) + " " + input_text},  
            ],
            temperature=0, 
            max_tokens=500,
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
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], string_guarantee_op='OR', string_guarantee=guaranteedWords, premium=True).as_dicts
        newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        context = ""
        for article in newsArticles:
            context += article.summary
        #print(context)
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
                #{"role": "user", "content": "Provide a humorous and sarcastic prediction for the upcoming matchup, including relevant statistics and odds. Highlight any notable injuries or key player information. Based on the provided context, make a informed best bet, taking into account the historical underdog win rates across different sports: 41% in baseball and hockey and Soccer, 35% in NFA football and MMA, 32% in NBA basketball, 26% in NCAA Basketball, 22% in NCAA Football and 30% in Tennis. Ensure that all information is accurate and not fabricated." + context + str(oddsJson) + " " + input_text},
                {"role": "user", "content": "Provide a witty and tongue-in-cheek analysis of the upcoming matchup, complete with relevant statistics and odds. Highlight any significant injuries or key player updates that might impact the game's outcome. Based on the context, make a data-driven best bet, considering the historical trends and win rates of various teams and players across different sports. For reference, the overall underdog win rates are: 41% in baseball, hockey, and soccer; 35% in NFL football and MMA; 32% in NBA basketball; 26% in NCAA basketball; 22% in NCAA football; and 30% in tennis. Ensure that all information is accurate, up-to-date, and not made up on the spot.  If there is no information about the match requests make a prediction based only on the odds provided. Calculate the Odds Expected Value, , split the diffrence between the calculated probability and underdog win rate. Your best be should be one with the best expected value and most likely outcome. " + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=4000,
            reasoning_format='hidden'
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Provide a witty and tongue-in-cheek analysis of the upcoming matchup, complete with relevant statistics and odds. Highlight any significant injuries or key player updates that might impact the game's outcome. Based on the context, make a data-driven best bet, considering the historical trends and win rates of various teams and players across different sports. For reference, the overall underdog win rates are: 41% in baseball, hockey, and soccer; 35% in NFL football and MMA; 32% in NBA basketball; 26% in NCAA basketball; 22% in NCAA football; and 30% in tennis. Ensure that all information is accurate, up-to-date, and not made up on the spot.  If there is no information about the match requests make a prediction based only on the odds provided.   Calculate the Odds Expected Value, split the diffrence between the calculated probability and underdog win rate. your best be should be one with the best expected value and most likely outcome. " + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=1000
        )
        #print("gpt4o")

    # Return the API response
    #generate_audio(response.choices[0].message.content)
    return response

def get_results(prediction, title, gameId, sportKey):
    try:
        newsArticles = ask.news.search_news(title, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        context = ""
        for article in newsArticles:
            context += article.summary
    except:
        context = ""
    
    try: 
        score = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/scores/?apiKey={ODDSAPI_API_KEY}&eventIds={gameId}&daysFrom=3")
        scoreJson = score.json()
    except:
        scoreJson = ""
    
    response = groq_client.chat.completions.create(
        model=RESULT_MODEL,
        messages=[
            {"role": "system", "content": "you are a data analyst"},
            {"role": "user", "content": "Determine if the prediction made in the following context was accurate or not based on the context. Return only the prediction, outcome and score and whether the bet would have won or lost (win/lose) if it was accurate" + "Prediction: " + prediction + "Context: " + context + "Score: " + str(scoreJson)},
        ],
        temperature=0, 
        max_tokens=1000
    )

    result = response.choices[0].message.content
    #update boolean field
    response = groq_client.chat.completions.create(
        model=RESULT_MODEL,
        messages=[
            {"role": "system", "content": "you are a data analyst"},
            {"role": "user", "content": "analyze the following text and return just a Boolean response;  True if win, False if lose and None if undetermined. Text: " + result},
        ],
        temperature=0, 
        max_tokens=1000
    )
    bool = response.choices[0].message.content

    try:
        my_object = Predictions.objects.get(id=gameId)
        my_object.results = result
        my_object.won = bool
        my_object.save()
    except:
        print(bool)
    
    print(result)
    return(result)

def generate_audio(text):
    speech_file_path = "speech2.mp3" 
    model = "playai-tts"
    voice = "Fritz-PlayAI"
    text = text
    response_format = "mp3"

    response = groq_client.audio.speech.create(
    model=model,
    voice=voice,
    input=text,
    response_format=response_format
    )

    response.write_to_file(speech_file_path)

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
        max_tokens=4000,
        reasoning_format='hidden'
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
            max_tokens=4000,
            reasoning_format='hidden'
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
    #print("top News input: " + str(input_text))
    #print("top News string guarantee: " + str(string_guarantee))
    context=""
    #newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end), string_guarantee=string_guarantee).as_dicts
    newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=5, categories=["Sports"], premium=True).as_dicts
    for article in newsArticles:
        context += article.summary
        #print(article.summary)
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
            max_tokens=4000,
            reasoning_format='hidden'
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
            max_tokens=4000,
            reasoning_format='hidden'
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
    print(response)
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
