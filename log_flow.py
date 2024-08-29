from prefect import flow, task

@task
def log_task(name):
    print(f"Hello, {name}!")

@flow
def log_flow(name: str = "World"):
    log_task(name)

if __name__ == "__main__":
    log_flow()

