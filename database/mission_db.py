from . import connection_db as cdb
import mysql.connector

connection = cdb.Db_Connection()
class DB_Mission:
    def create_mission(self, data: dict):
        conn, cursor = self.get_connection_with_db()
        risk_level = self.calculate_risk_level(data['difficulty'], data['importance'])
        try:
            cursor.execute("""
                INSERT INTO missions (title, description, location, difficulty, importance, status, risk_level)
                            VALUES(%s, %s, %s, %s, %s, %s, %s);
                """, (data['title'], data['description'], data['location'],
                    data['difficulty'], data['importance'], 'NEW', risk_level))
        except mysql.connector.errors.DatabaseError as e: 
            raise ValueError
        row_id = cursor.lastrowid
        new_object = {'id':row_id, 'title':data['title'], 'description':data['description'], 
                        'location':data['location'], 'difficulty':data['difficulty'],
                            'importance': data['importance'], 'status':'NEW', 'risk_level':risk_level}
        conn.commit()
        cursor.close()
        conn.close()
        return new_object
    

    def get_all_missions(self):
        conn, cursor = self.get_connection_with_db()
        cursor.execute("""SELECT * FROM missions;""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row
    

    def get_mission_by_id(self, mission_id):
        conn, cursor = self.get_connection_with_db()
        cursor.execute("""SELECT * FROM missions WHERE id = %s;""", (mission_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


    def update_mission(self, mission_id, data):
        #To Do IN tests - if not data, if id does not exist
        parts = [f'{key} = %s' for key in data.keys()]
        parts_in_str = (', '.join(parts))
        parsed_data = list(data.values()) + [mission_id]

        #cursor = conn.cursor(dictionary=True)
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""
        UPDATE missions SET {parts_in_str} WHERE id = %s
        """, parsed_data)
        did_update = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return did_update
    
    

    def assign_mission(self, m_id, a_id):
        #checks!!!
        assign = self.update_mission(m_id, {'assigned_agent_id':a_id})
        update_status = self.update_mission_status(m_id, 'ASSIGNED')
        return 'mission assigned successfully.' if assign and self.update_mission_status else 'could not assign mission to agent'
    
    def update_mission_status(self, id, status):
        #checks!!!
        return 'status updated successfully.' if self.update_mission(id, {'status':status}) else 'could not assign mission to agent'
    

    def get_open_missions_by_agent(self, id):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT * FROM missions WHERE STATUS LIKE '%SS%';""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row

    def calculate_risk_level(self, difficulty, importance):
        risk = 2 * difficulty + importance
        if risk < 9: return 'LOW'
        elif 9 < risk < 17: return 'MEDIUM'
        elif 17 < risk < 25: return 'HIGH'
        return 'CRITICAL'


    def count_all_missions(self):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT COUNT(*) as count FROM missions;""")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['count']


    def count_by_status(self, status):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT COUNT(*) as count FROM missions
                       GROUP BY status
                       HAVING status = %s;""", (status,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row is not None:
            return row['count']
        return row


    def get_connection_with_db(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    
    #NEW', 'ASSIGNED', 'IN_PROGRESS'

    def count_open_missions(self):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT COUNT(*) as count FROM missions
                       WHERE status = 'NEW' OR status = 'ASSIGNED' OR status = 'IN_PROGRESS';""")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['count']
    

    def count_critical_missions(self):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT COUNT(*) as count FROM missions
                       WHERE risk_level = 'CRITICAL';""")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['count']
    

    def get_top_agent(self):
        conn, cursor = self.get_connection_with_db()
        cursor.execute(f"""SELECT assigned_agent_id FROM missions
                       WHERE status = 'COMPLETED'
                       GROUP BY assigned_agent_id
                       ORDER BY COUNT(*) DESC
                       LIMIT 1;""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row['assigned_agent_id']


#title, description, location, difficulty, importance, status, risk_level) 
if __name__ == "__main__":

    ms = DB_Mission()
    #mission = ms.create_mission({'title':'Yoni','description': 'LEV', 
                                #'location': 'Jerusalem', 'difficulty': 5, 'importance': 5})
    #print(mission)
    #print(ms.get_open_missions_by_agent(5))
    ms.update_mission_status(4, 'COMPLETED')
    print(ms.get_top_agent())
    #print(ms.update_mission_status(4,'COMPLETED'))