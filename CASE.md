## CASE: READING ANOTHER USER'S NOTE

## Scenario

In my local Flask lab, Elliot and Alex each own private notes. Elliot signs in and requests 'GET /notes/2', which belongs to Alex.
The expected response is '403 Forbidden'.

## Finding and impact

I deliberately disabled the ownership check to simulate an access-control bug. The server returned '200 OK' and disclosed Alex's note to Elliot.
Any signed user could read another user's note if they knew its ID.

## FIX

Before returning the note, Flask compares its 'owner_id' which the user ID from the session. If they differ, Flask returns '403'.

## Evidence

| Lab state | Response to Elliot's request | AccessCheck result |
| --- | --- | --- |
| Ownership check disabled | `200 OK` | `[FAIL]`, exit code `1` |
| Ownership check restored | `403 Forbidden` | `[PASS]`; all 10 checks passed, exit code `0` |

## How to run the checks

Clone 'accesscheck' and 'appsec-notes-lab' into sibling directories. From 'accesscheck', run:
```bash
docker compose up --build --exit-code-from accesscheck
```

Github Actions runs the same suite on changes to accesscheck.
The workflow passed with the ownership check in place.
