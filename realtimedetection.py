from keras.models import model_from_json
import cv2
import numpy as np
import tkinter as tk
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

# Add heading
heading_label = tk.Label(root, text="Sign Language to Text", font=("Helvetica", 24))
heading_label.grid(row=0, column=0, columnspan=2, pady=10)

# Add row for displaying letter
letter_label = tk.Label(root, text="Letter:", font=("Helvetica", 18))
letter_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
prediction_letter_label = tk.Label(root, text="", font=("Helvetica", 18))
prediction_letter_label.grid(row=1, column=1, sticky='w', padx=5, pady=5)

# Add row for displaying word
word_label = tk.Label(root, text="Word:", font=("Helvetica", 18))
word_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
prediction_word_label = tk.Label(root, text="", font=("Helvetica", 18))
prediction_word_label.grid(row=2, column=1, sticky='w', padx=5, pady=5)

# Add row for displaying sentence
sentence_label = tk.Label(root, text="Sentence:", font=("Helvetica", 18))
sentence_label.grid(row=3, column=0, sticky='e', padx=5, pady=5)
prediction_sentence_label = tk.Label(root, text="", font=("Helvetica", 18))
prediction_sentence_label.grid(row=3, column=1, sticky='w', padx=5, pady=5)

# Add "Audio" button
audio_button = tk.Button(root, text="Audio", command=on_audio_click, font=("Helvetica", 12))
audio_button.grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=5)

# Add "Developers" button
developers_button = tk.Button(root, text="Developers", command=on_developers_click, font=("Helvetica", 12))
developers_button.grid(row=5, column=0, columnspan=2, sticky='we', padx=5, pady=5)

# Initialize start time
start_time = None
predicted_letters = []

def update_frame():
    global start_time, predicted_letters
    
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
    if pred_label == 'blank':
        cv2.putText(frame, " ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
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
                predicted_letters.append(pred_label)
                prediction_letter_label.config(text=' '.join(predicted_letters))
                start_time = None
        else:
            start_time = time.time()
    else:
        if start_time is not None:
            start_time = None
        
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