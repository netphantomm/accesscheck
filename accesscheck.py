import requests  #importing requests library to make HTTP requests

url = "http://127.0.0.1:5000/notes/1" #Url for accessing the note with id 1

response = requests.get(url, timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds

print("Status:", response.status_code) #Printing the status code of the response received from the GET request

assert response.status_code == 401, "Anonymous access should return 401" #Asserting that the response status code is 401 for anonymous access

print("[PASS] Anonymous access is blocked") #Printing a success message if anonymous access is blocked

elliot = requests.Session() #Creating a session object for Elliot to maintain cookies and session data across requests

login_response = elliot.post("http://127.0.0.1:5000/login",
    data={
        "username": "elliot",
        "password": "training-password",
    },
    timeout=10,
)  #Making a POST request to the login endpoint with Elliot's credentials and a timeout of 10 seconds
assert login_response.status_code == 200, "Elliot login failed" #Asserting that the response status code is 200 for a successful login attempt by Elliot
print("[PASS] Elliot login succeeded") #Printing a success message if Elliot's login is successful

note_response = elliot.get(url, timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds using Elliot's session
print("Status:", note_response.status_code) #Printing the status code of the response received from the GET request made by Elliot
print("Text:", note_response.text) #Printing the text content of the response received from the GET request made by Elliot

assert note_response.status_code == 200, "Elliot should be able to access his own note" #Asserting that the response status code is 200 for a successful access attempt by Elliot to his own note
print("[PASS] Elliot can access his own note") #Printing a success message if Elliot can access his own note

url = "http://127.0.0.1:5000/notes/2"
note_response = elliot.get(url, timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds using Elliot's session to access Alex's note
print("Status:", note_response.status_code) #Printing the status code of the response received from the GET request made by Elliot to access Alex's note
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
) #Making a POST request to the login endpoint with Alex's credentials and a timeout of 10 seconds
assert login_response.status_code == 200, "Alex login failed" #Asserting that the response status code is 200 for a successful login attempt by Alex
print("[PASS] Alex login succeeded") #Printing a success message if Alex's login is successful
alex_response = alex.get("http://127.0.0.1:5000/notes/2", timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds using Alex's session to access his own note
print("Status:", alex_response.status_code)
assert alex_response.status_code == 200, "Alex should be able to access his own note"
print("[PASS] Alex can access his own note")
alex_response2 = alex.get("http://127.0.0.1:5000/notes/1", timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds using Alex's session to access Elliot's note
print("Status:", alex_response2.status_code)
assert alex_response2.status_code == 403, "Alex should not be able to access Elliot's note"
print("[PASS] Alex cannot access Elliot's note")
missing_note_response = elliot.get("http://127.0.0.1:5000/notes/99", timeout=10)
assert missing_note_response.status_code == 404, "Expected 404 for non-existent note"
print("[PASS] Nonexistent note access returns 404") #Printing a success message if access to a non-existent note returns a 404 status code
elliot_response = elliot.post("http://127.0.0.1:5000/logout", timeout=10) #Making a POST request to the logout endpoint with a timeout of 10 seconds using Elliot's session to log out
print("Status:", elliot_response.status_code)
assert elliot_response.status_code == 200, "Elliot logout failed"
print("[PASS] Elliot logout succeeded")
elliot_response2 = elliot.get("http://127.0.0.1:5000/notes/1", timeout=10) #Making a GET request to the specified URL with a timeout of 10 seconds using Elliot's session to access a note after logout
print("Status:", elliot_response2.status_code)
assert elliot_response2.status_code == 401, "Elliot should not be able to access notes after logout" #Asserting that the response status code is 401 for a failed access attempt by Elliot to a note after logout
print("[PASS] Access after logout is blocked") #Printing a success message if access after logout is blocked for Elliot