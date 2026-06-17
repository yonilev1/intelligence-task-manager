## INTELLIGENCE TASK MANAGER ##

this program helps to manage the tasks and agents that the unit has.

Agents:
we can add, edit, deactivate agents. can get all agents or one by id and get number of mission 
that were success or failure

Missions:
we can add, edit, change status, assigne to agent. can get all missions or one by id and more

file structur:

    intelligence-task-manager/
    ├── database/
    │   ├── db_connection.py
    │   ├── agent_db.py
    │   └── mission_db.py
    ├── README.md
    ├── requirements.txt
    └── .gitignore

Tables:

    agnets:
        id, INT, AUTO_INCREMENT, PK [unique id of agent]
        name, VARCHAR, NOT NULL, [name of agent]
        specialty,  VARCHAR, NOT NULL, [specialty of agent]
        is_active, BOOLEAN, default TRUE, [is agent active]
        completed_missions, INT, default 0, [amount of completed_missions]
        failed_missions, INT, default 0, [amount of failed_missions]
        agent_rank, ENUM(Junior / Senior / Commander ), [rank of agent]

    missions:
        id, INT, AUTO_INCREMENT, PK [unique id of mission]
        title, VARCHAR, NOT NULL, [title of mission]
        description, TEXT, NOT NULL, [description of mission]
        location,	VARCHAR, NOT NULL, [location of mission]
        difficulty,	INT, NOT NULL, [difficulty of mission]
        importance,	INT, NOT NULL [importance of mission]
        status,	VARCHAR, NOT NULL, [status of mission]
        risk_level,	VARCHAR, NOT NULL, [risk_level of mission, calculate = (2 * difficulty + importance)]
        assigned_agent_id,	INT, [assigned_agent_id to mission]


classes:

    AgentDB:
        meneges all access (create and edit rows, mulipilate and get date) to table agents
        if there is no mentiond reurn value - returns success/faliure message

        methods:
            create_agent(data)	                Creates a new agent and returns the agent object.
            get_all_agents()	                Returns a list of all agents
            get_agent_by_id(id)	                Returns one agent by ID, or None
            update_agent(id, data)	            UPDATE for the entire row (cannot change id)
            deactivate_agent(id)	            Sets agent inactive status
            increment_completed(id)	            Updates the number of tasks completed.
            increment_failed(id)	            Updates the number of failed tasks
            get_agent_performance(id)	        Returns a dictionary with these keys completed, failed, total, success_rate(completed / failed) of missions assigned to this agent
            count_active_agents()	            Returns the number of active agents


    MissionDB:
        meneges all access (create and edit rows, mulipilate and get date) to table missions:
        if there is no mentiond reurn value - returns success/faliure message

        methods:
            create_mission(data)	            Creates a new task and returns the entire object
            get_all_missions()	                Returns all tasks
            get_mission_by_id(id)	            Returns one task by ID, or None
            assign_mission(m_id, a_id)          Assign a mission to an agent
            update_mission_status(id, status)   is used for any status change
            get_open_missions_by_agent(id)	    Returns agent ASSIGNED/IN_PROGRESS tasks
            count_all_missions()	            Total tasks
            count_by_status(status)	            Counting by a certain status
            count_open_missions()	            Open task counter
            count_critical_missions()	        CRITICAL task counter
            get_top_agent()	                    The agent with the highest completed_missions

    connectionDB:
        manneges and create all connections to db and creation of db and tables
        if there is no mentiond reurn value - returns success/faliure message

        methods: 
            get_connection()	                Returns an active connection to MySQL
            create_database()	                Creates Intelligence_db if it does not exist.
            create_tables()	                    Creates both tables if they do not exist.


DATA ROOLS:

    1: rank must be Junior / Senior / Commander — any other value throws an error.
    2: difficulty and importance must be between 1 and 10 — otherwise an error.
    3: risk_level is calculated automatically when creating a task — the user does not submit it.
    4: An agent with is_active=False cannot accept tasks.
    5: An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
    6: If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
    7: Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
    8: Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
    9: Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
    10: Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.


DOCKER:

    to create container:
        docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

    to access throu CMD:
        1: docker exec -it intelligence-mysql mysql -uroot -p1234
        2: in mysql shell
            A: SHOW DATABASES; 
            B: USE Intelligence_db;
            C: DESCRIBE TABLES;


how to run DB layer:

    mission_db:
        in terminal, in path file intelligence-task-manager (C:\...\...\intelligence-task-manager):
            run: cd database
            then: python mission_db.py

    agent_db:
        in terminal, in file intelligence-task-manager (C:\...\...\intelligence-task-manager):
            run: cd database
            then: python agent_db.py

    connection_db:
        in terminal, in file intelligence-task-manager (C:\...\...\intelligence-task-manager):
            run: cd database
            then: python connection_db.py




