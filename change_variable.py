import os
import requests
import json

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class ChangeVariable:
    def __init__(
        self,
        gitlab_url,
        access_token,
        target_variable,
        target_value,
        target_group=False,
        target_group_name=False,
    ):
        self.target_group = target_group
        self.gitlab_url = gitlab_url
        self.access_token = access_token
        self.target_variable = target_variable
        self.target_value = target_value
        self.target_group_name = target_group_name

        # print(target_group, gitlab_url, access_token, target_variable, target_value)

    def find_target_groups(self):
        if self.target_group is False or not self.target_group:
            if self.target_group_name:
                res = requests.get(
                    url=f"{self.gitlab_url}/api/v4/groups/{self.target_group_name}/",
                    headers={
                        "PRIVATE-TOKEN": self.access_token,
                        "Content-Type": "application/json",
                    },
                )
                if res.status_code == 200:
                    self.target_group = res.json()["id"]
                else:
                    raise Exception("Error with group_name")

            else:
                raise Exception("No target_group_name or target_group_id!")

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
            print("project ", project)

            res = requests.get(
                url=f"{self.gitlab_url}/api/v4/projects/{project}/variables/",
                headers={
                    "PRIVATE-TOKEN": self.access_token,
                },
            )

            res2 = requests.get(
                url=f"{self.gitlab_url}/api/v4/projects/{project}",
                headers={"PRIVATE-TOKEN": self.access_token},
            )

            data: dict = res2.json()
            for _ in data:
                if _ == "name":
                    self.repo_name = data[_]
                    break

            for variable in res.json():
                if variable["key"] == self.target_variable:
                    new_var = f"{self.target_value}/{self.repo_name}"

                    if not variable["value"] == new_var:
                        res = requests.put(
                            url=f"{self.gitlab_url}/api/v4/projects/{project}/variables/{self.target_variable}/",
                            headers={"PRIVATE-TOKEN": self.access_token},
                            data={"value": new_var},
                        )
                        print(
                            f'{res.status_code}, "{variable["value"]}" changed to "{new_var}" in project {project}"'
                        )
                    else:
                        print(
                            f'Variable already equals target_variable "{new_var} in project {project}"'
                        )
                    break

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
    gitlab_url=os.environ.get("GITLAB_URL"),
    access_token=os.environ.get("ACCESS_TOKEN"),
    target_variable=os.environ.get("TARGET_VARIABLE"),
    target_value=os.environ.get("TARGET_VALUE"),
    target_group=os.environ.get("TARGET_GROUP"),
    target_group_name=os.environ.get("TARGET_GROUP_NAME"),
)

worker.start()
