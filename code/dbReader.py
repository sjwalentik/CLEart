import json
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

class Artworks:
    def __init__(self,list):
        self.listOfArt = list

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    

class Artwork:
    def __init__(self,conn,id):
        self.id = id
        cur = conn.cursor()
        cur.execute("SELECT * FROM artwork WHERE id = '" + str(id) + "'")
        rows = cur.fetchall()

        for row in rows:
            self.Accession_number = row[1]
            self.Title = row[2]
            self.Tombstone = row[3]
            
        cur = conn.cursor()
        cur.execute("SELECT * FROM artwork a INNER JOIN artwork__department ad ON a.id = ad.artwork_id WHERE a.id = '" + str(id) + "' ")
        rows = cur.fetchall()

        self.departments = []

        for row in rows:
            self.departments.append(Department(conn,row[5]))

        cur = conn.cursor()
        cur.execute("SELECT * FROM artwork a INNER JOIN artwork__creator ac ON a.id = ac.artwork_id WHERE a.id = '" + str(id) + "' ")
        rows = cur.fetchall()

        self.creators = []

        for row in rows:
            self.creators.append(Creator(conn,row[5]))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
            
class Department:
    def __init__(self,conn,departmentId):
        self.id = departmentId
        cur = conn.cursor()
        cur.execute("SELECT * FROM department WHERE id = '" + str(departmentId) + "'")
        rows = cur.fetchall()

        for row in rows:
            self.name = row[1]

class Creator:
    def __init__(self,conn,creatorId):
        self.id = creatorId
        cur = conn.cursor()
        cur.execute("SELECT * FROM creator WHERE id = '" + str(creatorId) + "'")
        rows = cur.fetchall()

        for row in rows:
            self.role = row[1]
            self.description = row[2]


def select_all_artwork(conn, dataFile):
    cur = conn.cursor()
    cur.execute("SELECT * FROM artwork")

    print(list(map(lambda x: x[0], cur.description)))

    rows = cur.fetchall()

    art = []

    for row in rows:
        art.append(Artwork(conn,row[0]))

    outFile = open(dataFile, 'w')
    outFile.write(Artworks(art).toJson())
    outFile.close()






def select_all_artworkDepartments(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM artwork__department")

    print(list(map(lambda x: x[0], cur.description)))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_all_artworkCreators(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM artwork__creator")

    print(list(map(lambda x: x[0], cur.description)))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_all_creators(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM creator")

    rows = cur.fetchall()

    print(list(map(lambda x: x[0], cur.description)))

    for row in rows:
        print(row)

def select_all_departments(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM department")

    rows = cur.fetchall()

    print(list(map(lambda x: x[0], cur.description)))

    for row in rows:
        print(row)

def select_tablenames(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")

    rows = cur.fetchall()

    print(list(map(lambda x: x[0], cur.description)))

    for row in rows:
        print(row)

def select_all_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM artwork a LEFT JOIN artwork__creator ac ON a.id = ac.artwork_id LEFT JOIN creator c ON ac.creator_id = c.id LEFT JOIN artwork__department ad ON a.id = ad.artwork_id LEFT JOIN department d ON ad.department_id = d.id")

    rows = cur.fetchall()

    print(list(map(lambda x: x[0], cur.description)))

    data = {}
    data = []

    for row in rows:
        print(row)
        data.append({
            'Id': row[0],
            'Accession_number': row[1],
            'Title': row[2],
            'Tombstone': row[3],
            'Creator_id': row[5],
            'Creator_role': row[7],
            'Creator_description': row[8],
            'Department_id': row[10],
            'Department_name': row[12]
        })

    with open(r'C:\Users\st_jo\source\repos\CLEart\CLEart\data.txt', 'w') as outfile:
        json.dump(data, outfile)
    


def main():
    database = r"C:\Users\st_jo\Desktop\code\cma-artworks.db"
    webSolutionDataFile = r"C:\Users\st_jo\source\repos\CLEart\CLEart\data.txt"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("Query all artwork")
        select_all_artwork(conn,webSolutionDataFile)


        """
        print("Query Table names:")
        select_tablenames(conn)
        """

"""
        print("Query all creators")
        select_all_creators(conn)
"""

"""
        print("Query all departments")
        select_all_departments(conn)
"""

"""
        print("Query all artwork departments")
        select_all_artworkDepartments(conn)
"""

"""
        print("Query all artwork creators")
        select_all_artworkCreators(conn)
"""

"""
        print("Query all artwork")
        select_all_artwork(conn)
"""

"""
        print("Update JSON file")
        select_all_data(conn)
"""

if __name__ == '__main__':
    main()