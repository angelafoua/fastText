import csv
import re

def extract_words_from_csv(file_path):
    words_set = set()
    
    # Regex to match words (letters only)
    word_pattern = re.compile(r"[a-zA-Z]+")

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            # Skip if row is empty or has only one column
            if len(row) < 2:
                continue
            
            # Process columns starting from the second one
            for cell in row[1:]:
                # Find all words in the cell
                words = word_pattern.findall(cell)
                
                # Add lowercase version to ensure uniqueness
                for word in words:
                    words_set.add(word.lower())

    return words_set
