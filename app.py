from flask import Flask, render_template, request, jsonify
from books import BookRecommendationSystem

app = Flask(__name__)


print("Starting Book Recommendation System Server...")
recommender = BookRecommendationSystem()
# root route where d
@app.route('/')
def home():
    """Main page."""
    return render_template('index.html')
# API endpoint for getting book recommendations  - sends user's book title and number of recommendations through POST request
@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """API endpoint for recommendations."""
    try:
        data = request.get_json()
        book_title = data.get('book_title', '')
        num_recommendations = data.get('num_recommendations', 5)
        # if book title not there means return 400 status code to notify user to enter book title
        if not book_title:
            return jsonify({'error': 'Book title is required'}), 400
        # calls the get_recommendations method 
        recommendations = recommender.get_recommendations(book_title, num_recommendations)
        
        if isinstance(recommendations, str):  # Error message
            return jsonify({'error': recommendations}), 404
        
        return jsonify({
            'recommendations': recommendations,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get Database Info to /api/stats endpoint."""
    try:
        stats = recommender.get_system_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting web server...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run()
