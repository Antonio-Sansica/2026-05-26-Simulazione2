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
            SELECT distinct r.avg_rating 
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
    def getAllNodi(rate1, rate2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
                SELECT distinct n.*
                from names n 
                join role_mapping rm on n.id = rm.name_id 
                join ratings r on rm.movie_id = r.movie_id 
                where r.avg_rating between %s and %s and n.date_of_birth is not null
                    """
            cursor.execute(query,(rate1, rate2))

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
    def getAllMovies(rate1, rate2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
                    SELECT distinct rm.movie_id, rm.name_id 
                    from role_mapping rm 
                    join ratings r on rm.movie_id = r.movie_id 
                    join movie m on rm.movie_id = m.id 
                    where r.avg_rating between %s and %s and m.worlwide_gross_income is not null and m.worlwide_gross_income like('$%')
                        """
            cursor.execute(query, (rate1, rate2))

            for row in cursor:
                result.append((row['movie_id'], row['name_id']))

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()

    @staticmethod
    def getAllIncassi(rate1, rate2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None: return result
        try:
            cursor = cnx.cursor(dictionary=True)

            query = """
            SELECT distinct m.id, m.worlwide_gross_income 
            from movie m 
            JOIN ratings r ON m.id = r.movie_id 
            where m.worlwide_gross_income LIKE ('$%') AND m.worlwide_gross_income IS NOT NULL and r.avg_rating between %s and %s
                            """
            cursor.execute(query, (rate1, rate2))

            for row in cursor:
                result.append((row['id'], row['worlwide_gross_income']))

            return result
        except Exception as e:
            print(f"Errore DAO estrazione base: {e}")
            return []
        finally:
            cursor.close()
            cnx.close()



