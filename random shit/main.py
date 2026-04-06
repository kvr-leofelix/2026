import easyocr
import pandas as pd
import re
import cv2
import numpy as np
from datetime import datetime

# Initialize reader
reader = easyocr.Reader(['en'])

def update_attendance(image_path, csv_path):
    # 1. LOAD AND ERASE NOTEBOOK LINES
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to get black and white
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Identify horizontal lines (notebook lines)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Subtract the lines from the original thresholded image
    clean_img = cv2.subtract(thresh, remove_horizontal)
    
    # Dilate slightly to make your pen strokes solid again
    kernel = np.ones((2,2), np.uint8)
    final_img = cv2.dilate(clean_img, kernel, iterations=1)
    final_img = cv2.bitwise_not(final_img) # Flip back to black text on white

    print("Processing handwritten sheet...")
    results = reader.readtext(final_img)
    
    found_roll_nos = []
    # Pattern: Look for any 5-6 digit sequence that might start with B or 8
    # We use a very broad search and then 'fix' the results
    for (bbox, text, prob) in results:
        # Clean the string: remove spaces and non-alphanumeric junk
        s = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # If it looks like a roll number (e.g., 825210 or B25211)
        if len(s) >= 5:
            # Fix common OCR errors for 'B'
            if s.startswith('8') or s.startswith('13') or s.startswith('6'):
                s = 'B' + s[1:] if s.startswith('8') or s.startswith('6') else 'B' + s[2:]
            
            # Final check: Does it match B + 5 digits?
            match = re.search(r'B\d{5}', s)
            if match:
                roll = match.group()
                found_roll_nos.append(roll)
                print(f"✅ Found Roll: {roll} ({int(prob*100)}% sure)")

    # 2. UPDATE CSV
    try:
        df = pd.read_csv(csv_path)
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in df.columns:
            df[today] = 'Absent'
        
        for roll in set(found_roll_nos):
            if roll in df['RollNo'].values:
                df.loc[df['RollNo'] == roll, today] = 'Present'
        
        df.to_csv(csv_path, index=False)
        print(f"\nAttendance marked for: {set(found_roll_nos)}")
    except Exception as e:
        print(f"Error: {e}")

# Run it
update_attendance('1.jpeg', 'file.csv')