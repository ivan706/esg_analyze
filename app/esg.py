import os
import pandas as pd
from flask import Flask, render_template, jsonify, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/esg_data")
def me_api():
    data = get_esg_data()
    return data

def get_esg_data():
    return {
        "bse": obtain_esg_data("beijiaosuo"),
        "scse": obtain_esg_data("shenzheng"),
        "sse": obtain_esg_data("shangzheng"),
    }

def obtain_esg_data(filename):
    esg_folder = 'esgs'
    file_path = os.path.join(esg_folder, f"{filename}.csv")

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # 读取CSV文件
    df = pd.read_csv(file_path, skiprows=0, dtype={0: str})
    df.fillna("", inplace=True)
    # 将数据转换为字典格式
    # data = df.to_dict(orient='records')

    return df.values.tolist()