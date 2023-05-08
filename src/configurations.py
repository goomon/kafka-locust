import os


class DBConfigurations:
    postgres_username = "postgres" if os.getenv("POSTGRES_USER") is None else os.getenv("POSTGRES_USER")
    postgres_password = "postgres" if os.getenv("POSTGRES_PASSWORD") is None else os.getenv("POSTGRES_PASSWORD")
    postgres_port = 5432 if os.getenv("POSTGRES_PORT") is None else os.getenv("POSTGRES_PORT")
    postgres_db = "postgres" if os.getenv("POSTGRES_DB") is None else os.getenv("POSTGRES_DB")
    postgres_host = "localhost" if os.getenv("POSTGRES_HOST") is None else os.getenv("POSTGRES_HOST")
    sql_alchemy_url = (
        f"postgresql://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    )
