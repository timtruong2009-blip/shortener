import sqlalchemy as sa
import os
import secrets
import string
from dotenv import load_dotenv
load_dotenv()

class Shorten:
    def __init__(self):

        self.alphabet = string.ascii_letters + string.digits
        postgres_link = os.environ["DATABASE_URL"]

        self.engine = sa.create_engine(postgres_link)
        self.connection = self.engine.connect()

        self.metadata = sa.MetaData()

        self.info_table = sa.Table(
            "info_tab",
            self.metadata,
            sa.Column("id", sa.Integer, primary_key= True),
            sa.Column("old_link", sa.CHAR(1000), unique = True),
            sa.Column("short_link", sa.CHAR(1000), unique= True, index=True)
        )
        self.metadata.create_all(self.engine)


    def insert_old_and_short_link(self, old_link: str, short_link:str):
        query = self.info_table.insert().values(old_link = old_link, short_link = short_link)
        self.connection.execute(query)
        self.connection.commit()

    def send_back_new_short_link(self, new_link: str):
        new_short_link = "".join(secrets.choice(self.alphabet) for _ in range(6))
        self.insert_old_and_short_link(old_link= new_link, short_link= new_short_link)
        return new_short_link

    def check_url_in_db(self, link: str):
        query = sa.select(self.info_table.c.short_link).where(self.info_table.c.old_link == link)
        return self.connection.execute(query).scalar()

    def send_link(self, link: str):
        query = sa.select(self.info_table.c.old_link).where(self.info_table.c.short_link == link.removeprefix("http://127.0.0.1:8000/"))
        result = self.connection.execute(query).scalar()
        return result.strip() if result else None