
from sklearn.feature_extraction.text import CountVectorizer
# Sample documents
documents = [
"I love programming in Python",
"Python is great for data science",
"I love learning new programming languages"
]
# Create the Bag of Words model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
# Get feature names and transformed data
feature_names = vectorizer.get_feature_names_out()
print("Feature Names:", feature_names)
print("Bag of Words Model:\n", X.toarray())