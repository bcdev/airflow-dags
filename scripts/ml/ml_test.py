import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

with mlflow.start_run():
    print("Begin logging")
    mlflow.log_param("model_type", "logistic_regression")
    mlflow.log_metric("test_accuracy", 0.95)
    print("End logging")
