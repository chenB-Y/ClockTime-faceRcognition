import os
import threading
import time
import schedule
from deepface import DeepFace
from flask import Flask, request, render_template
import util
from s3_storage import importUsers, uploadUsers, downloadAttendanceSheet, uploadAttendanceSheet
import subprocess
from dotenv import load_dotenv
from logic import search_and_modify_name_in_file

class FlaskServer:
    def __init__(self):
        self.app = Flask(__name__)

        load_dotenv()
        self.db_dir = os.getenv("DB")
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = os.getenv("LOG_FILE")

        @self.app.route('/', methods=['GET'])
        def index():
            return render_template('index.html')

        @self.app.route('/compare_faces', methods=['POST'])
        def compare_faces():
            try:
                if 'image' not in request.files:
                    return 'No image sent', 400

                image = request.files['image']
                unknown_img_path = './tmp.jpg'
                image.save(unknown_img_path)
                type = request.form['type']

                output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])
                output = str(output)
                print(output)
                name = ""
                if output.count("tmp") > 1:
                    print("more than one person is similar")
                    dfs = DeepFace.find(img_path=unknown_img_path, db_path=self.db_dir)
                    print(dfs)
                    if dfs:
                        # Extract the identity of the image from the first row
                        first_row_identity = dfs[0]['identity'][0]
                        print(first_row_identity)
                        name_without_extension = os.path.splitext(first_row_identity)[0]
                        name_without_extension = os.path.basename(name_without_extension)
                        print(name_without_extension)
                        name = name_without_extension
                    else:
                        print("Empty DataFrame")
                        util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')
                else:
                    name = output.split(',')[1][:-5]

                if name in ['no_persons_found', 'unknown_person']:
                    return 'Unknown user', 404
                else:
                    current_date = datetime.now()
                    downloadAttendanceSheet()
                    if type == "login":
                        with open(self.log_path, 'a') as file:
                            file.write(
                                '{} {}/{}/{} ; Entrance time-{:02d}:{:02d}\n'.format(name, current_date.day,
                                                                                     current_date.month,
                                                                                     current_date.year,
                                                                                     current_date.hour,
                                                                                     current_date.minute))
                    elif type == "logout":
                        search_and_modify_name_in_file(name)
                    uploadAttendanceSheet()
                    return name, 200

            except Exception as e:
                print("Exception:", e)
                return 'Error', 500

        @self.app.route('/register_user', methods=['POST'])
        def register_user():
            try:
                # Check if the request contains the image file and user name
                if 'image' not in request.files or 'name' not in request.form:
                    return "missing parameter", 400

                # Get the image file and user name from the request
                image = request.files['image']
                name = request.form['name']

                # Save the image to the appropriate directory with the user's name as the filename
                image.save(os.path.join('./db', '{}.jpg'.format(name)))
                uploadUsers(name)
                # its also ok to do like this
                # cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)),  self.register_new_user_capture)

                # Return a success response
                return 'User registered successfully', 200

            except Exception as e:
                # Handle any exceptions
                print("Exception:", e)
                return 'Error occurred', 500

        from datetime import datetime

        @self.app.route('/get_log_file', methods=['GET'])
        def get_log_file():
            try:
                total_time = ""
                if 'name' in request.args:
                    name = request.args.get('name')
                    downloadAttendanceSheet()
                    with open(self.log_path, 'r') as file:
                        lines_with_name = []
                        total_hours = 0
                        total_minutes = 0
                        for line in file:
                            if name in line:
                                if 'month' in request.args:
                                    month = request.args.get('month')
                                    if month:
                                        date_str = line.split(' ; ')[0].split(' ')[1]
                                        date = datetime.strptime(date_str, '%d/%m/%Y')
                                        if date.strftime('%m') == month:
                                            lines_with_name.append(line.strip())
                                            if "Total Time is:" in line:
                                                total_day_time = line.split("Total Time is:")[1].strip()
                                                # Split the reading into hours and minutes
                                                hours, minutes = map(int, total_day_time.split(':'))
                                                total_hours += hours
                                                total_minutes += minutes
                                else:
                                    lines_with_name.append(line.strip())
                                    if "Total Time is:" in line:
                                        total_day_time = line.split("Total Time is:")[1].strip()
                                        # Split the reading into hours and minutes
                                        hours, minutes = map(int, total_day_time.split(':'))
                                        total_hours += hours
                                        total_minutes += minutes

                        if len(lines_with_name) == 0:
                            log_content = f"There is no information about {name}."
                        else:
                            log_content = '\n'.join(lines_with_name)
                            total_hours += total_minutes // 60
                            total_minutes %= 60
                            total_time = f"Total time : {total_hours}:{total_minutes}"

                else:
                    # Read the content of the log file
                    with open(self.log_path, 'r') as file:
                        log_content = file.read()

                # Return the log content as the response
                return render_template('log.html', log_content=log_content, total_time=total_time), 200

            except FileNotFoundError:
                return "Log file not found", 404
            except Exception as e:
                print("Exception:", e)
                return 'Error occurred', 500

    def start_server(self):

        scheduling_thread = threading.Thread(target=self.schedule_import_users)
        scheduling_thread.start()

        self.app.run(host='0.0.0.0', port=5000)

    def schedule_import_users(self):
        # Schedule the import_users function to run every 24 hours
        schedule.every().day.at("05:00").do(importUsers)

        # Run the scheduler in an infinite loop
        while True:
            schedule.run_pending()
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage


