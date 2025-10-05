from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ---------------------------
# 1. Загрузка данных и обучение модели
# ---------------------------
data_file = "cumulative_2025.10.03_22.30.54.csv"

df = pd.read_csv(data_file)

y = df["koi_disposition"]

# Ключевые признаки
key_features = [
    "koi_prad",     
    "koi_srad", 
    "koi_depth",
    "koi_duration",
    "koi_teq",

    "koi_insol",
    "koi_period",
    "koi_duration_err2"
]

X = df[key_features].fillna(df[key_features].median())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.3f}")

# Сохраняем модель
model_file = "forest_model_data1_v3.pkl"
joblib.dump(model, model_file)
print(f"Модель сохранена в {model_file}")

# ---------------------------
# 2. Flask-приложение для веб-теста модели
# ---------------------------
app = Flask(__name__)

# Загружаем только что обученную модель
model = joblib.load(model_file)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Классификация планеты</title>
    <style>
        body { font-family: Arial; text-align:center; margin:50px;}
        input { margin:5px 0; padding:5px; width:200px; }
        button { padding:5px 15px; margin-top:10px; }
        #result { margin-top:20px; font-weight:bold; font-size:1.2em; color:green; }
    </style>
</head>
<body background="1.jpg">
<h2>Классификация планеты</h2>
<form id="planetForm">
    {% for feat in key_features %}
    <div>
        <label>{{ feat }}: <input type="number" step="any" name="{{ feat }}" required></label>
    </div>
    {% endfor %}
    <button type="submit">Предсказать класс планеты</button>
</form>
<div id="result"></div>

<script>
document.getElementById("planetForm").addEventListener("submit", async function(e){
    e.preventDefault();
    const formData = new FormData(this);
    const user_input = {};
    formData.forEach((value, key) => { user_input[key] = parseFloat(value); });
    const response = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(user_input)
    });
    const result = await response.json();
    if(result.predicted_class){
        document.getElementById("result").innerText = "Класс планеты: " + result.predicted_class;
    } else {
        document.getElementById("result").innerText = "Ошибка: " + result.error;
    }
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE, key_features=key_features)

@app.route("/predict", methods=["POST"])
def predict_planet():
    try:
        user_input = request.json
        X_new = pd.DataFrame([user_input], columns=key_features)
        prediction = model.predict(X_new)[0]
        return jsonify({"predicted_class": prediction})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
