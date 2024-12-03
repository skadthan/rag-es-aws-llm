from utilities import llm_client
from utilities import esclient
from utilities import textutil
import boto3
from utilities import llm_client
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.load.dump import dumps
import json



# Initialize environment and specify the AWS profile name
os.environ["AWS_DEFAULT_REGION"] = boto3.Session().region_name 
session = boto3.Session(profile_name='ai-project')

#Initialize Variables

query = "Who signs the Project Completion Letter?"
vector_store_name = 'ashu-open-search-vector-db'
embdedding_model=llm_client.get_bedrock_embedding_model()
claude_llm=llm_client.get_bedrock_anthropic_claude_llm()
es_client = esclient.get_es_connection()
prompt_template = """Human: Use the following pieces of context to provide a concise answer in English to the question at the end.
      If you don't know the answer, just say that you don't know, don't try to make up an answer. {context} Question: {question} Assistant:"""

def get_vector_store():
    vector_store_name = 'ashu-elastic-search-vector-db'
    es_vector_store = ElasticsearchStore(es_connection=es_client,index_name=vector_store_name,embedding=embdedding_model)
    return es_vector_store

def chat_interface():
    tu = textutil.textcolor()
    print("====================================================================================================================================================")
    print(tu.BOLD +"....................................................Welcome to the Ashu & Ananya's ChatBot! Type 'exit' to end the chat............................."+ tu.END)
    print("====================================================================================================================================================")
    try:
        while True:
            try:
                user_input = input(tu.BOLD +tu.BLUE+"\nYou: "+tu.BLUE+tu.BOLD ).strip()
                # Handle empty input (Enter key)
                if not user_input:
                    print(tu.PURPLE+"ChatBot: I'm still here! Feel free to type something."+tu.PURPLE)
                    continue
                if user_input.lower() == "exit":
                    print(tu.RED+"ChatBot: Goodbye! Have a great day!"+tu.RED)
                    break
                
                # Process user input and generate a response
                response = process_user_input(user_input)
                print(tu.BOLD +tu.GREEN+f"ChatBot: {response}"+tu.GREEN+tu.BOLD)
            except EOFError:
                print(tu.RED+"\nChatBot: Looks like you want to end the chat. Goodbye!"+tu.RED)
                break
    except KeyboardInterrupt:  # Gracefully handle Ctrl+C
        print(tu.RED+"\n\nChatBot: Chat interrupted. See you next time!"+tu.RED)

def process_user_input(user_input):
    # Example response logic (you can replace this with your own logic or model inference)
    docsearch = get_vector_store()
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    qa_prompt = RetrievalQA.from_chain_type(
        llm=claude_llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    #result = qa_prompt({"query": user_input})
    result = qa_prompt.invoke({"query": user_input})
    ai_response=dumps(result, pretty=True)
    ai_response=json.loads(ai_response)
    #print("Human Query: ", ai_response["query"])
    #print("\nAI Response: ", ai_response["result"])
    return ai_response["result"]


def main():
    chat_interface()
    
if __name__ == "__main__":
    main()