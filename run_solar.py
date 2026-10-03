import allsolve

# Initialize client using credentials from .env
client = allsolve.Client(dotenv_file=".env")

# Create project
project = client.create_project(
    name="Solar Soldering Simulation",
    description="Created via Client SDK",
)

print(f"Project created: {client.get_url(project)}")

# Define geometry, materials, and physics using SDK objects
# (or load an existing cad/mesh into the project)
# ...

# Fetch or trigger a simulation run
# project.run() or sim = project.create_simulation(...)