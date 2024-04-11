from flask import Flask, jsonify, render_template, request
from model import DiamondModel

app = Flask(__name__)

cuts = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
colors = [
    ('Colorless', ['D', 'E', 'F']),
    ('Near Colorless', ['G', 'H', 'I', 'J']),
    ('Faint Yellow', ['K', 'L', 'M']),
    ('Very Light Yellow', ['N', 'O', 'P', 'Q', 'R']),
    ('Light Yellow', ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
]
clarities = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
    
# Initialize the model
model = DiamondModel("models/")

if __name__ == "__main__":
    app.run(port=5000)

def extract_data(raw_data):
    data = {}
    data["cut"] = raw_data["cut"]
    data["color"] = raw_data["color"]
    data["clarity"] = raw_data["clarity"]
    data["carat"] = float(raw_data["carat"])
    data["x"] = float(raw_data["x"])
    data["y"] = float(raw_data["y"])
    data["z"] = float(raw_data["z"])
    data["table"] = float(raw_data["table"])
    data["depth"] = float(raw_data["depth"])

    return data

@app.route("/")
def index():
    form_values = {}
    features = {}
    return render_template('index.html',
                            cuts=cuts,
                            colors=colors,
                            old_values=form_values,
                            clarities=clarities,
                            features=features)

@app.post("/api/predict-price")
@app.post("/predict-price")
def predict_price():
    form_values = {field: request.form[field] for field in request.form}
    
    if request.path == "/api/predict-price":
        if request.headers.get('Content-Type') == "application/json":
            data = extract_data(request.json)
        else: return jsonify({"message": "Content-Type not supported"})
    else:
        data = extract_data(request.form)
    
    # Data preparation
    row = model.prepare_data(data)

    # Prediction
    price = model.predict(row)

    # Calculate features importance
    shap_df = model.get_features_importance(row)

    # Return the response as a JSON if used the API endpoint, else render the page
    if request.path == "/api/predict-price":
        return jsonify({'predictedPrice': price[0], "featuresImportance": shap_df.to_dict()})
    return render_template('index.html',
                            cuts=cuts,
                            colors=colors,
                            clarities=clarities,
                            old_values=form_values,
                            predictedPrice=price[0],
                            features=shap_df.to_dict())