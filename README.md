# Smart Face Recognition Attendance System

An automated, real-time facial recognition attendance system built using **OpenCV**, **Machine Learning (KNN)**, and a live **Streamlit Web Dashboard**.

---

## 🚀 Features

- **Real-Time Face Detection & Recognition**: Detects and tracks faces using Haar Cascades and classifies identities via K-Nearest Neighbors.
- **Voice Feedback**: Audio confirmation when attendance is logged using Windows SAPI Speech.
- **Attendance Logging**: Automatically saves daily attendance records into timestamped CSV files (`Attendance/Attendance_DD-MM-YYYY.csv`).
- **Live Streamlit Dashboard**: Real-time interactive web dashboard with metrics, search filter, historical log browsing, and one-click CSV export.
- **Fallback Architecture**: Native pure-NumPy KNN classifier fallback ensuring compatibility across Windows environments.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.14)
- A working **Webcam**

### 2. Install Required Dependencies
Open PowerShell or Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

Required packages:
- `opencv-contrib-python` (Computer Vision & Camera Capture)
- `numpy` (Numerical Computations)
- `scikit-learn` (KNN Classifier)
- `pandas` (Attendance Data Processing)
- `streamlit` & `streamlit-autorefresh` (Interactive Web Dashboard)
- `pywin32` (Windows Voice Feedback)

---

## 📖 How to Run the Project

### Step 1: Register New Faces
To enroll a new user into the face recognition system:
```bash
python add_faces.py
```
- Enter the person's name when prompted.
- Look directly at the webcam. The system will collect 100 face samples and save them in the `data/` directory.
- Press **`q`** anytime to cancel.

---

### Step 2: Run Real-time Face Recognition & Take Attendance
To start the recognition camera:
```bash
python test.py
```
- The camera window will appear embedded in the system template.
- Recognized names will appear above detected faces.
- **Key controls:**
  - Press **`o`**: Mark attendance for the recognized face. Voice feedback will confirm: *"Attendance Taken"*.
  - Press **`q`**: Quit and close the camera.

---

### Step 3: Launch the AttendAI Web UI & Dashboard
To start the modern full-stack web application with the complete AttendAI biometric interface:
```bash
python run_app.py
```
- Opens automatically in your default browser at `http://localhost:5000/login`.
- **Features included:**
  - **Login Portal**: Student & Faculty authentication with quick demo pills, password toggle, and SSO standard.
  - **Biometric Enrollment**: 2-step registration with academic credentials, live password verification, webcam capture/photo upload, 68-point facial landmark vector encoding, and database persistence.
  - **Student Attendance Dashboard**: Real-time KPI metrics, attendance progress donut chart, weekly distribution, subject breakdowns, and recent verification logs connected directly to `Attendance/` CSV files.
  - **Live Biometric Scanner**: Terminal sensor viewport with real webcam access, HUD reticle and laser sweep, state simulation, and real-time check-in stream.
  - **Historical Database Ledger**: Browse and search all historical check-ins across dates, filter unique attendees, and download raw CSV reports.

*(Optional)* You can also still run the legacy Streamlit viewer if desired:
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
face_recognition_project/
│
├── add_faces.py        # Script to capture and register new faces
├── test.py             # Script to run camera recognition & log attendance
├── app.py              # Streamlit web dashboard for viewing attendance
├── background.png      # Dashboard graphic frame for camera feed
├── requirements.txt    # Project dependencies list
├── README.md           # Documentation
│
├── data/               # Model and dataset storage
│   ├── haarcascade_frontalface_default.xml # Haar Cascade detector
│   ├── names.pkl                           # Pickled user names
│   ├── faces.pkl                           # Pickled face feature vectors
│   └── faces_data.pkl                      # Compatibility copy of face vectors
│
└── Attendance/         # CSV attendance storage
    └── Attendance_DD-MM-YYYY.csv # Daily attendance logs
```