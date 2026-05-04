import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_and_compare_models(input_file='processed_diabetes.csv'):
    print(f"Loading preprocessed data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'. Please run 01_preprocess.py first.")
        return

    # Split into Features (X) and Target (y)
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    # Split into Training and Testing Sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}\n")

    # Define the models we want to compare
    models = {
        "Logistic Regression": LogisticRegression(),
        "Random Forest": RandomForestClassifier(random_state=42),
        "Support Vector Machine": SVC()
    }

    results = []

    print("--- Model Comparison Results ---")
    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions on the test set
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Store and print results
        results.append({'Model': name, 'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1})
        print(f"{name}:")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1-Score:  {f1:.4f}\n")

    # Save results to a CSV so you can put it in your paper
    results_df = pd.DataFrame(results)
    results_df.to_csv('model_comparison_results.csv', index=False)
    print("Saved comparison metrics to 'model_comparison_results.csv'.")
    print("You can use these results for your baseline before applying your security analysis!")

if __name__ == "__main__":
    train_and_compare_models()
