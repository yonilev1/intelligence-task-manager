import connection_db as cdb
import mysql.connector

connection = cdb.Db_Connection()
class DB_connection:
    def create_agent(self, data: dict):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            INSERT INTO agents (name, specialty, agent_rank) VALUES(%s, %s, %s);
            """, (data['name'], data['specialty'], data['agent_rank']))
            row_id = cursor.lastrowid
            new_object = {'id':row_id, 'name':data['name'], 'specialty':data['specialty'], 
                        'is_active':True, 'completed_missions':0,
                            'failed_missions':0, 'agent_rank':data['agent_rank']}
        except mysql.connector.errors.DatabaseError as e: 
            raise ValueError(f'agent rank should by one of 3 types, not {data['agent_rank']}')
        conn.commit()
        cursor.close()
        conn.close()
        return new_object
    

    def get_all_agents(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM agents;""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row
    
    def get_agent_by_id(self, agent_id):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT * FROM agents WHERE id = %s;""", (agent_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

obj = DB_connection()
#obj_con = obj.create_agent({'name':"YONI", 'specialty':'CODER', 'agent_rank':'Senior'})
print((obj.get_agent_by_id(54)))