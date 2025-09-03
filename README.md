# 📚Book Recommendation System

A clean, easy-to-understand book recommendation system perfect for explaining in interviews and presentations.

# Live URL : https://book-recommendation-system-hef5hdb3fyccccds.southindia-01.azurewebsites.net/
## 🎯 What It Does

This system recommends books based on similarity using:
- **Content-Based Filtering**: Finds books similar to ones you like
- **TF-IDF Vectorization**: Converts book information to numbers
- **Cosine Similarity**: Measures how similar books are
- **Fuzzy Matching**: Handles typos in book titles

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Book Recommendation System
```bash
# Command line version
python books.py

# For WebServer
python app.py
# Then open: http://localhost:5000
```

## 🔍 How It Works (Easy to Explain!)

### Step 1: Data Loading
- Loads book data from CSV file
- Cleans and prepares the data
- Keeps essential info: title, author, rating, language

### Step 2: Feature Creation
- Combines book title, author, and language into text
- Uses TF-IDF to convert text to numerical vectors
- Creates similarity matrix between all books

### Step 3: Making Recommendations
- Find the input book in database
- Calculate similarity with all other books
- Return most similar books as recommendations

## 📊 Example Usage

```python
from books import BookRecommendationSystem

# Initialize system
recommender = BookRecommendationSystem('books.csv')

# Get recommendations
recommendations = recommender.get_recommendations('Harry Potter', 5)

# Show statistics
recommender.show_stats()
```

## 🎨 Features

### ✅ Simple & Explainable
- Clean, readable code
- Easy to understand algorithms
- Well-documented functions

### ✅ Robust
- Handles typos with fuzzy matching
- Error handling for missing books
- Data validation and cleaning

### ✅ Visual
- Data distribution charts
- Author popularity graphs
- Rating vs pages analysis

### ✅ Interactive
- Command line interface
- Web interface with Flask
- Real-time recommendations

## 📁 Project Structure

```
book-recommendation-system/
├── books.py          # Main recommendation system
├── app.py            # Web application
├── requirements.txt  # Dependencies
├── books.csv         # book dataset
└── templates/
    └── index.html   # html - frontend
```

## 📈 Algorithm Explanation

### TF-IDF (Term Frequency-Inverse Document Frequency)
- **Term Frequency**: How often a word appears in a book's description
- **Inverse Document Frequency**: How rare/common a word is across all books
- **Result**: Important words get higher scores

### Cosine Similarity
- Measures angle between two vectors
- Range: 0 (completely different) to 1 (identical)
- Works well for text similarity

### Content-Based Filtering
- Recommends items similar to what user likes
- Based on item features (title, author, genre)
- No need for other users' data

## 📚 Sample Output

```
🎯 Top 2 recommendations for 'Harry Potter':

1. 📖 The Lord of the Rings
   👤 Author: J.R.R. Tolkien
   ⭐ Rating: 4.5
   🔗 Similarity: 0.85

2. 📖 The Chronicles of Narnia
   👤 Author: C.S. Lewis
   ⭐ Rating: 4.3
   🔗 Similarity: 0.78
```
