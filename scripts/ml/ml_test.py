import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)

model = LogisticRegression(max_iter=20)
model.fit(X[:5], y[:5])

mlflow.set_tracking_uri("http://mlflow.default.svc.cluster.local:5000")

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

