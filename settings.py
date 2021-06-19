import psycopg2


connection = psycopg2.connect(
    database="db_name",
    user="username",
    password="password",
    host="host",
    port=5432
)
