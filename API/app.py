from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from pydantic import BaseModel

class Config:
    arbitrary_types_allowed = True


load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)

add_routes(
    app,
    ChatOpenAI(model="gpt-4o-mini"),
    path="/openai"
)


model=ChatOpenAI(model="gpt-4o-mini")
##Ollama Gemma:2b
llm=Ollama(model="gemma2:2b")

prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 200 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} for a 10 years child with 100 words")

add_routes(
    app,
    prompt1|model,
    path="/essay"
)

add_routes(
    app,
    prompt2|llm,
    path="/poem"
)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)