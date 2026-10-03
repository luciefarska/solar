import allsolve

def run_app_simulation():
    # Load credentials and initialize the client
    client = allsolve.Client(dotenv_file=".env")
    
    # Load your existing project
    project_id = "cE2m4FtLUu3juQ5prU"
    project = client.get_project(project_id)
    
    print(f"App successfully linked to project '{project.name}' (ID: {project.id})")
    print(f"Open in browser: {client.get_url(project)}")

if __name__ == "__main__":
    run_app_simulation()