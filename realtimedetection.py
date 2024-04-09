from keras.models import model_from_json
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
import time

# Load the model
json_file = open("signlanguagedetectionmodel48x48.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("signlanguagedetectionmodel48x48.h5")

# Define the label names
label=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y','blank']

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

def on_developers_click():
    print("Developers button clicked!")

def on_audio_click():
    print("Audio button clicked!")

# Open video capture
cap = cv2.VideoCapture(0)

# Initialize Tkinter
root = tk.Tk()
root.title("Sign Language to Text")

# Set window size and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a style
style = ttk.Style()
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 18))
style.configure("TButton", background="#007bff", foreground="black", font=("Poppins", 12))
style.map("TButton", background=[("active", "#0056b3")])

# Create a frame for the content
content_frame = ttk.Frame(root, style="TFrame")
content_frame.pack(expand=True, fill='both', padx=20, pady=20)

# Add heading
heading_label = ttk.Label(content_frame, text="Sign Language to Text", font=("Helvetica", 24))
heading_label.pack(pady=(0, 20))

# Add row for displaying letter
letter_label = ttk.Label(content_frame, text="Letter:")
letter_label.pack(anchor='w', padx=5, pady=5)
prediction_letter_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_letter_label.pack(anchor='w', padx=5, pady=5)

# Add row for displaying word
word_label = ttk.Label(content_frame, text="Word:")
word_label.pack(anchor='w', padx=5, pady=5)
prediction_word_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_word_label.pack(anchor='w', padx=5, pady=5)

# Add row for displaying sentence
sentence_label = ttk.Label(content_frame, text="Sentence:")
sentence_label.pack(anchor='w', padx=5, pady=5)
prediction_sentence_label = ttk.Label(content_frame, text="", font=("Helvetica", 18))
prediction_sentence_label.pack(anchor='w', padx=5, pady=5)

# Add "Audio" button
audio_button = ttk.Button(content_frame, text="Audio", command=on_audio_click)
audio_button.pack(expand=True, fill='both', padx=5, pady=5)

# Add "Developers" button
developers_button = ttk.Button(content_frame, text="Developers", command=on_developers_click)
developers_button.pack(expand=True, fill='both', padx=5, pady=5)

# Initialize start time, predicted_letter, current_word, and current_sentence
start_time = None
predicted_letter = ""
current_word = ""
current_sentence = ""

def update_frame():
    global start_time, predicted_letter, current_word, current_sentence
    
    _, frame = cap.read()
    cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 1)
    
    # Crop the frame
    cropframe = frame[40:300, 0:300]
    cropframe = cv2.cvtColor(cropframe, cv2.COLOR_BGR2GRAY)
    cropframe = cv2.resize(cropframe, (48, 48))
    cropframe = extract_features(cropframe)
    
    # Make predictions
    pred = model.predict(cropframe)
    max_accu = np.max(pred) * 100
    pred_label = label[pred.argmax()]
    
    # Draw prediction on frame
    cv2.rectangle(frame, (0, 0), (300, 40), (0, 165, 255), -1)
    if pred_label != 'blank':
        accu = "{:.2f}".format(max_accu)
        cv2.putText(frame, f'{pred_label}  {accu}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        accu = "{:.2f}".format(max_accu)
        cv2.putText(frame, f'{pred_label}  {accu}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Show frame
    cv2.imshow("Sign Language to Text", frame)
    
    # Update letter prediction label if accuracy > 85% for 5 seconds
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

    # Update sentence if the current word is blank for more than 5 seconds
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

    # Check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        root.quit()

    # Update frame
    root.after(10, update_frame)

# Start updating frame
update_frame()

root.mainloop()

# Release the capture
cap.release()
cv2.destroyAllWindows()
