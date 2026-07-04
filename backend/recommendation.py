import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


df_clean = joblib.load("laptop_data.pkl")
preprocessor = joblib.load("preprocessor.pkl")
scaler = joblib.load("scaler.pkl")
feature_columns = joblib.load("feature_columns.pkl")


def gaming_score(row):

    score = 0
    ram = int(str(row["Ram"]).replace("GB",""))

    if "RTX" in str(row["gpu_family"]):
        score += 50
    elif "GTX" in str(row["gpu_family"]):
        score += 30
    elif "Radeon" in str(row["gpu_family"]):
        score += 25

    score += row["vram"] * 5
    score += ram * 2
    score += row["cores"] * 2

    return score


def coding_score(row):

    score = 0

    ram = int(str(row["Ram"]).replace("GB", ""))

    # CPU
    score += row["cores"] * 5
    score += row["threads"] * 2

    # RAM
    score += ram * 4

    # Spec Rating
    score += row["spec_rating"] * 0.5

    # SSD
    if "SSD" in str(row["ROM_type"]):
        score += 10

    # CPU Family
    cpu = str(row["cpu_family"]).lower()

    if "i7" in cpu or "ryzen 7" in cpu:
        score += 15
    elif "i5" in cpu or "ryzen 5" in cpu:
        score += 10
    elif "i3" in cpu or "celeron" in cpu:
        score -= 10

    # Office-friendly laptops ko halka boost
    if "Vivobook" in str(row["name"]):
        score += 8
    elif "ThinkPad" in str(row["name"]):
        score += 12
    elif "IdeaPad" in str(row["name"]):
        score += 8
    elif "Zenbook" in str(row["name"]):
        score += 10

    # Gaming laptop ko halka penalty
    if "Gaming" in str(row["name"]):
        score -= 12

    return score


def office_score(row):

    score = 0

    ram = int(str(row["Ram"]).replace("GB",""))

    score += ram * 2
    score += row["spec_rating"] * 0.7

    if "SSD" in str(row["ROM_type"]):
        score += 15

    if "Windows" in str(row["OS"]):
        score += 10

    if "Gaming" in str(row["name"]):
        score -= 10

    return score

def get_score(row, use_case):

    use_case = use_case.lower()

    if use_case == "gaming":
        return gaming_score(row)

    elif use_case == "coding":
        return coding_score(row)

    elif use_case == "office":
        return office_score(row)

    return 0


def recommend_laptops(
    user_budget,
    primary_use,
    secondary_use=None,
    top_n=5
):

    df = df_clean.copy()

    # Budget filter (±5k)
    df = df[
        (df["price"] >= user_budget - 5000) &
        (df["price"] <= user_budget + 5000)
    ].copy()

    # Agar budget range me laptop hi nahi mila
    if df.empty:
        return "No laptops found in this budget."

    # Primary score
    df["primary_score"] = df.apply(
        lambda row: get_score(row, primary_use),
        axis=1
    )

    # Secondary score
    if secondary_use:

        df["secondary_score"] = df.apply(
            lambda row: get_score(row, secondary_use),
            axis=1
        )

        df["final_score"] = (
            0.85 * df["primary_score"] +
            0.15 * df["secondary_score"]
        )

    else:

        df["final_score"] = df["primary_score"]

    # Sort by score
    df = df.sort_values(
        "final_score",
        ascending=False
    )

    # Top 50 candidates
    df = df.head(50)

    # Prepare features
    x_candidate = df.drop(
        columns=[
            "name",
            "price",
            "primary_score",
            "secondary_score",
            "final_score"
        ],
        errors="ignore"
    )

    x_candidate = x_candidate.reindex(columns=feature_columns)
    x_candidate = x_candidate.fillna(0)

    x_enc = preprocessor.transform(x_candidate)
    x_scaled_candidate = scaler.transform(x_enc)

    # KNN
    knn = NearestNeighbors(metric="cosine")
    knn.fit(x_scaled_candidate)

    query_vector = x_scaled_candidate[0].reshape(1, -1)

    distances, indices = knn.kneighbors(
        query_vector,
        n_neighbors=min(top_n, len(df))
    )

    result = df.iloc[indices[0]].copy()

    result["name"] = (
    result["brand"].astype(str).str.strip() + " " +
    result["name"].astype(str).str.strip()
)

# Processor
    result["processor"] = (
    result["cpu_brand"].astype(str) + " " +
    result["cpu_family"].astype(str) + "-" +
    result["generation"].astype(str)
)

# Memory
    result["memory"] = (
    result["Ram"].astype(str) + "GB RAM • " +
    np.where(
        result["ROM"].between(1, 4),
        result["ROM"].astype(str) + "TB " + result["ROM_type"].astype(str),
        result["ROM"].astype(str) + "GB " + result["ROM_type"].astype(str)
    )
)

# Graphics
    result["graphics"] = np.where(
    result["vram"] == 0,
    result["gpu_brand"].astype(str) + " " +
    result["gpu_family"].astype(str),

    result["gpu_brand"].astype(str) + " " +
    result["gpu_family"].astype(str) + " " +
    result["vram"].astype(str) + "GB"
)
    
    result["name"] = (
    result["name"]
    .str.replace("Gaming Laptop", "", regex=False)
    .str.replace("Laptop", "", regex=False)
    .str.replace("Notebook", "", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
    .str[:17]
)

# Final response
    result = result[
    [
        "name",
        "price",
        "processor",
        "memory",
        "graphics",
        "final_score"
    ]
]

    return result.to_dict(orient="records")