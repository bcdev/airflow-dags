import time

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pandas as pd


def run():

  X, y = load_iris(return_X_y=True)

  model = LogisticRegression(max_iter=200)
  print("Fitting Model!!")
  model.fit(X, y)
  print("Model Fit!!")

  sample_data = pd.DataFrame([[5.1, 3.5, 1.4, 0.2]],
    columns=["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"])

  prediction = model.predict(sample_data)
  print(f"Prediciton for sample_data {sample_data}: ", prediction)
  print("waiting for a few seconds")
  time.sleep(10)
  print("bye")


if __name__ == "__main__":
  run()