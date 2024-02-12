from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

# Charger le dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# Diviser le dataset en données d'entraînement et données de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialiser le modèle Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Entraîner le modèle sur les données d'entraînement
clf.fit(X_train, y_train)

# Prédire les étiquettes pour les données de test
y_pred = clf.predict(X_test)

# Calculer l'exactitude
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy for RandomFOrest test : ", accuracy)


# Now SVM 

# Initialiser le modèle SVM
clf = SVC(random_state=42)

# Entraîner le modèle sur les données d'entraînement
clf.fit(X_train, y_train)

# Prédire les étiquettes pour les données de test
y_pred = clf.predict(X_test)

# Calculer l'exactitude
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy for SVM : ",accuracy)

# jack change