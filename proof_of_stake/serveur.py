from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import concurrent.futures
import requests
import threading
import time
import json
from collections import Counter


app = Flask(__name__)
CORS(app)

# Charger le dataset Iris
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialiser les modèles
models = {
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train),
    'SVC': SVC(random_state=42).fit(X_train, y_train),
    'linear' : LinearRegression().fit(X_train, y_train)
}

# Charger les informations des nœuds à partir de participants.json
with open('participants.json') as f:
    nodes_info = json.load(f)


def send_request(node_ip, input_features, timeout=1):
    url = f"http://{node_ip}:5000/predict"
    data = {"input": input_features}
    try:
        # Utiliser le paramètre timeout pour limiter le temps d'attente de la réponse
        response = requests.post(url, json=data, timeout=timeout)
        # Retourner la réponse en JSON si la requête est réussie
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Response from {node_ip} with status code {response.status_code}")
            return None
    except requests.RequestException as e:
        # Gérer les exceptions, telles que des dépassements de délai, et retourner None
        print(f"Error: Request to {node_ip} failed with exception: {e}")
        return None

def collect_predictions():
	while True:

		print("\n\nfaire une prediction : \n\n")

		print("sepalLength : ")
		sepalLength = input()

		print("sepalWidth : ")
		sepalWidth = input() 

		print("petalLength : ")
		petalLength = input() 

		print("petalWidth : ")
		petalWidth = input() 

		input_features = [sepalLength, sepalWidth, petalLength, petalWidth]

		responses = []
		list_ip = []

		print(nodes_info)

		for node in nodes_info:
			response = send_request(node, input_features)
			if response:
				predic = response["prediction"]
				responses.append(predic)
				list_ip.append(node)

				print(f"Received response from {node}: {predic}")


		# Utiliser Counter pour compter les occurrences de chaque réponse
		response_counts = Counter(responses)

		# Trouver la réponse la plus fréquente
		most_common_response = response_counts.most_common(1)[0][0]

		print("\nreponse la plus représentée : ", most_common_response)

		for k in range(len(responses)) :

			if most_common_response == responses[k] and nodes_info[list_ip[k]]["weight"] < 1 :
				nodes_info[list_ip[k]]["weight"] = nodes_info[list_ip[k]]["weight"] + 0.1
				nodes_info[list_ip[k]]["deposit"] = nodes_info[list_ip[k]]["deposit"] + 100

			elif most_common_response == responses[k] and nodes_info[list_ip[k]]["weight"] == 1 :
				nodes_info[list_ip[k]]["deposit"] = nodes_info[list_ip[k]]["deposit"] + 100

			elif most_common_response != responses[k] and nodes_info[list_ip[k]]["weight"] == 0 :
				nodes_info[list_ip[k]]["deposit"] = nodes_info[list_ip[k]]["deposit"] - 100

			elif most_common_response != responses[k] and nodes_info[list_ip[k]]["weight"] > 0 :
				nodes_info[list_ip[k]]["weight"] = nodes_info[list_ip[k]]["weight"] - 0.1
				nodes_info[list_ip[k]]["deposit"] = nodes_info[list_ip[k]]["deposit"] - 100

		with open('participants.json', 'w') as file:
			json.dump(nodes_info, file, indent=4)




@app.route('/predict', methods=['POST'])
def predict():

	data = request.get_json(force=True)

	input_features = data['input']
	print("(serveur) input : ", input_features)

	model = models.get("random_forest")

	prediction = model.predict([input_features])
	species = iris.target_names[prediction][0]
	return jsonify({'prediction': species})


def run_flask_app():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)  # Désactiver le reloader

if __name__ == '__main__':

    threading.Thread(target=run_flask_app, daemon=True).start()

    time.sleep(1)

    threading.Thread(target=collect_predictions, daemon=True).start()
    
    # Gardez le thread principal en vie
    while True:
        time.sleep(1)