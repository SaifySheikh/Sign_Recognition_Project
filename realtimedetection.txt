from keras.models import model_from_json
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw
import time
import pyttsx3
from tkinter import messagebox
import webbrowser

json_file = open("signlanguagedetectionmodel48x48.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("signlanguagedetectionmodel48x48.h5")

label=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I','J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','blank']

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

def create_circular_image(image_path, size):
    original_image = Image.open(image_path)
    original_image = original_image.resize(size, Image.BICUBIC)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    result.paste(original_image, (0, 0), mask)
    return result


def on_developers_click():
    developers_window = tk.Toplevel(root)
    developers_window.title("Developers")
    window_width = 800
    window_height = 300
    screen_width = developers_window.winfo_screenwidth()
    screen_height = developers_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    developers_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    developers_window.configure(bg="#0B0B45")

    canvas = tk.Canvas(developers_window, bg="#0B0B45")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(developers_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = ttk.Frame(canvas, style="TFrame")
    canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)

    heading_label = tk.Label(content_frame, text="Developers", font=("Helvetica", 24), background="#0B0B45", foreground="white")
    heading_label.pack(pady=(20, 10))

    images_info = [("Images/Saify.jpeg", "Mohammad Saify Sheikh (Team Leader)"),
                   ("Images/Himanshu.jpg", "Himanshu Shrigiriwar"),
                   ("Images/Soham.jpg", "Soham Bedi"),
                   ("Images/image4.jpeg", "Rugved Mhatre")]

    for image_path, name in images_info:
        developer_frame = ttk.Frame(content_frame, style="TFrame", padding=10)
        developer_frame.pack(side="top", pady=10)

        circular_image = create_circular_image(image_path, (200, 200))

        circular_image_photo = ImageTk.PhotoImage(circular_image)

        image_label = tk.Label(developer_frame, image=circular_image_photo, background="#0B0B45")
        image_label.image = circular_image_photo
        image_label.pack(side="left", padx=10)

        developer_name_label = tk.Label(developer_frame, text=name, font=("Helvetica", 14), background="#0B0B45", foreground="white")
        developer_name_label.pack(side="left", padx=10, pady=5)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    developers_window.mainloop()



engine = pyttsx3.init()
engine.setProperty('rate', 125)

def on_audio_click():
    print("Audio button clicked!")
    global current_sentence
    if current_sentence:
        engine.say(current_sentence)
        engine.runAndWait()
    else:
        engine.say("Nothing to say")
        engine.runAndWait()    

def get_suggestions(current_word):
    suggestions = ['APPLE', 'BANANA', 'ORANGE', 'PEAR', 'PEACH', 'PINEAPPLE', 'HI', 'HELLO', 'HEY', 'GOOD MORNING', 'GOOD AFTERNOON', 'GOOD EVENING', 
               'HOWDY', 'GREETINGS', 'SALUTATIONS', 'WHATS UP', 'SUP', 
               'HOWS IT GOING', 'NICE TO MEET YOU', 'PLEASED TO MEET YOU', 'WELCOME', 
               'HOLA', 'BONJOUR', 'CIAO', 'SALAAM', 'NAMASTE', 'DOG', 'CAT', 'BIRD', 'ELEPHANT', 'LION', 'TIGER', 
               'HOUSE', 'CAR', 'BIKE', 'PLANE', 'TRAIN', 'BOAT', 
               'RED', 'BLUE', 'GREEN', 'YELLOW', 'ORANGE', 'PURPLE', 
               'HAPPY', 'SAD', 'ANGRY', 'EXCITED', 'CALM', 'SURPRISED', 
               'EAT', 'DRINK', 'SLEEP', 'RUN', 'WALK', 'JUMP', 
               'BIG', 'SMALL', 'TALL', 'SHORT', 'THIN', 
               'HOT', 'COLD', 'FAST', 'SLOW', 'OLD', 'NEW',
               'APPLE', 'BALL', 'CAT', 'DOG', 'ELEPHANT', 'FISH',
               'GOAT', 'HAT', 'ICE', 'JUICE', 'KITE', 'LION',
               'MOON', 'NEST', 'OWL', 'PEAR', 'QUEEN', 'RAT',
               'SUN', 'TREE', 'UMBRELLA', 'VAN', 'WATCH', 'RCOEM',
               'YES', 'NO', 'ZEBRA', 'CARROT', 'BUS', 'TRAIN', 'AIRPLANE',
               'TRUCK', 'ROBOT', 'ROCKET', 'PIANO', 'GUITAR', 'VIOLIN',
               'COMPUTER', 'PHONE', 'TABLET', 'CAMERA', 'RAMDEOBABA', 'OVEN',
               'CHAIR', 'TABLE', 'BED', 'LAMP', 'MIRROR', 'WINDOW','COLLEGE','ENGINEERING','AND','MANAGEMENT']

    
    return [suggestion for suggestion in suggestions if suggestion.startswith(current_word)]

def suggestion_click(suggestion):
    global current_word, current_sentence
    current_sentence += " " + suggestion
    prediction_sentence_label.config(text=current_sentence)
    current_word = ""
    prediction_word_label.config(text=current_word)
    prediction_letter_label.config(text="")
    # Destroy all suggestion buttons
    for widget in content_frame.winfo_children():
        if isinstance(widget, ttk.Button):
            widget.destroy()

cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Sign Language to Text")

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.configure(bg="#0B0B45")


style = ttk.Style()
style.configure("TFrame", background="#0B0B45")
style.configure("TLabel", background="#0B0B45", foreground="white", font=("Poppins", 18))
style.configure("TButton", background="#00c04b", foreground="#00c04b", font=("Poppins", 12))

content_frame = ttk.Frame(root, style="TFrame")
content_frame.pack(expand=True, fill='both', padx=20, pady=20)

heading_label = ttk.Label(content_frame, text="Sign Language to Text", font=("Helvetica", 24))
heading_label.pack(pady=(0, 20))

letter_label = ttk.Label(content_frame, text="Letter:")
letter_label.pack(anchor='w', padx=5, pady=5)
prediction_letter_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_letter_label.pack(anchor='w', padx=5, pady=5)

word_label = ttk.Label(content_frame, text="Word:")
word_label.pack(anchor='w', padx=5, pady=5)
prediction_word_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_word_label.pack(anchor='w', padx=5, pady=5)

sentence_label = ttk.Label(content_frame, text="Sentence:")
sentence_label.pack(anchor='w', padx=5, pady=5)
prediction_sentence_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_sentence_label.pack(anchor='w', padx=5, pady=5)

audio_button = ttk.Button(root, text="Audio", command=on_audio_click)
audio_button.pack(side="top", anchor="ne", padx=10, pady=10)

developers_button = ttk.Button(root, text="Developers", command=on_developers_click)
developers_button.pack(side="top", anchor="ne", padx=10, pady=10)

suggestion_label = ttk.Label(content_frame, text="", font=("Helvetica", 12))
suggestion_label.pack(side="bottom", padx=20, pady=20, fill='both', expand=True)

start_time = None
predicted_letter = ""
current_word = ""
current_sentence = ""

def update_frame():
    global start_time, predicted_letter, current_word, current_sentence
    
    _, frame = cap.read()
    cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 1)

    cropframe = frame[40:300, 0:300]
    cropframe = cv2.cvtColor(cropframe, cv2.COLOR_BGR2GRAY)
    cropframe = cv2.resize(cropframe, (48, 48))
    cropframe = extract_features(cropframe)

    pred = model.predict(cropframe)
    max_accu = np.max(pred) * 100
    pred_label = label[pred.argmax()]
    
    cv2.rectangle(frame, (0, 0), (300, 40), (0, 165, 255), -1)
    if pred_label != 'blank':
        accu = "{:.2f}".format(max_accu)
        cv2.putText(frame, f'{pred_label}  {accu}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        accu = "{:.2f}".format(max_accu)
        cv2.putText(frame, f'{pred_label}  {accu}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Sign Language to Text", frame)

    if max_accu > 85:
        if start_time is not None:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 5 and pred_label != 'blank':
                predicted_letter = pred_label
                prediction_letter_label.config(text=predicted_letter)
                start_time = None
                if pred_label != 'blank':
                    current_word += pred_label
                    prediction_word_label.config(text=current_word)
                    update_suggestion(current_word)
            elif elapsed_time >= 5 and pred_label == 'blank':
                predicted_letter = ' '
                prediction_letter_label.config(text=predicted_letter)
                start_time = None
                if current_word:
                    if current_sentence:
                        current_sentence += " " + current_word
                    else:
                        current_sentence += current_word
                    prediction_sentence_label.config(text=current_sentence)
                    current_word = ""
                    prediction_word_label.config(text=current_word)
        else:
            start_time = time.time()
    else:
        if start_time is not None:
            start_time = None

    if predicted_letter == 'blank':
        if start_time is not None:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 5:
                if current_word:
                    if current_sentence:
                        current_sentence += " " + current_word
                    else:
                        current_sentence += current_word
                    prediction_sentence_label.config(text=current_sentence)
                    current_word = ""
                    prediction_word_label.config(text=current_word)
                    prediction_letter_label.config(text="")
                    start_time = None
        else:
            start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.quit()

    root.after(10, update_frame)

update_frame()

def update_suggestion(current_word):
    suggestions = get_suggestions(current_word)
    if suggestions:
        for widget in content_frame.winfo_children():
            if isinstance(widget, ttk.Button) and widget.winfo_name() == 'suggestion_button':
                widget.destroy()

        for i in range(min(len(suggestions), 3)):
            suggestion_btn = ttk.Button(content_frame, text=suggestions[i], command=lambda s=suggestions[i]: suggestion_click(s), name='suggestion_button')
            suggestion_btn.pack(side="left", padx=5, pady=5)
    else:
        suggestion_label.config(text="No suggestions available")
        root.after(3000, lambda: suggestion_label.config(text=""))


def on_project_description_click():
    project_description_window = tk.Toplevel(root)
    project_description_window.title("Project Description")
    project_description_window.configure(bg="#0B0B45")

    window_width = 600
    window_height = 400
    screen_width = project_description_window.winfo_screenwidth()
    screen_height = project_description_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    project_description_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    project_description_label = tk.Label(project_description_window, text="Project Description", font=("Helvetica", 20), bg="#0B0B45", fg="#00c04b")
    project_description_label.pack(pady=(20, 10))

    project_info = """
    This project is a Sign Language to Text converter that uses a convolutional neural network (CNN)
    to recognize hand signs and translate them into text. The model is trained on a dataset of
    images of hand signs corresponding to letters of the alphabet and some common words.

    Tech Stack:
    - Python
    - OpenCV
    - Keras
    - Tkinter
    - pyttsx3

    Team Members:
    - Mohammad Saify Sheikh (Team Leader)
    - Himanshu Shrigiriwar
    - Soham Bedi
    - Rugved Mhatre

    GitHub Repository: https://github.com/SaifySheikh/Sign_Recognition_Project
    """

    def open_github(event):
        webbrowser.open_new_tab("https://github.com/SaifySheikh/Sign_Recognition_Project")

    project_info_label = tk.Label(project_description_window, text=project_info, font=("Helvetica", 14), bg="#0B0B45", fg="white", justify="left")
    project_info_label.pack(expand=True, padx=20, pady=10)

    project_info_label.bind("<Button-1>", open_github)

project_description_button = ttk.Button(root, text="Project Description", command=on_project_description_click)
project_description_button.pack(side="top", anchor="ne", padx=10, pady=10)

root.mainloop()

cap.release()
cv2.destroyAllWindows()
