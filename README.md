# Artist Genius API REST com Flask, AWS e Redis
Integração da API Genius com Flask, AWS e Redis.

## Passos para utilizar esta API

1. Clone o repositório

2. Renomeie o arquivo "example.env" para ".env" e configure o mesmo com as chaves de autorização do Genius API e AWS.  

2. Execute a aplicação Flask do lado do servidor no terminal:

    ```sh
    $ python -m venv venv
    $ Ubuntu: source venv/bin/activate 
    or 
    $ Windows: venv\Scripts\activate
    (venv)$ pip install -r requirements.txt
    (venv)$ python app.py
    ```

3. Acesse [http://localhost:5000/api/artist/<artist>](http://localhost:5000/api/artist/<artist>)