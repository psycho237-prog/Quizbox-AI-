import cv2
import pytesseract
import subprocess
import re

# IP camera URL
url = "http://10.52.46.36:8080/video" #address ip de ma camera ip

# Function to check if text is a question
def is_question(text):
    text = text.strip().lower()
    return (text.endswith('?') or 
            text.startswith(('what', 'how', 'why', 'when', 'where', 'who', 'quel', 'quelle', 'quand', 'comment', 'pourquoi', 'qui')))

# Function to check if text is an MCQ
def is_mcq(text):
    mcq_pattern = r"[A-Z]\)"
    return bool(re.search(mcq_pattern, text))

# Function to run TinyLlama and get response
def run_tinyllama(prompt):
    command = f"ollama run tinyllama '{prompt}'"
    response = subprocess.check_output(command, shell=True)
    return response.decode("utf-8").strip()

# Create a VideoCapture object
cap = cv2.VideoCapture(url)

cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Frame', 640, 480)

frame_skip = 5
# Dictionary to keep track of current questions
current_questions = {}

frame_count = 0
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    
    if not ret:
        break
    
    frame_count += 1
    if frame_count % 5 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (320, 240))
        text = pytesseract.image_to_string(gray)
        
        # Check if detected text is a question or MCQ
        if is_question(text) or is_mcq(text):
            question = text.strip().lower()
            if question not in current_questions:
                current_questions[question] = True
                # Run TinyLlama and get response
                response = run_tinyllama(text.strip())
                print(f"Question: {text.strip()}")
                print(f"Answer: {response}")
        else:
            current_questions = {}
    
    # Display the frame
    cv2.imshow('Frame', frame)
    
    # Exit on key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
