# Scholar Sprint API

This repository contains the backend api for Scholar Sprint Web app.

## Install Python 3.9

Current Supported version for Scholar Sprint API is python v3.9.6

### MacOS
To Download and install v3.9 [click here](https://www.python.org/downloads/macos/).

## Install Required Packaged

This API uses about 23 third party packages which can be found in the `requirements.txt` file.

### MacOS

```bash 
$ python3 -m pip install -r requirements.txt
```

## Environment variables

Some Environment variables are required such as mongoDB information to connect to the database for development and testing purposes.

1. REACT_APP_MONGO_HOST
2. REACT_APP_DB
3. REACT_APP_COLLECTIONS
4. REACT_APP_DB_QUIZ
5. REACT_APP_QUIZ_COLLECTIONS

## Getting Started

This API is building using fast api.

```bash
$ python3 -m uvicorn main:app --reload
```