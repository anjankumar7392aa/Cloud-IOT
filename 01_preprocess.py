import pandas as pd
import numpy as np

def preprocess_data(input_file='diabetes.csv', output_file='processed_diabetes.csv'):
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find '{input_file}'. Please make sure the dataset is in the same folder.")
        return

    # 1. Select only 4 columns to keep it simple as requested
    columns_to_keep = ['Glucose', 'BloodPressure', 'BMI', 'Outcome']
    print(f"\nSelecting 4 columns: {columns_to_keep}")
    df_subset = df[columns_to_keep].copy()

    # 2. Add Unique Patient ID column at the beginning
    # Creating IDs like PID-1, PID-2, etc.
    df_subset.insert(0, 'Patient_ID', ['PID-' + str(i+1) for i in range(len(df_subset))])
    print("Added unique 'Patient_ID' column for each row.")

    # 3. Replace 0 with NaN for valid biological metrics
    cols_with_zeros = ['Glucose', 'BloodPressure', 'BMI']
    df_subset[cols_with_zeros] = df_subset[cols_with_zeros].replace(0, np.nan)

    # 4. Impute missing values with the mean of each column
    for col in cols_with_zeros:
        mean_value = df_subset[col].mean()
        df_subset[col] = df_subset[col].fillna(mean_value)

    # 5. Save the new preprocessed dataset
    df_subset.to_csv(output_file, index=False)
    print(f"\nPreprocessing complete! Saved clean dataset to '{output_file}'")
    print("\nFirst 5 rows of the new dataset:")
    print(df_subset.head())

if __name__ == "__main__":
    preprocess_data()
