import os, requests
from asknews_sdk import AskNewsSDK
from groq import Groq
from datetime import datetime, timedelta
from openai import OpenAI
from duckduckgo_search import DDGS
from balldontlie import BalldontlieAPI
from .models import Predictions
from tavily import TavilyClient
#from google import genai

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

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
TWEET_MODEL2="meta-llama/llama-4-scout-17b-16e-instruct"
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

system_prompt = f"""You are the world’s foremost AI sportswriter and handicapper, renowned for your sharp wit, incisive analysis, and unshakable confidence. Your predictions are grounded in statistical rigor, historical context, and real-time data. When calculating implied probabilities:  
- **For American odds (positive):** Use the formula `100 / (odds + 100)`.  
- **For American odds (negative):** Use the formula `|odds| / (|odds| + 100)`.  
- **For decimal odds:** Use the formula `1 / decimal_odds * 100%`.  

Example: For -150 odds, the implied probability is `150 / (150 + 100) = 60%`. For +200 odds, it’s `100 / (200 + 100) = 33.33%`.  

Your tone should blend humor and authority, but always prioritize factual accuracy and logical reasoning. Avoid speculative or fabricated information unless explicitly instructed to extrapolate from odds alone."""

prediction_prompt = USER_PROMPT = """Analyze the upcoming using the provided statistical odds and news articles. Your task is to predict the winner while crafting a humorous yet factually accurate analysis. Use the following guidelines:  

1. **Parse the Odds**: Highlight key statistics (e.g., win percentages, player injuries, historical matchups) and explain their relevance.  
2. **Digest the News**: Summarize recent news about each team (e.g., ‘Star player X is recovering from a hamstring injury after tripping over their own shoelaces’).  
3. **Humorous Spin**: Inject jokes, puns, or absurd analogies (e.g., ‘Team A’s defense is so porous, they’d let a breeze score a goal’). Ensure humor enhances clarity, not confusion.  
4. **Prediction**: Conclude with a clear winner based on your analysis, tying together odds, news, and jokes.  

**Tone**: Think of a sports commentator who’s also a stand-up comedian—entertaining but never misleading. Avoid sarcasm that borders on cruelty; keep it lighthearted.  

**Example**:  
*If analyzing a soccer match where Team A’s star striker is injured and Team B’s goalie is a former circus acrobat:*  
‘Team A’s striker is out, tripping over his own ambition last week. Without him, their offense is like a toaster in a bakery—present but useless. Team B’s goalie? A human flywall who once caught a falling elephant (in a circus, not a metaphor). Bet on Team B, unless you’re a fan of dramatic last-minute own goals.’  

Now, apply this to the follwoing matchup.  The article should be ~500 words long.
"""

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
    system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. If the odds are positive, apply this formula: 100/(odds + 100). If the odds are negative, apply this formula: odds/(odds + 100). For our example, as the odds are negative, the implied probability will be 150/(150 + 100) = 60%.  """
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
        newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], string_guarantee_op='OR', string_guarantee=guaranteedWords, premium=True).as_dicts
        #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True).as_dicts
        context = ""
        for article in newsArticles:
            context += article.summary
            image_url = article.image_url
            #print(image_url)
    except:
        max_results = 5
        client = TavilyClient(api_key=TAVILY_API_KEY)
        # For basic search:
        response = client.search(input_text, search_depth="basic")
        # For advanced search:
        #response = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")
        # Get the search results as context to pass an LLM:
        #context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        #context = [{"body": obj["content"]} for obj in response.get("results", [])]
        context = [{"href": obj["url"], "body": obj["content"]} for obj in response.get("results", [])]
        context = str(context)
        #print(context[:20000])
    
     # Construct the system prompt. Feel free to experiment with different prompts.
    
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prediction_prompt + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=10000,
            reasoning_format='hidden'
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prediction_prompt + context + str(oddsJson) + " " + input_text},
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
    
    #print(result)
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
    print(sportKey)
    if "soccer" in sportKey:
        #odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
        #odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/events/{gameId}?apiKey={ODDSAPI_API_KEY}&regions=us&markets=batter_home_runs,batter_first_home_run,batter_hits,batter_total_base,batter_rbis,batter_runs_scored,batter_hits_runs_rbis,batter_singles,batter_doubles,batter_triples,batter_walks,batter_strikeouts,batter_stolen_bases,pitcher_strikeouts,pitcher_record_a_win,pitcher_hits_allowed,pitcher_walks,pitcher_earned_runs,pitcher_outs&oddsFormat=american")
        odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/events/{gameId}/odds?apiKey={ODDSAPI_API_KEY}&regions=us&markets=player_goal_scorer_anytime,player_first_goal_scorer,player_last_goal_scorer,player_to_receive_card,player_to_receive_red_card,player_shots_on_target,player_shots,player_assists&oddsFormat=american")
        odds2 = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    elif "baseball" in sportKey:
        odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/events/{gameId}/odds?apiKey={ODDSAPI_API_KEY}&regions=us&markets=batter_home_runs,batter_first_home_run,batter_hits,batter_total_bases,batter_rbis,batter_runs_scored,batter_hits_runs_rbis,batter_singles,batter_doubles,batter_triples,batter_walks,batter_strikeouts,batter_stolen_bases,pitcher_strikeouts,pitcher_record_a_win,pitcher_hits_allowed,pitcher_walks,pitcher_earned_runs,pitcher_outs&oddsFormat=american")
        odds2 = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    elif "basketball" in sportKey:
        odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/events/{gameId}/odds?apiKey={ODDSAPI_API_KEY}&regions=us&markets=player_points,player_points_q1,player_rebounds,player_rebounds_q1,player_assists,player_assists_q1,player_threes,player_blocks,player_steals,player_blocks_steals,player_turnovers,player_points_rebounds_assists,player_points_rebounds,player_points_assists,player_rebounds_assists,player_field_goals,player_frees_made,player_frees_attempts,player_first_basket,player_first_team_basket,player_double_double,player_triple_double,player_method_of_first_basket&oddsFormat=american")
        odds2 = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    else:
        odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
        odds2 = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    odds2Json = odds2.json()
    response = get_prop(input_text, guaranteedWords, oddsJson, odds2Json)
    # Format and return the response
    return format_response(response)

def get_prop(input_text, guaranteedWords, oddsJson, odds2Json):
    #print(oddsJson)
    #print(odds2Json)
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    #context = ask.news.search_news("player prop bets for " + input_text, method='kw', return_type='string', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_string
    try:
        context = ask.news.search_news("player prop bets for " + input_text, method='kw', return_type='string', n_articles=3, categories=["Sports"], string_guarantee_op='OR', string_guarantee=guaranteedWords, premium=True).as_string
    except:
        max_results = 5
        client = TavilyClient(api_key=TAVILY_API_KEY)
        # For basic search:
        response = client.search(input_text, search_depth="basic")
        # For advanced search:
        #response = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")
        # Get the search results as context to pass an LLM:
        #context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        #context = [{"body": obj["content"]} for obj in response.get("results", [])]
        context = [{"href": obj["url"], "body": obj["content"]} for obj in response.get("results", [])]
        context = str(context)
        #print(context[:20000])
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    #system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate in your predictions.  If the odds are positive, apply this formula: 100/(odds + 100). If the odds are negative, apply this formula: odds/(odds + 100). For our example, as the odds are negative, the implied probability will be 150/(150 + 100) = 60%. If the odds are positive, apply this formula: 100/(odds + 100). If the odds are negative, apply this formula: odds/(odds + 100). For our example, as the odds are negative, the implied probability will be 150/(150 + 100) = 60%. For decimal odds the implied probability is Implied Probability = (1 / Decimal Odds) * 100%  """
    # Make the API call
    response = groq_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Write a humorous prediction for the following matchup.   Include only relevant stats and odds for the game in question. Do not make up any details.  Mention any player prop bets found in the context.  The odds are in JSON format." + context + str(oddsJson) + str(odds2Json) + " " + input_text},
        ],
        temperature=0.3, 
        max_tokens=10000,
        reasoning_format='hidden'
    )

    # Return the API response
    return response

