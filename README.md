# AccessCheck

A Python CLI tool that runs 10 authentication and access-control
checks against the local AppSec Notes Lab.

## Target application

This tool expects the routes, demo users and notes provided by:
https://github.com/netphantomm/appsec-notes-lab

Start that application in a separate terminal:

```bash
cd ~/appsec-notes-lab
.venv/bin/python -m flask --app app run --host 127.0.0.1 --port 5000
```

## Installation

Run from the AccessCheck project directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Usage

With the target application running:

```bash
.venv/bin/python accesscheck.py
echo $?
```

The default target is http://127.0.0.1:5000.
The target URL is configured in BASE_URL inside accesscheck.py.

## Checks

- Anonymous access to a note returns 401.
- Elliot and Alex can log in.
- Both users can access their own notes.
- Both users receive 403 when requesting the other user's note.
- An authenticated request for a nonexistent note returns 404.
- Logout returns 200.
- Access to a protected note after logout returns 401.

## Results

- [PASS]: the response status matches the expected status.
- [FAIL]: a status does not match; execution stops.
- [ERROR]: an HTTP request failed.

Exit code 0 means all checks passed.
Exit code 1 means a check or request failed.

## Validation

Temporarily disabling the lab's ownership check caused AccessCheck
to detect a 200 response where 403 was expected and exit with code 1.
After restoring the ownership check, all 10 checks passed.

## Limitations

- Designed for this specific local learning lab.
- Uses public demo credentials defined in the source code.
- Checks HTTP status codes, not response contents.
- Stops at the first failure.
- Passing these checks does not prove the application is fully secure.

## Run with Docker Compose

Keep `accesscheck` and `appsec-notes-lab` in sibling directories.
From the `accesscheck` directory, run:

```bash
docker compose up --build --exit-code-from accesscheck
```

Compose waits for Flask to respond, runs the 10 access checks,
then stops Flask. Exit code `0` means all checks passed.
Flask is reached over the Compose network without publishing a host port.
