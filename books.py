import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz, process
import warnings
warnings.filterwarnings('ignore')

class BookRecommendationSystem:
    # Loading Datasets 
    def __init__(self, csv_path='books.csv'):
        print("Loading data...")
        self.books_df = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        
        self.load_data(csv_path)
        self.prepare_features()
        print("Data loaded successfully")
        
    def load_data(self, csv_path):
        print("Loading book data...")
        
        try:
            self.books_df = pd.read_csv(csv_path, encoding='utf-8')
            self.books_df = self.books_df.dropna(axis=1, how='all')
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return
        
        columns_to_keep = ['title', 'authors', 'average_rating', 'language_code', 'num_pages', 'ratings_count']
        available_columns = [col for col in columns_to_keep if col in self.books_df.columns]
        self.books_df = self.books_df[available_columns]
        
        self.books_df.dropna(subset=['title', 'authors'], inplace=True)
        
        self.books_df['average_rating'] = pd.to_numeric(self.books_df['average_rating'], errors='coerce')
        self.books_df = self.books_df.dropna(subset=['average_rating'])
        
        self.books_df['language_code'].fillna('eng', inplace=True)
        self.books_df['num_pages'] = pd.to_numeric(self.books_df['num_pages'], errors='coerce')
        self.books_df['num_pages'].fillna(300, inplace=True)
        
        self.books_df.reset_index(drop=True, inplace=True)
        
        print(f"Loaded {len(self.books_df)} books successfully!")
        # Handling missing values and resetting index
    def prepare_features(self):
        print("Creating book features...")
        
        self.books_df['combined_features'] = (
            self.books_df['title'].fillna('') + ' ' + 
            self.books_df['authors'].fillna('') + ' ' + 
            self.books_df['language_code'].fillna('')
        )
        
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.books_df['combined_features'])
        
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        print("Features created!")
        
    # Fuzzy matching for book titles - which helps to find similar titles even user enter wrong title
    def find_book_fuzzy(self, book_title, threshold=70):
        titles = self.books_df['title'].tolist()
        match = process.extractOne(book_title, titles, scorer=fuzz.ratio)
        
        if match and match[1] >= threshold:
            return match[0], match[1]
        return None, 0
    # Get recommendations is processed based on book title
    def get_recommendations(self, book_title, num_recommendations=5):
        try:
            book_indices = self.books_df.index[self.books_df['title'] == book_title].tolist()
            
            if not book_indices:
                fuzzy_title, confidence = self.find_book_fuzzy(book_title)
                if fuzzy_title:
                    print(f"Did you mean '{fuzzy_title}'? (Match: {confidence}%)")
                    book_indices = self.books_df.index[self.books_df['title'] == fuzzy_title].tolist()
                    book_title = fuzzy_title
                else:
                    return f"Sorry, couldn't find '{book_title}' in our database."
            
            book_index = book_indices[0]
            
            similarity_scores = list(enumerate(self.cosine_sim[book_index]))
            
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]
            
            recommendations = []
            print(f"\nTop {num_recommendations} recommendations for '{book_title}':\n")
            
            for i, (book_idx, score) in enumerate(similarity_scores, 1):
                book_info = self.books_df.iloc[book_idx]
                recommendations.append({
                    'rank': i,
                    'title': book_info['title'],
                    'author': book_info['authors'],
                    'rating': book_info['average_rating'],
                    'similarity': score
                })
                
                print(f"{i}. {book_info['title']}")
                print(f"   Author: {book_info['authors']}")
                print(f"   Rating: {book_info['average_rating']:.1f}")
                print(f"   Similarity: {score:.2f}")
                print()
            
            return recommendations
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    # Get system statistics about database
    def get_system_stats(self):
        stats = {
            'Total Books': len(self.books_df),
            'Unique Authors': self.books_df['authors'].nunique(),
            'Average Rating': round(self.books_df['average_rating'].mean(), 2),
            'Languages': self.books_df['language_code'].nunique(),
            'Average Pages': round(self.books_df['num_pages'].mean(), 0)
        }
        return stats
    # return statistics about database
    def show_stats(self):
        stats = self.get_system_stats()
        print("\nDatabase Statistics:")
        print("=" * 30)
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("=" * 30)
    
    def test_system(self):
        print("\nTesting System with Popular Books:")
        print("=" * 40)
        
        popular_books = self.books_df.nlargest(3, 'ratings_count')['title'].tolist()
        
        for book in popular_books:
            print(f"\nTesting with: {book}")
            recs = self.get_recommendations(book, 3)
            if isinstance(recs, str):
                print(recs)
            print("-" * 40)
# Main function to run with CLI interface
def main():
    print("Welcome to the Book Recommendation System!")
    print("=" * 50)
    
    try:
        recommender = BookRecommendationSystem()
        
        recommender.show_stats()
        # user need to enter 1-5 to choose the option
        while True:
            print("\nWhat would you like to do?")
            print("1. Get book recommendations")
            print("2. View database statistics")
            print("3. Test system")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            # Switch case for user's choice
            if choice == '1':
                book_title = input("\nEnter a book title: ").strip()
                if book_title:
                    try:
                        num_recs = int(input("How many recommendations? (default 5): ") or "5")
                        recommender.get_recommendations(book_title, num_recs)
                    except ValueError:
                        recommender.get_recommendations(book_title, 5)
                else:
                    print("Please enter a book title!")
                    
            elif choice == '2':
                recommender.show_stats()
                
            elif choice == '3':
                recommender.test_system()
                
            elif choice == '4':
                print("Thank you for using the Recommendation System!")
                break
                
            else:
                print("Invalid choice. Please try again.")
                
    except FileNotFoundError:
        print("Error: books.csv file not found!")
        print("Please make sure the books.csv file is in the same directory.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
