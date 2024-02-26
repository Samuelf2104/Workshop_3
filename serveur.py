from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

# Charger le dataset Iris
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialiser les modèles
models = {
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train),
    'svm': SVC(random_state=42).fit(X_train, y_train),
    'logistic_regression': LogisticRegression(random_state=42).fit(X_train, y_train)
}

@app.route('/predict', methods=['POST'])
def predict():

	print("ok")

	data = request.get_json(force=True)

	print(data)
	model_name = data['model']
	input_features = data['input']
	print("input : ", input_features)
	print("model : ", model_name)

	model = models.get(model_name)

	if model:
		# Faire la prédiction
		prediction = model.predict([input_features])
		species = iris.target_names[prediction][0]
		return jsonify({'prediction': species})
	else:
		return jsonify({'error': 'Model not found.'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