def generate_parlay(input_text, guaranteedWords, gameId, sportKey):
    # Call the OpenAI API to generate the story
    #print(sportKey)
    odds = requests.get(f"https://api.the-odds-api.com/v4/sports/{sportKey}/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDSAPI_API_KEY}&eventIds={gameId}")
    oddsJson = odds.json()
    response = get_parlay(input_text, guaranteedWords, oddsJson)
    # Format and return the response
    return format_response(response)

def get_parlay(input_text, guaranteedWords, oddsJson):
    start = (datetime.now() - timedelta(hours=48)).timestamp()
    end = datetime.now().timestamp()
    input_text = "Same Game Parlays for " + input_text
    #newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], premium=True, start_timestamp=int(start), end_timestamp=int(end)).as_dicts
    try:
        newsArticles = ask.news.search_news(input_text, method='kw', return_type='dicts', n_articles=3, categories=["Sports"], string_guarantee_op='OR', string_guarantee=guaranteedWords, premium=True).as_dicts
        context = ""
        for article in newsArticles:
            context += article.summary
    except:
        max_results = 5
        client = TavilyClient(api_key=TAVILY_API_KEY)
        # For basic search:
        response = client.search(input_text, search_depth="basic")
        # For advanced search:
        #response = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")
        # Get the search results as context to pass an LLM:
        #context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        #context = [{"body": obj["content"]} for obj in response.get("results", [])]
        context = [{"href": obj["url"], "body": obj["content"]} for obj in response.get("results", [])]
        context = str(context)
        #print(context[:20000])
    #print(context)
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Find the best same game parlay bet for the following match. " + prediction_prompt + context + str(oddsJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=10000,
            reasoning_format='hidden'
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Find the best same game parlay bet for the following match. " + prediction_prompt + context + str(oddsJson) + " " + input_text},
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
    try:
        newsArticles = ask.news.search_news("Top News for " + input_text, method='kw', return_type='dicts', n_articles=5, categories=["Sports"], premium=True).as_dicts
        for article in newsArticles:
            context += article.summary
        #print(article.summary)
    except:
        max_results = 5
        client = TavilyClient(api_key=TAVILY_API_KEY)
        # For basic search:
        response = client.search(input_text, search_depth="basic")
        # For advanced search:
        #response = tavily.search(query="Should I invest in Apple in 2024?", search_depth="advanced")
        # Get the search results as context to pass an LLM:
        #context = [{"url": obj["url"], "content": obj["content"]} for obj in response.results]
        #context = [{"body": obj["content"]} for obj in response.get("results", [])]
        context = [{"href": obj["url"], "body": obj["content"]} for obj in response.get("results", [])]
        context = str(context)
        #print(context[:20000])
    #print(context)
    # Construct the system prompt. Feel free to experiment with different prompts.
    #system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty and accurate.  If the odds are positive, apply this formula: 100/(odds + 100). If the odds are negative, apply this formula: odds/(odds + 100). For our example, as the odds are negative, the implied probability will be 150/(150 + 100) = 60%. """
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
    #system_prompt = f"""You are a the worlds greatest AI sportswriter and handicapper. You are smart, funny and witty but very accurate.  """
    # Make the API call
    try:
        response = groq_client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a humorous recap for the following matchup. " + prediction_prompt + context + str(scoresJson) + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=10000,
            reasoning_format='hidden'
        )
    except:
        response = openAI_client.chat.completions.create(
            model=OPENAI_GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a humorous recap for the following matchup. " + prediction_prompt + context + str(scoresJson) + " " + input_text},
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
    print(response)
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
    '''
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
    '''
    response = groq_client.chat.completions.create(
            model=TWEET_MODEL2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Write a funny, sarcastic tweet summarizing the following text. Use funny but approprate hashtags, emojis and tags. Limit your resonse to 150 characters" + " " + input_text},
            ],
            temperature=0.3, 
            max_tokens=500
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
