### Variable changer

- **Create .env file** 
```
ACCESS_TOKEN=youraccesstoken
TARGET_GROUP=4
GITLAB_URL=https://gitlab.example.com
TARGET_VARIABLE=variable_name
TARGET_VALUE=variable_target_value
```

- **Install project && python environment**
```
git clone https://github.com/pudge063/gitlab_variable_changer
cd giltab_variable_changer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- **Start script**
```
python change_variable.py
```