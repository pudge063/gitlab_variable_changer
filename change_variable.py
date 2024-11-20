import os
import requests

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class ChangeVariable:
    def __init__(
        self, target_group, gitlab_url, access_token, target_variable, target_value
    ):
        self.target_group = target_group
        self.gitlab_url = gitlab_url
        self.access_token = access_token
        self.target_variable = target_variable
        self.target_value = target_value

        # print(target_group, gitlab_url, access_token, target_variable, target_value)

    def find_target_groups(self):
        res = requests.get(
            url=f"{self.gitlab_url}/api/v4/groups/{self.target_group}/projects/",
            headers={
                "PRIVATE-TOKEN": self.access_token,
                "Content-Type": "application/json",
            },
        )

        self.projects = [_["id"] for _ in res.json()]

        print(f"Projects in group: {self.projects}.")

    def change_if_need(self):
        for project in self.projects:
            res = requests.get(
                url=f"{self.gitlab_url}/api/v4/projects/{project}/variables/",
                headers={
                    "PRIVATE-TOKEN": self.access_token,
                },
            )
            print(f"Check in project {project}, status: {res.status_code}")

            for variable in res.json():
                if variable["key"] == self.target_variable:
                    if not variable["value"] == self.target_value:
                        res = requests.put(
                            url=f"{self.gitlab_url}/api/v4/projects/{project}/variables/{self.target_variable}/",
                            headers={"PRIVATE-TOKEN": self.access_token},
                            data={"value": self.target_value},
                        )
                        print(
                            f'{res.status_code}, "{variable["value"]}" changed to "{self.target_value} in project {project}"'
                        )
                    else:
                        print(
                            f'Variable already equals target_variable "{self.target_value} in project {project}"'
                        )
                    return None

        # print("No changes.")

    def start(self):
        self.find_target_groups()
        self.change_if_need()


# worker = ChangeVariable(
#     target_group=4,
#     gitlab_url="https://gitlab.example.com",
#     access_token="key",
#     target_variable="external_repo",
#     target_value="new_value",
# )

worker = ChangeVariable(
    target_group=os.environ.get("TARGET_GROUP"),
    gitlab_url=os.environ.get("GITLAB_URL"),
    access_token=os.environ.get("ACCESS_TOKEN"),
    target_variable=os.environ.get("TARGET_VARIABLE"),
    target_value=os.environ.get("TARGET_VALUE"),
)

worker.start()
