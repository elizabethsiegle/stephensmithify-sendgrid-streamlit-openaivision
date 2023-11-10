import requests
import os
#langchain==0.0.316 openai==0.28.1
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool, tool
config = dotenv_values(".env")

@tool
def search_statmuse(query: str):
    """Useful for when you need to search Statmuse and parse the webpage for the answer Statmuse has about sports and the NBA based on the input query"""
    URL = f'https://www.statmuse.com/nba/ask?q={query}'
    req = requests.get(URL)

    soup = BeautifulSoup(req.content, features="html.parser")
    #soup2 = BeautifulSoup(requests.get(url).text)
    resp = soup.find("h1")
    return resp

os.environ["OPENAI_API_KEY"] = config.get('OPENAI_API_KEY')
#llm = ChatOpenAI(model_name='gpt-4-32k', temperature=0.2)
llm = ChatOpenAI(temperature=0.2)

tools = load_tools(["llm-math"], llm=llm)
tools = tools + [search_statmuse]

agent = initialize_agent(tools, llm,
agent="zero-shot-react-description", verbose=True, handle_parsing_errors=True)
agent.run(
    "How many 3-point shots is Stephen Curry averaging per game in 2023?"
)