import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import cv2
from ultralytics import YOLO


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

__model = None

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens

def load_model(model_path):
    global __model
    # Load the YOLOv8 model from the specified path
    __model = YOLO(model_path)
    # return model  # Return the loaded YOLO model

def detect_damage(image_path, model):

    try:
        # Load the image
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found or unable to load: {image_path}")

        # Perform inference using the YOLO model
        results = model.predict(img)

        # Extract detected labels (modify based on your model's output structure)
        # Access the 'names' attribute of the model to get class labels
        labels = [model.names[int(result.boxes.cls[i])] for result in results for i in range(len(result.boxes.cls))] if results else None
        return labels

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Indicate error
    
def match_labels_nlp(detected_labels, user_description):
    if detected_labels is None:
        return "Error: Label extraction failed."
    elif not detected_labels:
        return "No damage detected."
    else:
        # Preprocess user description and labels
        user_description_tokens = preprocess_text(user_description)
        label_tokens = [preprocess_text(label) for label in detected_labels]

        # Calculate exact match score (already implemented)
        exact_match_score = 1 if user_description.lower() in [label.lower() for label in detected_labels] else 0

        # Calculate word overlap score
        word_overlap_score = sum(len(set(user_description_tokens).intersection(label_tokens)) for label_tokens in label_tokens)

        # Combine scores and determine confidence level (adjust weights based on your needs)
        confidence = 0.7 * exact_match_score + 0.3 * word_overlap_score 

        if confidence >= 0.5:
            return "Match: Detected damage aligns with your description."
        elif confidence >= 0.3:
            return "Suspicious: Detected damage might not perfectly match your description, but there's some similarity."
        else:
            return "Uncertain: Detected labels (%s) don't seem to match your description (%s)." % (", ".join(detected_labels), user_description)


def output(image_path, user_description):
    detected_labels = detect_damage(image_path)
    match_message = match_labels_nlp(detected_labels, user_description)
    return match_message