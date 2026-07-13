from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllRatings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT DISTINCT r.avg_rating 
            from ratings r 
            order by r.avg_rating 
                """
            cursor.execute(query)

            for row in cursor:
                result.append(row['avg_rating'])

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllNodi(r1, r2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT DISTINCT n.*
            from role_mapping rm  
            join ratings r on rm.movie_id  = r.movie_id 
            join names n on rm.name_id = n.id 
            where r.avg_rating between %s and %s and n.date_of_birth is not NULL
                    """
            cursor.execute(query,(r1, r2))

            for row in cursor:
                attore = Attore(**row)
                result.append(attore)

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllMovies(r1, r2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT distinct rm.name_id, rm.movie_id 
            from role_mapping rm 
            join movie m on rm.movie_id = m.id 
            join ratings r on rm.movie_id = r.movie_id 
            where m.worlwide_gross_income is not null and m.worlwide_gross_income LIKE ('$%') and r.avg_rating between %s and %s
                """
            cursor.execute(query, (r1, r2))

            for row in cursor:
                result.append((row['name_id'], row['movie_id']))

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllIncassi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT m.id, m.worlwide_gross_income as incasso
            from movie m 
            where m.worlwide_gross_income is not null and m.worlwide_gross_income LIKE ('$%')
                    """
            cursor.execute(query)

            for row in cursor:
                result.append((row['id'], row['incasso']))

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

