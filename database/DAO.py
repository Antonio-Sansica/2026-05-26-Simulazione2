from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_ratings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:

            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT DISTINCT r.avg_rating AS rating
            FROM ratings r 
            ORDER BY r.avg_rating ASC   
            """
            cursor.execute(query)

            for row in cursor:
                result.append(row['rating'])

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_id_nodi_validi(rate1, rate2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
                    SELECT DISTINCT n.*
                    FROM names n 
                    JOIN role_mapping rm ON n.id = rm.name_id 
                    JOIN ratings r ON rm.movie_id = r.movie_id
                    WHERE r.avg_rating BETWEEN %s AND %s 
                      AND n.date_of_birth IS NOT NULL
                      AND (rm.category = 'actor' OR rm.category = 'actress')
                    """
            cursor.execute(query, (rate1, rate2))

            for row in cursor:
                result.append(Attore(**row))

            print(f"Nodi estratti dal DB: {len(result)}")
            return result

        except Exception as e:
            print(f"Errore DAO ID Nodi Grafo: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def get_archi_grafo_pesato():
        print("Inizio estrazione archi dal DB...")
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return []
        try:
            cursor = cnx.cursor(dictionary=True)

            # Query ottimizzata: unisce la tabella role_mapping con se stessa (su stesso film)
            # e filtra direttamente per attori, senza parametri extra!
            query = """
                    SELECT rm1.name_id AS id_1, rm2.name_id AS id_2, m.id AS idFilm, m.worlwide_gross_income AS pesoParziale
                    FROM role_mapping rm1
                    JOIN role_mapping rm2 ON rm1.movie_id = rm2.movie_id
                    JOIN movie m ON rm1.movie_id = m.id
                    WHERE rm1.name_id < rm2.name_id
                      AND (rm1.category = 'actor' OR rm1.category = 'actress')
                      AND (rm2.category = 'actor' OR rm2.category = 'actress')
                    """

            cursor.execute(query)

            for row in cursor:
                result.append((row['id_1'], row['id_2'], row['idFilm'], row['pesoParziale']))

            print(f"Archi estratti dal DB: {len(result)}")
            return result

        except Exception as e:
            print(f"Errore DAO estrazione archi: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()