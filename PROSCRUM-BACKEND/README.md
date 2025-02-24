# PROSCRUM-API

## How to install the api

Python Version 3.10+ \
Python virtualenv:

```
python3 -m venv .venv
```

Add .gitignore:

```
echo "*" > .venv/.gitignore
```

Activate virtualenv:\
Linux, macOS:

```
source .venv/bin/activate
```

Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Windows Bash:

```
source .venv/Scripts/activate
```

Install from `requirements.txt`:

```
pip install -r requirements.txt
```

Deactivate the virtual environment:

```
deactivate
```

## Start the server:

Make sure to be in the activated virtual environment:
Activate virtualenv:\
Linux, macOS:

```
source .venv/bin/activate
```

Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

Windows Bash:

```
source .venv/Scripts/activate
```

Make sure to be in the `PROSCRUM-API` directory and enter:

```
uvicorn app.main:app --reload
```
