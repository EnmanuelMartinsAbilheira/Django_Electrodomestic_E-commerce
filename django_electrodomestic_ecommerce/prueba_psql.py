import psycopg2
import traceback

try:
    connection = psycopg2.connect(
        database="railway",
        user="postgres",
        password="OXEHOoEUCGUXrQekrqoDorYTkrPTYhQC",
        host="postgres.railway.internal",
        port="5432",
        client_encoding="utf8"
    )
    print("Conexión exitosa a PostgreSQL")
except Exception as e:
    print("Error al conectar a la base de datos:")
    traceback.print_exc()
