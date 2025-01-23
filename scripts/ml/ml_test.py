import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pandas as pd


X, y = load_iris(return_X_y=True)

model = LogisticRegression(max_iter=200)
model.fit(X, y)

mlflow.set_tracking_uri("http://127.0.0.1:5001")

with mlflow.start_run():
    print("Begin logging")
    mlflow.log_param("model_type", "logistic_regression")
    mlflow.log_metric("test_accuracy", 0.95)
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="iris_model",
        registered_model_name="tiny_iris_classifier"
    )
    print("End logging")

model = mlflow.pyfunc.load_model("models:/tiny_iris_classifier/latest")

sample_data = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],
  columns=["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"])

prediction = model.predict(sample_data)
print(prediction)

