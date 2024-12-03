from elasticsearch import Elasticsearch

def get_es_connection():
    es_client = Elasticsearch(
        "https://localhost:9200",
        ssl_assert_fingerprint='48:DA:5E:B4:A2:E7:59:29:DF:FC:5A:9A:B6:72:50:E4:D1:58:1F:0B:6E:2B:EE:1B:CE:23:A2:79:B9:46:DD:5D',
        basic_auth=("elastic", "Ashu#123")
        )
    return es_client