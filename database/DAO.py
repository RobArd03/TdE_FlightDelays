from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * 
                    from airports a 
                    order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(nMin: int, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.ID, COUNT(*) as N
                    FROM (	SELECT a.ID, a.IATA_CODE, f.AIRLINE_ID, COUNT(*) 
                            FROM airports a, flights f 
                            WHERE a.ID = f.ORIGIN_AIRPORT_ID 
                            OR a.ID = f.DESTINATION_AIRPORT_ID 
                            GROUP BY a.ID, a.IATA_CODE, f.AIRLINE_ID ) t
                    GROUP BY t.ID
                    HAVING N >= %s
                    """

        cursor.execute(query,(nMin,))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])

        cursor.close()
        conn.close()
        return result