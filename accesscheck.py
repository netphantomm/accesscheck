import requests

url = "http://127.0.0.1:5000/notes/1"

response = requests.get(url, timeout=10)

print("Status:", response.status_code)

assert response.status_code == 401, "Anonymous access should return 401"

print("[PASS] Anonymous access is blocked")

elliot = requests.Session()

login_response = elliot.post(
    "http://127.0.0.1:5000/login",
    data={
        "username": "elliot",
        "password": "training-password",
    },
    timeout=10,
)
assert login_response.status_code == 200, "Elliot login failed"
print("[PASS] Elliot login succeeded")

note_response = elliot.get(url, timeout=10)
print("Status:", note_response.status_code)
print("Text:", note_response.text)

assert note_response.status_code == 200, "Elliot should be able to access his own note"
print("[PASS] Elliot can access his own note")

url = "http://127.0.0.1:5000/notes/2"
note_response = elliot.get(url, timeout=10)
print("Status:", note_response.status_code)
assert note_response.status_code == 403, "Expected 403 for Elliot accessing Alex's note"
print("[PASS] Elliot cannot access Alex's note")


alex = requests.Session()
login_response = alex.post(
    "http://127.0.0.1:5000/login",
    data={
        "username": "alex",
        "password": "alex-password",
    },
    timeout=10,
)
assert login_response.status_code == 200, "Alex login failed"
print("[PASS] Alex login succeeded")
alex_response = alex.get("http://127.0.0.1:5000/notes/2", timeout=10)
print("Status:", alex_response.status_code)
assert alex_response.status_code == 200, "Alex should be able to access his own note"
print("[PASS] Alex can access his own note")

alex_response2 = alex.get("http://127.0.0.1:5000/notes/1", timeout=10)
print("Status:", alex_response2.status_code)
assert alex_response2.status_code == 403, "Alex should not be able to access Elliot's note"
print("[PASS] Alex cannot access Elliot's note")
