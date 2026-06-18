from . import connection_db as cdb
import mysql.connector

connection = cdb.Db_Connection()
class DB_Agent:
    def create_agent(self, data: dict):
        conn, cursor = self.get_connrection_with_db()
        try:
            cursor.execute("""
            INSERT INTO agents (name, speciality, agent_rank) VALUES(%s, %s, %s);
            """, (data['name'], data['speciality'], data['agent_rank']))
            row_id = cursor.lastrowid
            new_object = {'id':row_id, 'name':data['name'], 'speciality':data['speciality'], 
                        'is_active':True, 'completed_missions':0,
                            'failed_missions':0, 'agent_rank':data['agent_rank']}
        except mysql.connector.errors.DatabaseError as e: 
            raise ValueError(f'agent rank should by one of 3 types, not {data['agent_rank']}')
        conn.commit()
        cursor.close()
        conn.close()
        return new_object
    

    def get_all_agents(self):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute("""SELECT * FROM agents;""")
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        return row
    

    def get_agent_by_id(self, agent_id):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute("""SELECT * FROM agents WHERE id = %s;""", (agent_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row


    def update_agent(self, agent_id, data):
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
        return 'Agent updated successfuly.'
    

    def deactivate_agent(self, agent_id):
        return self.update_agent(agent_id, {'is_active':False})

    def increment_completed(self, agent_id):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute(f"""SELECT completed_missions AS cm FROM agents WHERE id = %s;""",(agent_id,))
        complete_number = cursor.fetchone()
        try:
            return self.update_agent(agent_id, {'completed_missions': complete_number['cm'] + 1})
        except TypeError as e:
            raise
    

    def increment_failed(self, agent_id):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute(f"""SELECT failed_missions AS fm FROM agents WHERE id = %s;""",(agent_id,))
        failed_number = cursor.fetchone()
        try:
            return self.update_agent(agent_id, {'failed_missions': failed_number['fm'] + 1})
        except TypeError as e:
            raise

    
    def get_agent_performance(self, agent_id):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute(f"""SELECT completed_missions, failed_missions FROM agents WHERE id = %s;""",(agent_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        success_rate = 0 if (row['completed_missions'] + row['failed_missions']) == 0 else row['completed_missions']/(row['completed_missions'] + row['failed_missions'])
        return {'Total': row['completed_missions'] + row['failed_missions'],
                 'Completed': row['completed_missions'],
                 'Failed': row['failed_missions'],
                 'Success_rate': f'{success_rate * 100} %'}
    

    def count_active_agents(self):
        conn, cursor = self.get_connrection_with_db()
        cursor.execute(f"""SELECT COUNT(*) AS count FROM agents
                       WHERE is_active = True
                       GROUP BY is_active;""")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row['count']


    def get_connrection_with_db(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        return conn, cursor



if __name__ == "__main__":
    obj = DB_Agent()
    obj_con = obj.create_agent({'name':"YONI", 'specialty':'CODER', 'agent_rank':'Senior'})
    print((obj.get_all_agents()))
    print(obj.get_agent_by_id(3))
    print(obj.deactivate_agent(1))
    print(obj.get_agent_performance(3))
    print(obj.count_active_agents())