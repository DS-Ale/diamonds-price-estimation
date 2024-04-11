import pickle
import os
import numpy as np
import shap
import pandas as pd

# Map frontend Cut categories to those used in the Model
cut_map = {
    'Poor': "Fair",
    'Fair': "Good",
    'Good': "Very Good",
    'Very Good': "Premium",
    'Excellent': "Ideal"
}

class DiamondModel:
    def __init__(self, path):
        self.model = pickle.load(open(os.path.join(path, 'regression_model.sav'), 'rb'))
        self.encoder = pickle.load(open(os.path.join(path, 'encoder.sav'), 'rb'))
        self.scaler = pickle.load(open(os.path.join(path, 'scaler.sav'), 'rb'))

        # Explainer for features importance
        self.explainer = shap.Explainer(self.model)


    def prepare_data(self, data):
        # Data Preparation
        cut = cut_map.get(data["cut"])
        depth = data["depth"] / data["z"] * 100
        table = data["table"] / data["x"] * 100
        measure = data["x"] * data["y"] * data["z"]

        # Encoding and Normalization
        encoded_categories = self.encoder.transform([[cut, data["color"], data["clarity"]]])
        normalized_numerics = self.scaler.transform([[data["carat"], depth, table, measure]])
        row = np.concatenate([encoded_categories, normalized_numerics], axis=1)
        
        # Ordering features as per model expectations
        return row[:, [3, 0, 1, 2, 4, 5, 6]]
    
    def predict(self, prepared_data):
        return self.model.predict(prepared_data)
    
    def get_features_importance(self, data):
            # Get the features importance
            shap_values = self.explainer(data)
            shap_df = pd.DataFrame(shap_values.values, columns=["carat", "cut", "color", "clarity", "depth", "table", "x * y * z"])
            return shap_df.apply(np.abs).mean().sort_values(ascending=False)