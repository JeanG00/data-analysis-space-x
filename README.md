# IBM Applied Data Science Capstone

## Project structure

```text
DATA_ANALYSIS_SPACE_X
|-- pyproject.toml
`-- assets
    |-- spacex_launch_dash.csv
    |-- spacex_dataset_part_2.csv
    |-- spacex_dataset_part_3.csv
`-- notebooks
    |-- apply_1_SpaceX_api.ipynb
    |-- apply_2_SpaceX_scraping.ipynb
    |-- apply_3_SpaceX_data_wrangling.ipynb
    |-- apply_3B_folium_launch_site_location.ipynb
    |-- apply_4_SQL.ipynb
    |-- apply_4B_SpaceX_MLP.ipynb
`-- src
    |-- dash
    |   `-- spacex.py
    |-- middlewares
    |-- models
    |   `-- __init__.py
    |-- services
    |   `-- dash.py
    |-- static
    |-- templates
    |   `-- base.html
    |   `-- index.html
    |   `-- dash.html
    |-- utils
    |   `-- util.py
    |   `-- version.py
    `-- routes.py
    `-- __init__.py
`-- test
`-- app.py
`-- conf.py
```

## Project setup

```sh
# list python envs
conda info --envs
conda create -n dash python=3.11
conda activate dash

pip install Flask
python3.11 -m pip install -r requirements.txt 

# freeze dependencies
conda list -e > requirements.txt
# alternative
pip freeze > requirements.txt
```

## script

```sh
# start app
flask run --host=0.0.0.0 --port=5000 --debug

#  secret key
python -c 'import secrets; print(secrets.token_hex())'
# 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf

# tells pip to find pyproject.toml in the current directory and install the project in `editable` or `development` mode
pip install -e .
# observe the project list
pip list

# find and run all the test functions you’ve written
pytest -v
# To measure the code coverage
coverage run -m pytest

# LINT: install dependency
pip install autopep8
# format file
autopep8 -i -a -a your-file-name.py

# @command init-db https://flask.palletsprojects.com/en/3.0.x/cli/
flask init-db 

# @command flush-redis
flask flush-redis
```

## [build & deploy](https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/)
