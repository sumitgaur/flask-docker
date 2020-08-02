import psycopg2
import sys
import boto3

ENDPOINT = "airflow.clukjtkpcpwu.us-west-2.rds.amazonaws.com"
PORT = "5432"
USR = "postgres"
REGION = "us-west-2"
DBNAME = "airflow"
DB_PASSWORD = 'airflow_pass'
# gets the credentials from .aws/credentials
# session = boto3.Session(profile_name='RDSCreds')
client = boto3.client('rds')

# token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)
command = """CREATE TABLE document_status (doc_id SERIAL PRIMARY KEY,doc_name VARCHAR(255) NOT NULL,
dag_name VARCHAR(255) NOT NULL,status VARCHAR(255) NOT NULL,created_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,updated_date TIMESTAMP NOT NULL DEFAULT CURRENT_DATE)"""
try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=DB_PASSWORD)
    cur = conn.cursor()
    # cur.execute("""SELECT now()""")
    cur.execute(command)
    cur.close()
    conn.commit()
except Exception as e:
    print("Database connection failed due to {}".format(e))


# def create_tables():
#     """ create tables in the PostgreSQL database"""
#     commands = (
#         """
#         CREATE TABLE vendors (
#             vendor_id SERIAL PRIMARY KEY,
#             vendor_name VARCHAR(255) NOT NULL
#         )"""
#     )
