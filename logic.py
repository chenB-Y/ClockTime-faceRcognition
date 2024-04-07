import datetime
import os
from io import BytesIO
from dotenv import load_dotenv
import cv2
import requests
import util

load_dotenv()
log_path = os.getenv("LOG_FILE")
db_dir =os.getenv("DB")
def login(most_recent_capture_arr):
    try:
        # Save the most recent capture as a temporary image file
        unknown_img_path = './tmp.jpg'
        cv2.imwrite(unknown_img_path, most_recent_capture_arr)
        # Send a POST request to the Flask server to compare faces
        with open(unknown_img_path, 'rb') as file:
            files = {'image': file}
            data = {'type': "login"}
            response = requests.post('http://localhost:5000/compare_faces', files=files, data=data)
            print(response.status_code)

        os.remove(unknown_img_path)

        # Process the server response
        if response.status_code == 200:
            name = response.text
            # Successful response, display welcome message
            util.msg_box('Welcome!', 'Welcome back, {}'.format(name))
        elif response.status_code == 404:
            # Unknown user, display appropriate message
            util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')
        else:
            # Error occurred, display error message
            util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')
    except Exception as e:
        # Handle any exceptions
        print("Exception:", e)
        util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')


def logout(most_recent_capture_arr):
    try:
        unknown_img_path = './tmp.jpg'
        cv2.imwrite(unknown_img_path,most_recent_capture_arr)  # inwrite  used to save an image to a specified file.
        with open(unknown_img_path, 'rb') as file:
            files = {'image': file}
            data = {'type': "logout"}
            response = requests.post('http://localhost:5000/compare_faces', files=files, data=data)
            print(response.status_code)

        os.remove(unknown_img_path)

        if response.status_code == 200:
            name = response.text
            util.msg_box('GoodBye!', 'GoodBye {}, Have a nice day :) '.format(name))
        elif response.status_code == 404:
            # Unknown user, display appropriate message
            util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')
        else:
            # Error occurred, display error message
            util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')
    except Exception as e:
        # Handle any exceptions
        print("Exception:", e)
        util.msg_box('Upss...', 'Unknown user!\n Please register new user or try again.')



def search_and_modify_name_in_file(target_name):
    is_login = False
    try:
        # Open the file in read and write mode
        with open(log_path, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            date = datetime.datetime.now()
            for line in lines:
                if target_name in line and "Entrance" in line:
                    date_str = line.split(';')[0].split()[1]  # Extract "28/3/2024" part
                    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
                    # Get today's date
                    today_date = datetime.date.today()
                    if date_obj == today_date:
                        print("The date in the line is today's date.")
                        is_login = True
                        # Modify the line if the target name is found
                        given_time = datetime.datetime.strptime(line.split('-')[1].strip(), "%H:%M")
                        current_time = datetime.datetime.now()
                        time_difference = current_time - given_time
                        hours = time_difference.seconds // 3600
                        minutes = (time_difference.seconds % 3600) // 60
                        line = line.replace("Entrance", "start")
                        new_line = line.rstrip('\n')
                        additional_text = ',  End time-{}. Total Time is:{:02d}:{:02d} \n'.format(
                            datetime.datetime.now().strftime("%H:%M"), hours, minutes)
                        new_line = new_line + additional_text
                        file.write(new_line)
                        break
                    else:
                        print("The date in the line is not today's date.")
                        file.write(line)
                else:
                    file.write(line)
            if not is_login:
                new_line = '{} {}/{}/{} ;  End time-{:02d}:{:02d}.\n'.format(target_name, date.day, date.month,
                                                                             date.year, date.hour, date.minute)
                file.write(new_line)
            # Truncate the file to remove any remaining lines
            file.truncate()

    except FileNotFoundError:
        print(f"File not found.")



def accept_register_new_user(register_new_user_window, entry_text_register_new_user, register_new_user_capture):
    try:
        image_data = register_new_user_capture
        name = entry_text_register_new_user.get(1.0, "end-1c")

        # Convert the image data (NumPy array) to bytes
        image_bytes = cv2.imencode('.jpg', image_data)[1].tobytes()

        # Create a BytesIO buffer from the image data
        image_buffer = BytesIO(image_bytes)
        filename = '{}.jpg'.format(name)

        # Create a file-like object from the BytesIO buffer
        image_file = {'image': (filename, image_buffer)}
        data = {'name': name}

        # Send the POST request to the Flask server
        response = requests.post('http://localhost:5000/register_user', files=image_file, data=data)

        # Process the server response
        if response.status_code == 200:
            # Display a success message if the registration was successful
            util.msg_box('Success!', 'User was registered successfully!')
        else:
            # Display an error message if registration failed
            util.msg_box('Error', 'Failed to register user. Please try again.')

        # Close the register new user window
        register_new_user_window.destroy()

    except Exception as e:
        # Handle any exceptions
        print("Exception:", e)
        util.msg_box('Error', 'An error occurred. Please try again.')
