import os
import psycopg2
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

SUPABASE_POSTGRES_URL = os.getenv("SUPABASE_POSTGRES_URL")

if not SUPABASE_POSTGRES_URL:
    raise Exception("ERROR: La variable SUPABASE_POSTGRES_URL no está definida")


class ProfessionalRepository:

    def search_by_vector(self, vector: list[float], limit: int):
        """
        Busca trabajadores por similitud vectorial usando la columna `embedding`
        (vector(384)).
        """
        SQL = """
            SELECT
                id_estable,
                json_data,
                embedding <-> (%s::vector) AS distancia
            FROM trabajadores
            ORDER BY distancia ASC
            LIMIT %s;
        """

        try:
            conn = psycopg2.connect(SUPABASE_POSTGRES_URL)
            cur = conn.cursor()

            cur.execute(SQL, (vector, limit))

            columns = [c[0] for c in cur.description] # type: ignore
            results = [dict(zip(columns, row)) for row in cur.fetchall()]

            cur.close()
            conn.close()

            return results

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error buscando trabajadores: {e}"
            )
