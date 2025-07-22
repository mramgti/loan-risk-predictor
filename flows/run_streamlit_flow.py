from prefect import flow, task
import subprocess
import os

@task
def run_streamlit_app():
    script_path = os.path.join(os.path.dirname(__file__), "..", "streamlit_app", "main.py")
    command = ["streamlit", "run", script_path]
    subprocess.run(command)

@flow(name="Streamlit Loan App Orchestration")
def streamlit_app_flow():
    run_streamlit_app()

if __name__ == "__main__":
    streamlit_app_flow()
