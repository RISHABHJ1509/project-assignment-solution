'''4. Develop a recommendation system using Flask that suggests content to users based on their preferences.'''

from flask import Flask, render_template, request

app = Flask(__name__)

# This dictionary will act as your content database
content_data = {
    'content1': {'genre': 'Action', 'tags': ['exciting', 'adventure']},
    'content2': {'genre': 'Drama', 'tags': ['emotional', 'real-life']},
    'content3': {'genre': 'Comedy', 'tags': ['funny', 'light-hearted']},
    # Add more content data here
}


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    user_preferences = request.form.getlist('preferences')

    # Perform recommendation logic
    recommended_content = recommend_content(user_preferences)

    return render_template('recommendations.html', recommendations=recommended_content)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_content(user_preferences):
    # Convert user preferences to a string
    user_prefs_str = ' '.join(user_preferences)

    # Prepare content features (using genre and tags as features)
    content_features = []
    content_names = []
    for content_name, data in content_data.items():
        content_names.append(content_name)
        content_features.append(' '.join([data['genre']] + data['tags']))

    # Vectorize content features
    vectorizer = TfidfVectorizer()
    content_matrix = vectorizer.fit_transform(content_features)

    # Vectorize user preferences
    user_prefs_vectorized = vectorizer.transform([user_prefs_str])

    # Calculate cosine similarity between user preferences and content
    similarities = cosine_similarity(user_prefs_vectorized, content_matrix).flatten()

    # Get indices of top recommendations
    top_indices = similarities.argsort()[::-1][:5]  # Get top 5 recommendations

    # Return recommended content names
    recommended_content = [content_names[idx] for idx in top_indices]
    return recommended_content

if __name__ == "__main__":
    app.run(debug=True)