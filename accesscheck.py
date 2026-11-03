import requests


BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10


def check_status(name, actual, expected):
    if actual != expected:
        raise AssertionError(
            f"{name}: expected {expected}, got {actual}"
        )

    print(f"[PASS] {name}: expected {expected}, got {actual}")


def login(client, username, password):
    response = client.post(
        f"{BASE_URL}/login",
        data={
            "username": username,
            "password": password,
        },
        timeout=TIMEOUT,
    )
    check_status(f"{username} login", response.status_code, 200)


def run_checks():
    # No session cookie: this request must be rejected.
    response = requests.get(
        f"{BASE_URL}/notes/1",
        timeout=TIMEOUT,
    )
    check_status(
        "Anonymous access is blocked",
        response.status_code,
        401,
    )

    # Each user has a separate cookie jar.
    with requests.Session() as elliot, requests.Session() as alex:
        login(elliot, "elliot", "training-password")

        response = elliot.get(
            f"{BASE_URL}/notes/1",
            timeout=TIMEOUT,
        )
        check_status(
            "Elliot can access his own note",
            response.status_code,
            200,
        )

        response = elliot.get(
            f"{BASE_URL}/notes/2",
            timeout=TIMEOUT,
        )
        check_status(
            "Elliot cannot access Alex's note",
            response.status_code,
            403,
        )

        login(alex, "alex", "alex-password")

        response = alex.get(
            f"{BASE_URL}/notes/2",
            timeout=TIMEOUT,
        )
        check_status(
            "Alex can access his own note",
            response.status_code,
            200,
        )

        response = alex.get(
            f"{BASE_URL}/notes/1",
            timeout=TIMEOUT,
        )
        check_status(
            "Alex cannot access Elliot's note",
            response.status_code,
            403,
        )

        # Check before logout: authentication is required first.
        response = elliot.get(
            f"{BASE_URL}/notes/99",
            timeout=TIMEOUT,
        )
        check_status(
            "Nonexistent note returns 404",
            response.status_code,
            404,
        )

        response = elliot.post(
            f"{BASE_URL}/logout",
            timeout=TIMEOUT,
        )
        check_status(
            "Elliot logout",
            response.status_code,
            200,
        )

        response = elliot.get(
            f"{BASE_URL}/notes/1",
            timeout=TIMEOUT,
        )
        check_status(
            "Access after logout is blocked",
            response.status_code,
            401,
        )

    print("\nAll 10 checks passed.")


def main():
    try:
        run_checks()
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] HTTP request failed: {error}")
        return 1
    except AssertionError as error:
        print(f"[FAIL] {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())