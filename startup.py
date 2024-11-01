from database import Projects

default_projects = [
    {
        "id": 1,
        "name": "Project Alpha",
        "start_date": "2023-01-15",
        "end_date": "2023-07-30",
        "team_members": [
            {"id": 101, "name": "Alice Smith", "role": "Developer"},
            {"id": 102, "name": "Bob Johnson", "role": "Tester"}
        ]
    },
    {
        "id": 2,
        "name": "Project Beta",
        "start_date": "2023-08-01",
        "end_date": "2023-12-31",
        "team_members": [
            {"id": 103, "name": "Charlie Lee", "role": "Designer"},
            {"id": 104, "name": "David Kim", "role": "Product Manager"}
        ]
    },
    {
        "id": 3,
        "name": "Project Delta",
        "start_date": "2024-01-01",
        "end_date": "2024-06-10",
        "team_members": [
            {"id": 103, "name": "John Depp", "role": "Developer"},
            {"id": 104, "name": "David Kim", "role": "Product Manager"}
        ]
    }
]

async def startup() -> None:
    """ Function checks the projects is already stored in firestore db or not
        If not stored then store the above sample projects when fastapi app boots
        and registered this event in main.py
        
        """

    for project in default_projects:
        project_instance = Projects.document(str(project["id"]))
        if not project_instance.get().exists:
            project_instance.set(project)
            print(f"Inserted project {project['name']}")
        else:
            print(f"Project {project['name']} already exists, skipping")
