import os
import requests
import uuid
import redis

from datetime import timedelta
from unidecode import unidecode
from dotenv import load_dotenv
from services.dynamodb import DynamoDb

load_dotenv()

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

dynamo_db = DynamoDb()
redis_cache = redis.Redis()

class GeniusArtist:
    
    # Retorna hits top 10 
    def _get_top_music(self, data_artist_songs):
        list_hits = [unidecode(hit_name['result']['title']) for hit_name in data_artist_songs['hits']]
        return list_hits
    
    # Retorna dados da GENIUS API
    def _get_base_url(self, artist_name):
        try:
            base_url = f"http://api.genius.com/search?q={artist_name}"
            headers = {"Authorization": f'Bearer {ACCESS_TOKEN}'}
            response = requests.get(base_url, headers=headers)                      
            return response.json()['response']
        
        #Caso ocorra algum erro
        except Exception as e:
            raise ValueError(e)
    
    #Pesquisa o artista e faz a inserção dos dados no banco de dados (DynamoDB) e no cache (Redis)
    def _search_artist(self, artist_name, cache):
        try:
            #Verifica se possui o artista no cache
            if cache: 
                #Verifica se o item existe no cache (redis)
                if redis_cache.exists(artist_name):
                    artist_cache = redis_cache.get(artist_name)
                    if artist_cache is not None:
                        return eval(artist_cache)

            #Recebe hists
            hits = self._get_top_music(self._get_base_url(artist_name))

            #ID da transação
            id_transaction = str(uuid.uuid4())
            
            data = {
                "artist_name": artist_name,
                "hits": hits,
                "id_transaction": id_transaction
            }

            #Realiza o insert no banco de dados e no cache
            dynamo_db._insert_artist(artist_name, id_transaction, hits)

            #Caso o cache seja 'False', limpa cache e atualiza banco de dados
            if redis_cache.exists(artist_name):
                redis_cache.delete(artist_name)
            
            #Insere dados e realiza a remoção após 7 dias
            redis_cache.set(artist_name, str(data))
            redis_cache.expire(artist_name, timedelta(days=7))

            return data

        #Caso ocorra algum erro
        except Exception as e:
            raise ValueError(e)
