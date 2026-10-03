from fastapi import FastAPI
import allsolve

app = FastAPI(title="Solar Soldering Simulation API")
client = allsolve.Client(dotenv_file=".env")
PROJECT_ID = "cE2m4FtLUu3juQ5prU"

@app.get("/status")
def get_status():
    project = client.get_project(PROJECT_ID)
    return {
        "project_name": project.name,
        "project_id": project.id,
        "url": client.get_url(project)
    }

@app.post("/run")
def trigger_run(laser_power: float, duration: float):
    project = client.get_project(PROJECT_ID)
    # Perform parameter update & job execution
    return {"status": "Job submitted", "laser_power": laser_power}