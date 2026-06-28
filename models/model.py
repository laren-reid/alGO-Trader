from sklearn.ensemble import RandomForestClassifier


def create_model():

    return RandomForestClassifier(
        n_estimators=150,
        max_depth=6,
        random_state=42
    )
