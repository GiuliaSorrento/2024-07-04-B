from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime` ) as year
                        from sighting s 
                        order by year(s.`datetime`) asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getStatesByYear(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.*
                    from sighting s , state st
                    where st.id = s.state 
                    and year(s.`datetime` ) = %s"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))
            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def getAllNodes(anno, id_stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                    from sighting s 
                    where year(s.`datetime` ) = %s
                    and s.state = %s"""
            cursor.execute(query, (anno, id_stato,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result



