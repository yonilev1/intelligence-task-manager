from database import agent_db, mission_db, connection_db

connection = connection_db.Db_Connection()


class ValidateData:
    def check_update(self, db, id, data):
        conn,cursor = self.get_connection_with_db()
        cursor.execute(f"select * from {db} WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f'id {id} was not found in {db}')
        
        try:
            if db == 'agents':
                obj = agent_db.DB_Agent()
                object = obj.update_agent(id, data)
            else:
                obj = mission_db.DB_Mission()
                object = obj.update_mission(id, data)
        except ValueError as e:
            raise
        return object


    def check_assign_mission(self, m_id, a_id):
        conn,cursor = self.get_connection_with_db()
        if self.check_id_exsits(m_id, 'missions') is None:
            raise ValueError(f'id {m_id} was not found in missions')
        if self.check_id_exsits(a_id, 'agents') is None:
            raise ValueError(f'id {a_id} was not found in agents')
        
        ms = mission_db.DB_Mission()
        ag = agent_db.DB_Agent()
        agent = ag.get_agent_by_id(a_id)
        mission = ms.get_mission_by_id(m_id)
        if agent['is_active'] == False:
            raise ValueError(f'Non active agent cant be assigned with missions')
        
        if not self.get_active_member_opend_missions(a_id):
            raise ValueError(f'Nagent cant be assigned with missions, already has 3 or more missions')
        
        if mission['risk_level'] =='CRITICAL' and agent['agent_rank'] != 'Commander':
            raise ValueError(f'only commander can get mission critical')
        
        if mission['status'] !='NEW':
            raise ValueError(f'only new mission can be assigned')

        return ms.assign_mission(m_id, a_id)        

        

    def check_id_exsits(self, id, db):
        conn,cursor = self.get_connection_with_db()
        cursor.execute(f"select * from {db} WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            return False
        return True
    

    def get_active_member_opend_missions(self, id):
        conn,cursor = self.get_connection_with_db()
        cursor.execute(f"select COUNT(*) as count from missions WHERE id = %s AND status LIKE %SS%", (id,))
        row = cursor.fetchone()
        if row['count'] <= 3:
            return True
        return False

    def get_connection_with_db(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("USE Intelligence_db")
        cursor.close()

        cursor = conn.cursor(dictionary=True)
        return conn, cursor
    
val = ValidateData()
print(val.check_assign_mission(3, 2))