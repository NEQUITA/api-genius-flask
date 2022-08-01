import boto3
import os

from dotenv import load_dotenv

load_dotenv()

AWS_Access_Key_Id = os.environ.get("AWS_Access_Key_Id")
AWS_Secret_Key = os.environ.get("AWS_Secret_Key")

class DynamoDb:
    #Inicializa o banco de dados
    def __init__(self):
        try:

            self.client = boto3.client(
                'dynamodb',
                aws_access_key_id=AWS_Access_Key_Id,
                aws_secret_access_key=AWS_Secret_Key,
                region_name="us-east-1"
            )
            self.resource = boto3.resource(
                'dynamodb',
                aws_access_key_id=AWS_Access_Key_Id,
                aws_secret_access_key=AWS_Secret_Key,
                region_name="us-east-1"
            )
            #Insere a tabela no banco
            self.table_name = 'artists_hits'
            self.table = self.resource.Table(self.table_name)
            self._create_artist_table()

        #Caso ocorra algum erro
        except Exception as e:
            raise ValueError(e)
    
    #Cria a tabela
    def _create_artist_table(self):
        try:
            #Verifica se a tabela já existe, caso não exista, cria a mesma
            table_exists = self.client.list_tables()['TableNames']
            if self.table_name not in table_exists:
                self.client.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'artist_name',
                            'KeyType': 'HASH',
                        }
                            ],
                        AttributeDefinitions=[
                        {
                            'AttributeName': 'artist_name',
                            'AttributeType': 'S',
                        }
            
                            ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 1,
                            'WriteCapacityUnits': 1
                        }
                )

        #Caso ocorra algum erro
        except Exception as e:
            raise ValueError(e)
    
    #Insere dados na tabela
    def _insert_artist(self, artist_name, id_transaction, hits):
        try:
            #Cria item com as informações (ID da transação, nome do artista e top 10 hits)
            response = self.table.put_item(
                Item={
                    'id_transaction': id_transaction,
                    'artist_name': artist_name,
                    'hits': hits
                })
            return response

        #Caso ocorra algum erro
        except Exception as e:
            raise ValueError(e)