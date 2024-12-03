from utilities import llm_client
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from requests_aws4auth import AWS4Auth
import warnings
import boto3
import os
import sys
import numpy as np
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from langchain_elasticsearch import ElasticsearchStore
from utilities import esclient

warnings.filterwarnings('ignore')
module_path = ".."
#print('os.path.abspath(module_path): ',os.path.abspath(module_path))
sys.path.append(os.path.abspath(module_path))


# Specify the AWS profile name
os.environ["AWS_DEFAULT_REGION"] = boto3.Session().region_name 
session = boto3.Session(profile_name='default')

# Initialize awsauth, open search parameters, boto clients and llm model 
s3 = session.client('s3')


def store_elastic_search_embeddings(split_data,embedding_model,es_client):
    vector_store_name = 'ashu-elastic-search-vector-db'
    es_vector_store = ElasticsearchStore(es_connection=es_client,index_name=vector_store_name,embedding=embedding_model)
    docsearch = es_vector_store.from_documents(documents=split_data,embedding=embedding_model,index_name=vector_store_name,es_connection=es_client)
    return docsearch

def process_s3_file(bucket_name, file_name,embedding_model, es_client):
    """Process the file: chunk, embed, and store."""
    # Download the file
    local_path = f"/tmp/{file_name.split('/')[-1]}"
    s3.download_file(bucket_name, file_name, local_path)
    print('Downloaded S3 file to local_path: ', local_path)

    # Read file content
    with open(local_path, "r",encoding='UTF-8') as file:
        print(file)
        loader = Docx2txtLoader(local_path)
        document= loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=2000,
        chunk_overlap=200,
        )
        split_data = text_splitter.split_documents(document)
        avg_doc_length = lambda split_data: sum([len(doc.page_content) for doc in split_data])
        len(split_data)
        avg_char_count_pre = avg_doc_length(split_data)
        avg_char_count_post = avg_doc_length(document)
        print(f"Average length among {len(document)} documents loaded is {avg_char_count_pre} characters.")
        print(f"After the split we have {len(split_data)} documents more than the original {len(document)}.")
        print(
            f"Average length among {len(split_data)} documents (after split) is {avg_char_count_post} characters."
        )

    try:
        sample_embedding = np.array(embedding_model.embed_query(split_data[0].page_content))
        modelId = embedding_model.model_id
        print("Embedding model Id :", modelId)
        print("Sample embedding of a document chunk: ", sample_embedding)
        print("Size of the embedding: ", sample_embedding.shape)

    except ValueError as error:
        if  "AccessDeniedException" in str(error):
                print(f"\x1b[41m{error}\
                \nTo troubeshoot this issue please refer to the following resources.\
                \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")      
                class StopExecution(ValueError):
                    def _render_traceback_(self):
                        pass
                raise StopExecution        
        else:
            raise error    

    opensearch_db_index = store_elastic_search_embeddings(split_data,embedding_model,es_client)


def main():
    print('\nHello! Suresh!! Welcome to RAG Experimentaion...!\n')
    bucket_name='ashu-data'
    file_name='test-file.docx'
    model = llm_client.get_bedrock_embedding_model();
    es_client =  esclient.get_es_connection()
    process_s3_file(bucket_name,file_name,model,es_client)

if __name__ == "__main__":
    main()