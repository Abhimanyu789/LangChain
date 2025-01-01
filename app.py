import json
import os
import sys
import boto3
import streamlit as st

## We will be using Titan Embeddings Model to generate embeddings for the input text

from langchain_community.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock

## Data Ingestion
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader, TextLoader

## Vector Embedding and Vector Store
from langchain.vectorstores import FAISS

##LLM Models
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

## Bedrock Client
bedrock = boto3.client(service_name='bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id='amazon.titan-embed-text-v2:0',client=bedrock)

## Data Ingestion
def data_ingestion():
    loader= PyPDFDirectoryLoader("data")
    documents = loader.load()

    # In  this case, we are using Character Text Splitter, which works better with PDFs

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    docs=text_splitter.split_documents(documents)

    return docs


## Vector Embedding Generation and Vector Store

def get_vector_store(docs):
    vectorstore_FAISS = FAISS.from_documents(docs,bedrock_embeddings)

    vectorstore_FAISS.save_local("faiss_index")

def get_claude_llm():
    ##Create a Claude LLM,Anthropic's retrieval model
    llm= Bedrock(model_id='anthropic.claude-v2',client=bedrock,model_kwargs={'max_tokens_to_sample':512})

    return llm

def get_llama2_llm():
    ##Create a Meta LLM,LLama2's retrieval model
    llm= Bedrock(model_id='meta.llama3-8b-instruct-v1:0',client=bedrock,model_kwargs={'max_gen_len':512})

    return llm

prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


def get_response_llm(llm,vectorstore_faiss,query):
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer = qa({"query": query})
    return answer['result']


def main():
    st.set_page_config("Chat with PDF")
    
    st.header("Chat with PDFs using AWS Bedrock")

    user_question = st.text_input("Ask a Question from the PDF Files")

    with st.sidebar:
        st.title("Update Or Create Vector Store:")
        
        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Done")

    if st.button("Claude Output"):
        with st.spinner("Processing..."):
            faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
            llm=get_claude_llm()
            
            #faiss_index = get_vector_store(docs)
            st.write(get_response_llm(llm,faiss_index,user_question))
            st.success("Done")

    if st.button("Llama2 Output"):
        with st.spinner("Processing..."):
            faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings)
            llm=get_llama2_llm()
            
            #faiss_index = get_vector_store(docs)
            st.write(get_response_llm(llm,faiss_index,user_question))
            st.success("Done")

if __name__ == "__main__":
    main()