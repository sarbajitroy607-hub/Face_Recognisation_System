import requests
import json

BASE = "http://localhost:5000"

print("==================================================")
print(" AttendAI Authentication & Real Data Test Suite  ")
print("==================================================")

# ----------------------------------------------------------------
# TEST 1: Unauthenticated Protection (Strict Access Control)
# ----------------------------------------------------------------
print("\n[TEST 1] Testing Strict Unauthenticated Redirections...")
client_anon = requests.Session()

for endpoint in ["/dashboard", "/scanner", "/history"]:
    r = client_anon.get(f"{BASE}{endpoint}", allow_redirects=False)
    assert r.status_code == 302, f"Expected 302 redirect for {endpoint}, got {r.status_code}"
    assert "/login" in r.headers.get("Location", ""), f"Expected redirect to /login for {endpoint}"
    print(f"  [PASS] Anonymous access to {endpoint} correctly blocked -> 302 Redirect to /login")

# ----------------------------------------------------------------
# TEST 2: Authentication Failures (Wrong Password & Non-existent User)
# ----------------------------------------------------------------
print("\n[TEST 2] Testing Authentication Error Handling...")

# Non-existent user
r = client_anon.post(f"{BASE}/api/login", json={"userId": "UNKNOWN_USER_999", "password": "anypassword"})
assert r.status_code == 404, f"Expected 404 for unknown user, got {r.status_code}"
assert r.json()["success"] is False
print("  [PASS] Non-existent user returns 404 with error message:", r.json()["message"])

# Wrong password
r = client_anon.post(f"{BASE}/api/login", json={"userId": "24IUT0010235", "password": "WrongPassword123"})
assert r.status_code == 401, f"Expected 401 for bad password, got {r.status_code}"
assert r.json()["success"] is False
print("  [PASS] Incorrect password returns 401 with error message:", r.json()["message"])

# Empty credentials
r = client_anon.post(f"{BASE}/api/login", json={"userId": "", "password": ""})
assert r.status_code == 400, f"Expected 400 for empty credentials, got {r.status_code}"
print("  [PASS] Empty credentials return 400:", r.json()["message"])

# ----------------------------------------------------------------
# TEST 3: Successful Authentication with Real User
# ----------------------------------------------------------------
print("\n[TEST 3] Testing Real User Authentication...")
auth_session = requests.Session()

# Login with Student ID
r = auth_session.post(f"{BASE}/api/login", json={"userId": "24IUT0010235", "password": "sarbajit2908"})
assert r.status_code == 200, f"Expected 200 for valid login, got {r.status_code}"
data = r.json()
assert data["success"] is True
assert data["user"]["name"] == "Sarbajit Roy"
print(f"  [PASS] Login successful via Student ID: Welcome, {data['user']['name']} ({data['user']['id']})")

# Login with Email also works
email_session = requests.Session()
r_email = email_session.post(f"{BASE}/api/login", json={"userId": "sarbajitroy607@gmail.com", "password": "sarbajit2908"})
assert r_email.status_code == 200, f"Expected 200 for email login, got {r_email.status_code}"
assert r_email.json()["user"]["name"] == "Sarbajit Roy"
print("  [PASS] Login successful via Email: sarbajitroy607@gmail.com")

# ----------------------------------------------------------------
# TEST 4: Authenticated Access to Protected Pages
# ----------------------------------------------------------------
print("\n[TEST 4] Testing Authenticated Access to Protected Pages...")

# Dashboard
r = auth_session.get(f"{BASE}/dashboard")
assert r.status_code == 200, f"Expected 200 for dashboard, got {r.status_code}"
assert "Welcome back, Sarbajit Roy" in r.text
assert "24IUT0010235" in r.text
print("  [PASS] Dashboard rendered with authenticated user profile Sarbajit Roy")

# Scanner
r = auth_session.get(f"{BASE}/scanner")
assert r.status_code == 200, f"Expected 200 for scanner, got {r.status_code}"
assert "Biometric Terminal: LH-102" in r.text
assert "Sarbajit Roy" in r.text
print("  [PASS] Scanner page rendered with authenticated session")

# History
r = auth_session.get(f"{BASE}/history")
assert r.status_code == 200, f"Expected 200 for history, got {r.status_code}"
assert "Institutional Attendance Database Ledger" in r.text
assert "Sarbajit Roy" in r.text
print("  [PASS] History & Database Ledger rendered with active session")

# ----------------------------------------------------------------
# TEST 5: Attendance Recording & Persistence
# ----------------------------------------------------------------
print("\n[TEST 5] Testing Attendance Logging & Database Synchronization...")
r = auth_session.post(f"{BASE}/api/mark_attendance", json={"name": "Sarbajit Roy", "course": "Biometric Gateway Test"})
assert r.status_code == 200, f"Expected 200 for mark_attendance, got {r.status_code}"
assert r.json()["success"] is True
print("  [PASS] Attendance check-in recorded:", r.json()["message"])

r = auth_session.get(f"{BASE}/api/attendance")
assert r.status_code == 200
records = r.json()["records"]
assert len(records) > 0
assert any(rec["name"] == "Sarbajit Roy" for rec in records)
print(f"  [PASS] Database verified: {len(records)} verified check-in(s) for today")

# ----------------------------------------------------------------
# TEST 6: Registration & Duplicate Prevention
# ----------------------------------------------------------------
print("\n[TEST 6] Testing Registration & Duplicate Prevention...")

# Duplicate Student ID should be rejected
r = client_anon.post(f"{BASE}/api/register", json={
    "fullName": "Duplicate Student",
    "studentId": "24IUT0010235",
    "email": "different.email@univ.edu",
    "password": "Password123"
})
assert r.status_code == 409, f"Expected 409 conflict for duplicate ID, got {r.status_code}"
print("  [PASS] Duplicate Student ID rejected:", r.json()["message"])

# Duplicate Email should be rejected
r = client_anon.post(f"{BASE}/api/register", json={
    "fullName": "Duplicate Email Student",
    "studentId": "NEW_STUDENT_001",
    "email": "sarbajitroy607@gmail.com",
    "password": "Password123"
})
assert r.status_code == 409, f"Expected 409 conflict for duplicate email, got {r.status_code}"
print("  [PASS] Duplicate Email rejected:", r.json()["message"])

# ----------------------------------------------------------------
# TEST 7: Logout & Session Invalidation
# ----------------------------------------------------------------
print("\n[TEST 7] Testing Logout & Session Invalidation...")
r = auth_session.get(f"{BASE}/api/logout", allow_redirects=False)
assert r.status_code == 302, f"Expected 302 redirect after logout, got {r.status_code}"
assert "/login" in r.headers.get("Location", "")
print("  [PASS] Logout endpoint successfully cleared session and redirected to /login")

# Verify session is destroyed
r = auth_session.get(f"{BASE}/dashboard", allow_redirects=False)
assert r.status_code == 302, f"Expected 302 redirect after session invalidation, got {r.status_code}"
print("  [PASS] Subsequent access to /dashboard is blocked -> 302 Redirect to /login")

print("\n" + "="*50)
print(" ALL 7 AUTHENTICATION & DATA TESTS PASSED (100%)! ")
print("==================================================")
