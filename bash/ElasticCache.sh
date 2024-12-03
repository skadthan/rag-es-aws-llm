#ElasticCache - Local Installation using Docker.


#Pull the docker images
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.12.2
docker pull docker.elastic.co/kibana/kibana:8.12.2


#Create a local Docker network
docker network create ashu-elastic-ntwk

#Run the local Docker image
docker run -d --name ashu-elasticsearch --net ashu-elastic-ntwk -p 9200:9200 -p 9300:9300 -m 1GB -e "discovery.type=single-node" -e "ELASTIC_PASSWORD=Ashu#123" docker.elastic.co/elasticsearch/elasticsearch:8.12.2

#Run the Kibana Dashboard
docker run -d --name ashu-kibana --net ashu-elastic-ntwk -p 5601:5601 docker.elastic.co/kibana/kibana:8.12.2



PUT /movies
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "genre": {
        "type": "keyword"
      },
      "release_year": {
        "type": "integer"
      },
      "title_embedding": {
        "type": "dense_vector",
        "dims": 1536
      }
    }
  }
}



openssl s_client -connect localhost:9200 -servername localhost -showcerts </dev/null 2>/dev/null | openssl x509 -fingerprint -sha256 -noout -in /dev/stdin

SHA256 Fingerprint=48:DA:5E:B4:A2:E7:59:29:DF:FC:5A:9A:B6:72:50:E4:D1:58:1F:0B:6E:2B:EE:1B:CE:23:A2:79:B9:46:DD:5D



#create Virtual Python environment

python3 -m venv elasticsearch-vectordb    

source .elasticsearch-vectordb






#Olla API Example with Stream

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?"
}'

#Olla API without stream

curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'

