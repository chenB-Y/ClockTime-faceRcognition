# Attendance Tracking Application

![WhatsApp Image 2024-03-29 at 12 39 01 (1)](https://github.com/chenB-Y/ClockTime-faceRcognition/assets/129218828/21ec4ef8-8977-47f3-93ce-d7ada4eb405f)


The Attendance Tracking Application is a tool designed to facilitate attendance management in various settings, such as schools, offices, or events. It allows users to log in and out using facial recognition technology and keeps track of attendance records.

## Features

- Face recognition-based login and logout system
- User registration with facial image capture
- Automatic attendance logging
- Import and export attendance data from AWS S3 bucket
- Web-based interface for easy access
- View attendance records on a website

## Technologies Used

- Python: Programming language used for backend development
- Tkinter: GUI toolkit for creating the graphical user interface
- Flask: Web framework used for backend server implementation
- OpenCV: Library for computer vision tasks, used for webcam integration and image processing
- AWS S3: Cloud storage service used for storing user data and attendance records
- Boto3: Python SDK for AWS, used for interacting with S3
- Face_recognition: Library for face recognition tasks
- DeepFace: Deep learning-based face recognition library

## Installation

1. Clone the repository:
   https://github.com/chenB-Y/ClockTime-faceRcognition.git
   
3. Navigate to the project directory:
   cd attendance-tracking
   
5. Create a .env file with the following data: <br>
   DB=./db <br>
  LOG_FILE=./log.txt <br>
  AWS_ACCESS_KEY_ID=<br>
  AWS_SECRET_ACCESS_KEY= <br>
Note: Replace `YOUR_AWS_ACCESS_KEY_ID` and `YOUR_AWS_SECRET_ACCESS_KEY` with your Amazon AWS access keys. If you don't have AWS credentials, you can obtain them from your AWS account.

6. Install dependencies:
   pip install -r requirements.txt


## Usage

1. Run the app:
   python main.py
   
3. Access the application through a web browser at `http://localhost:5000`.

4. Click on the "Register" button to register new users by capturing their facial images.

5. Use the "Clock In" and "Clock Out" buttons to log in and out, respectively.

6. Visit the website to view attendance records and generate reports.

## Contributing

Contributions to the Attendance Tracking Application are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your_feature_name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to the branch (`git push origin feature/your_feature_name`).
5. Create a new pull request.

