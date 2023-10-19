from omnivector.abstraction import AbstractDB

class PGVectorDB(AbstractDB):
    def __init__(self):
        from pgvector.psycopg import register_vector
        import psycopg

        super().__init__()

        self.conn = psycopg.connect(f'dbname={self.config["pgvector"]["DB_NAME"]} '
                                    f'user={self.config["pgvector"]["USER"]} '
                                    f'password={self.config["pgvector"]["PASSWORD"]}', autocommit=True)

        self.conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
        register_vector(self.conn)

    def create_index(self, ids, texts, vectors):
        self.conn.execute('DROP TABLE IF EXISTS documents')
        self.conn.execute('CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))')


        for id, content, embedding in zip(ids, texts, vectors):
            self.conn.execute('INSERT INTO documents (id, content, embedding) VALUES (%s, %s, %s)', (id, content, embedding))


    def vector_search(self, vector, k=3):
        neighbors = self.conn.execute('SELECT id, content FROM documents ORDER BY embedding <=> %s LIMIT 5', (vector,))

        return [n for n in  neighbors]
