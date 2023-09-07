from flask import Flask, render_template, request, url_for, flash, redirect, jsonify

import pickle
from datetime import datetime
import pandas as pd
from sklearn import datasets
from sqlalchemy import create_engine


app = Flask(__name__)
iris = datasets.load_iris()
engine = create_engine('postgres://fl0user:HlUWf7VTpyx1@ep-empty-king-96691665.eu-central-1.aws.neon.tech:5432/iris?sslmode=require')

@app.route('/hola', methods= ["GET"])
def saluda():
    
    return render_template("plantilla.html")     

@app.route("/v0/predictor", methods=["GET", "POST"])
def predictor_v0():
    if request.method == "POST":
        with open("iris_model.pkl", "rb") as file:
            model = pickle.load(file)

        s_length = float(request.form.get("s_length", None))
        s_width = float(request.form.get("s_width", None))
        p_length = float(request.form.get("p_length", None))
        p_width = float(request.form.get("p_width", None))
        time = datetime.now()
        formatted_dt = time.strftime('%Y-%m-%d %H:%M')

        if s_length is None or s_width is None or p_width is None or p_length is None:
            print("<Faltan datos, asegurate de que está todo")
        else:
            prediction = model.predict([[s_length,s_width,p_length,p_width]])
            class_name = iris.target_names[prediction]
            prediction = str(class_name[0])
            upload = {"p_length": p_length, "p_width": p_width, "s_length": s_length, "s_width": s_width, "prediction":prediction, "timestamp":formatted_dt}

            upload = pd.DataFrame([upload])
            upload.to_sql('predictions', con=engine, if_exists='append', index=False)

            return jsonify({"prediction": prediction})



if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)