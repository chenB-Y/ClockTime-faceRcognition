import threading
import os
import os.path
import datetime
import util
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from server import FlaskServer
from logic import login, logout, accept_register_new_user

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1110x520+350+100")
        self.main_window.title("Attendance Application")

        # Create a label for displaying date and time
        self.date_time_label = tk.Label(self.main_window, font=("Arial", 20))
        self.date_time_label.place(relx=0.5, y=10, anchor="n")
        self.update_date_time()

        self.additional_text_label = tk.Label(self.main_window, text="Time Clock ⏱", font=("Arial", 30))
        self.additional_text_label.place(x=770, y=50)  # Positioned below the date and time label

        self.additional_text_label = tk.Label(self.main_window, text="Attendance tracking application.\n "
                                                                     "ClockIn at the entrance and ClockOut exit ",
                                              font=("Arial", 12))
        self.additional_text_label.place(x=750, y=100)  # Positioned below the date and time label

        self.login_button_main_window = util.get_button(self.main_window,
                                                        'Clock In', 'green', lambda: login(self.most_recent_capture_arr))
        self.login_button_main_window.place(x=750, y=205)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Register', 'gray',
                                                                    self.register_new_user, fg='white')
        self.register_new_user_button_main_window.place(x=750, y=425)

        self.logout_button_main_window = util.get_button(self.main_window,
                                                         'Clock Out', 'blue', lambda: logout(self.most_recent_capture_arr))
        self.logout_button_main_window.place(x=750, y=315)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=15, y=50, width=700, height=450)

        self.add_webcam(self.webcam_label)

        # Start the Flask server in a separate thread
        flask_server = FlaskServer()
        server_thread = threading.Thread(target=flask_server.start_server)
        server_thread.start()

        self.main_window.mainloop()


    def update_date_time(self):
        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format date and time
        formatted_date_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Update the label text
        self.date_time_label.config(text=formatted_date_time)

        # Schedule the next update after 1000 ms (1 second)
        self.main_window.after(1000, self.update_date_time)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1110x520+350+100")

        self.accept_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Accept', 'green',
            lambda: accept_register_new_user(self.register_new_user_window,
                                             self.entry_text_register_new_user,
                                             self.register_new_user_capture))
        self.accept_button_register_new_user_window.place(x=750, y=300)


        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again',
                                                                         'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if frame is not None:  # Check if frame is not empty
            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

if __name__ == "__main__":
    app = App()
