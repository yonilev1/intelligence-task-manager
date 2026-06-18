from fastapi import FastAPI, status, HTTPException
from routes import agent_routes, mission_routes, report_routes
import uvicorn
from database import connection_db

app = FastAPI()
app.include_router(agent_routes.route)
app.include_router(mission_routes.route)
app.include_router(report_routes.route)

conn = connection_db.Db_Connection()
conn.create_database()
conn.create_tables()

if __name__=="__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)