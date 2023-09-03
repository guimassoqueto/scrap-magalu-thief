1. create .env file
```shell
make env
```
2. init the virtual environment
```shell
poetry shell
```

3. install dependencies
```shell
poetry install
```

4. pre-commit hooks (to avoid bad commit messages, and do tests before commit)
```shell
pre-commit install && pre-commit install --hook-type commit-msg
```

5. init the app
```shell
make a
```