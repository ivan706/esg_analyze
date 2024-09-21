## Introduction

#### Requirements
Before running the project, make sure you have Python 3 and Pip 3 installed on your develop machine.

* Python 3
* Pip 3

#### Download repository
    
```bash
git clone 本项目
cd esg_analysis
```

#### Installation virtualenv

To install virtualenv via pip run if you don't have it installed yet:
```bash
$ pip3 install virtualenv
```

#### Usage

Creation of virtualenv:
```bash
$ virtualenv -p python3 venv
```

Activate the virtualenv:
```bash
$ source venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Get data

In virtualenv, run the following command to get data through AJAX request and save it to a CSV file:

```bash
python scripts/sse.py
``` 

#### Start the server

```bash
flask --app app/esg run
``` 
#### Deactivate the virtualenv

Deactivate the virtualenv if needed:
```bash
$ deactivate
```
