# Campus AI Student Assistant 🎓

An offline Python NLP Chatbot built with **Flask**, **Scikit-Learn (TF-IDF + Logistic Regression)**, and modern HTML/CSS/JavaScript.

## Project Structure
```text
aman/
├── app.py              # Main Flask backend with NLP classifier
├── intents.json        # Intent dataset (patterns & responses)
├── templates/
│   └── index.html      # Frontend chat interface
├── requirements.txt    # Project dependencies
├── test_bot.py         # Unit test suite
└── README.md           # Documentation
```

## Setup Instructions

### 1. Install Dependencies
Make sure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app.py
```
Then open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### 3. Run Tests
To verify all NLP intents and endpoints work properly:
```bash
python test_bot.py
```
