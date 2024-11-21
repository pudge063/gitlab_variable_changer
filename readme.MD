### Variable changer

-**Change gitlab url**
```
TARGET_VARIABLE=http://gitlab.com
TARGET_VALUE=external_repo

external_repo :== http://gitlab.com/repo_name
```

- **Install project && python environment**
```
git clone https://github.com/pudge063/gitlab_variable_changer
cd giltab_variable_changer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- **Create .env file** 
```
ACCESS_TOKEN=youraccesstoken
GITLAB_URL=https://gitlab.example.com
TARGET_VARIABLE=http://gitlab.com
TARGET_VALUE=variable_target_value
TARGET_GROUP=4
TARGET_GROUP_NAME=
```

- **Select target group by name or id**
```
TARGET_GROUP=4

TARGET_GROUP_NAME=group_for_change
```

- **Start script**
```
python change_variable.py
```