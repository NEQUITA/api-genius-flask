from flask import Flask, request, jsonify
from services.geniusartist import GeniusArtist

app = Flask(__name__)

artist = GeniusArtist()

#Rota da API
@app.route("/api/artist/<artist_name>")
def get_artist(artist_name):
    try:
        #Padronizando string com nome do artista
        artist_name = artist_name.title().strip()

        #Verificando cache
        cache_param = request.args.get('cache')
        cache = False if cache_param is not None and cache_param == 'False' else True

        #Gerando top 10 do artista
        data = artist._search_artist(artist_name, cache)
        
        return data

    #Caso ocorra algum erro
    except Exception as e:
        raise ValueError(e)

#Executa o app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)