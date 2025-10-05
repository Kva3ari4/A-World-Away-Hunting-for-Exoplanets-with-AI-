# Exoplanet Classification — Local Guide

## 📌 Overview
This project classifies exoplanets based on astronomical data.  
It uses a **Random Forest classifier** trained on tabular features, and provides a **Flask web application** for interactive predictions.  
Everything runs **locally** on your machine.

---

## 📂 Project Structure
- **Final.py** — main script: loads data, trains model (if missing), saves model, and runs Flask app  
- **cumulative_2025.10.03_22.30.54.csv** — dataset with exoplanet parameters (required for training)  
- **forest_model_data1_v3.pkl** — saved trained model (created automatically on first run if not present)  
- *(optional)* `requirements.txt` — dependency list for quick installation  

---

## 🛠 Requirements
- **Python 3.9 or newer** (3.9–3.11 recommended)  
- `pip` or `conda` package manager  

### Check versions
```bash
python --version
pip --version
```
(Use `python3` instead of `python` on Linux/macOS if needed.)

---

## ⚙️ Virtual Environment Setup (recommended)
Creating a virtual environment isolates dependencies.

### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### Windows (cmd)
```cmd
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
```

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Conda
```bash
conda create -n exo_env python=3.10
conda activate exo_env
```

---

## 📦 Installing Dependencies
Two options:

### Option A — install manually
```bash
pip install flask pandas scikit-learn joblib
```

### Option B — use requirements.txt
If you have a `requirements.txt`:
```bash
pip install -r requirements.txt
```

Example contents:
```
flask==2.3.3
pandas==1.5.3
scikit-learn==1.2.2
joblib==1.3.2
```

---

## 📊 Dataset
The CSV file must contain these columns (names must match exactly):
- `koi_prad` — planet radius (Earth radii)  
- `koi_srad` — star radius (Solar radii)  
- `koi_depth` — transit depth (ppm)  
- `koi_duration` — transit duration (hours)  
- `koi_teq` — equilibrium temperature (K)  
- `koi_insol` — incident flux (Earth units)  
- `koi_period` — orbital period (days)  
- `koi_duration_err2` — duration error (hours)  
- **Target column**: `koi_disposition` — planet class (`CONFIRMED`, `CANDIDATE`, `FALSE POSITIVE`)  

Quick check:
```python
import pandas as pd
df = pd.read_csv("cumulative_2025.10.03_22.30.54.csv")
print(df.columns.tolist())
```

---

## 🚀 Running the App
1. Place `Final.py` and `cumulative_2025.10.03_22.30.54.csv` in the same folder.  
   - If `forest_model_data1_v3.pkl` is missing, it will be created on first run.  
2. Start the app:
```bash
python Final.py
```
3. Open your browser:
```
http://127.0.0.1:5000
```

Console output will show model training accuracy (if model was rebuilt) and Flask startup logs.

---

## 🖥 Using the Web Interface
- The homepage displays a form to enter all planet features.  
- Fill in numeric values for each field and click **Predict**.  
- The result (`CONFIRMED`, `CANDIDATE`, or `FALSE POSITIVE`) will be shown below the form.

---

## 🔌 Using the REST API
POST request to `/predict` with JSON body:

### Example (Linux/macOS with curl)
```bash
curl -X POST "http://127.0.0.1:5000/predict"  -H "Content-Type: application/json"  -d '{"koi_prad":1.0,"koi_srad":1.0,"koi_depth":500,"koi_duration":2.5,"koi_teq":300,"koi_insol":1.2,"koi_period":365,"koi_duration_err2":0.1}'
```

Response:
```json
{"predicted_class":"CANDIDATE"}
```

### Example (Windows PowerShell)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method POST -Body (@{
  koi_prad = 1.0
  koi_srad = 1.0
  koi_depth = 500
  koi_duration = 2.5
  koi_teq = 300
  koi_insol = 1.2
  koi_period = 365
  koi_duration_err2 = 0.1
} | ConvertTo-Json) -ContentType "application/json"
```

---

## 🔄 Retraining the Model
If you want to force retraining:  
- Delete the saved model file:
```bash
rm forest_model_data1_v3.pkl    # Linux/macOS
del forest_model_data1_v3.pkl   # Windows cmd
```
- Restart `Final.py`. A new model will be trained and saved.

---

## ⚙️ Customizing
- **Change CSV path or model file name**: edit variables in `Final.py`:
  ```python
  data_file = "cumulative_2025.10.03_22.30.54.csv"
  model_file = "forest_model_data1_v3.pkl"
  ```
- **Change host/port or disable debug**: edit the last line:
  ```python
  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=8080, debug=False)
  ```

---

## ❗ Common Issues

- **ModuleNotFoundError / ImportError**  
  → Install the missing package, e.g.:  
  ```bash
  pip install pandas
  ```

- **FileNotFoundError: cumulative_2025.10.03_22.30.54.csv**  
  → Check file name and location. Place CSV in the same folder or update `data_file`.

- **ValueError during prediction**  
  → Ensure JSON contains **all required fields** and values are numeric.

- **Pickle compatibility error (scikit-learn version mismatch)**  
  → Retrain the model (`delete forest_model_data1_v3.pkl`) or install a compatible scikit-learn version.

- **CSV encoding errors**  
  → Try:
  ```python
  pd.read_csv("file.csv", encoding="utf-8")
  ```
  or `"cp1251"` (Windows CSV).

---

## 🔧 Suggestions for Improvement
- Separate training into `train_model.py` and keep `Final.py` only for serving.  
- Add advanced metrics (F1-score, confusion matrix).  
- Use Docker for easier environment setup.  
- Log predictions and errors.  
- Deploy with `gunicorn` or `uvicorn` if moving beyond local use.

---

📅 **This guide is written for local usage.**  
Everything works offline on your own computer.
