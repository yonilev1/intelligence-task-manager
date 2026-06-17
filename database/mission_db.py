import connection_db as cdb
import mysql.connector

connection = cdb.Db_Connection()
class DB_Mission:
    def create_mission(self, data: dict):
        conn, cursor = self.get_connrection_with_db()
        risk_level = self.calculate_risk_level(data['difficulty'], data['importance'])
        cursor.execute("""
            INSERT INTO missions (title, description, location, difficulty, importance, status, risk_level)
                           VALUES(%s, %s, %s, %s, %s, %s, %s);
            """, (data['title'], data['description'], data['location'],
                   data['difficulty'], data['importance'], 'NEW', risk_level))
            
        row_id = cursor.lastrowid
        new_object = {'id':row_id, 'title':data['title'], 'description':data['description'], 
                        'location':data['location'], 'difficulty':data['difficulty'],
                            'importance': data['importance'], 'status':'NEW', 'risk_level':risk_level}
        conn.commit()
        cursor.close()
        conn.close()
        return new_object
    

    def get_all_agents(self):
        '''conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)'''
        conn, cursor = self.get_connrection_with_db()
        cursor.execute("""SELECT * FROM agents;""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row
    

    def get_agent_by_id(self, agent_id):
        '''conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)'''
        conn, cursor = self.get_connrection_with_db()
        cursor.execute("""SELECT * FROM agents WHERE id = %s;""", (agent_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


    def update_agent(self, agent_id, data):
        '''conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()'''
        #To Do IN tests - if not data, if id does not exist
        parts = [f'{key} = %s' for key in data.keys()]
        parts_in_str = (', '.join(parts))
        parsed_data = list(data.values()) + [agent_id]

        #cursor = conn.cursor(dictionary=True)
        conn, cursor = self.get_connrection_with_db()
        cursor.execute(f"""
        UPDATE agents SET {parts_in_str} WHERE id = %s
        """, parsed_data)
        did_update = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return 'Agent updated successfuly.' if did_update else 'could not update agent.'
    




    def calculate_risk_level(self, difficulty, importance):
        risk = 2 * difficulty + importance
        if risk < 9: return 'LOW'
        elif 9 < risk < 17: return 'MEDIUM'
        elif 17 < risk < 25: return 'HIGH'
        return 'CRITICAL'


    def get_connrection_with_db(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        return conn, cursor
#title, description, location, difficulty, importance, status, risk_level) 
ms = DB_Mission()
mission = ms.create_mission({'title':'Yoni','description': 'LEV', 
                             'location': 'Jerusalem', 'difficulty': 5, 'importance': 5})
print(mission)