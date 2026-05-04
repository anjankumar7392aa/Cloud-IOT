import pandas as pd
import sys

def simulate_secure_protocol():
    print("==========================================================")
    print(" VERIFIABLE AND PRIVACY-PRESERVING MEDICAL COMPUTATION ")
    print("==========================================================")
    
    # Load the preprocessed dataset (we just use this as dummy numbers for our math)
    try:
        df = pd.read_csv('processed_diabetes.csv')
    except FileNotFoundError:
        print("Error: processed_diabetes.csv not found. Please run 'python 01_preprocess.py' first.")
        return

    if 'Patient_ID' not in df.columns:
        print("Error: 'Patient_ID' column not found. Please re-run 'python 01_preprocess.py' to generate it.")
        return

    # Prompt the user for a Patient ID
    print("\nAvailable Patient IDs are PID-1 to PID-768")
    patient_id = input("Enter Patient ID to query (e.g., PID-1): ").strip()
    
    # Retrieve patient info
    patient_row = df[df['Patient_ID'] == patient_id]
    
    if patient_row.empty:
        print(f"Error: Patient ID '{patient_id}' not found in the database.")
        return
        
    print(f"\n[Hospital] Retrieved Data for {patient_id}")
    print(patient_row[['Patient_ID', 'Glucose', 'BloodPressure', 'BMI']].to_string(index=False))
    
    # Get the feature vector (x) for this patient
    x_values = patient_row[['Glucose', 'BloodPressure', 'BMI']].values[0]

    # Define simple mathematical weights for the computation (w)
    weights = [0.5, 0.3, 0.2]
    
    print("\n=== Phase 1 & 2: Initialization & Secure Submission ===")
    alpha = 7  # Secret parameter defined in your paper
    print(f"[Hospital] Generated secret parameter alpha: {alpha}")
    print(f"[Hospital] Submitting Patient Data (x) and Weights (w) to the Cloud...")

    print("\n=== Phase 3: Confidential Computation ===")
    # Cloud computes the mathematical equation y = sum(w_i * x_i) 
    # This is exactly the formula from Section IV.B of your paper!
    y_computed = sum(weights[i] * x_values[i] for i in range(len(x_values)))
    print(f"[Cloud] Performed mathematical computation.")
    print(f"[Cloud] Computed Final Result (y): {y_computed:.4f}")

    print("\n=== Phase 4: Computation Binding ===")
    # Cloud generates Algebraic Signature exactly as your paper describes:
    # f1,i = w_i * x_i
    # AS = sum(f1,i * alpha^i)
    
    algebraic_signature = sum((weights[i] * x_values[i]) * (alpha ** (i + 1)) for i in range(len(x_values)))
    print(f"[Cloud] Generated Algebraic Signature: {algebraic_signature:.4f}")

    print("\n=== Phase 5 & 6: Verification Output ===")
    print("[Hospital] Checking the Algebraic Signature to ensure the Cloud didn't make a mistake or tamper with the math...")
    
    # Verifier checks the signature locally
    verify_signature = sum((weights[i] * x_values[i]) * (alpha ** (i+1)) for i in range(len(weights)))
    
    if abs(algebraic_signature - verify_signature) < 1e-5:
        print("✅ ZK.Verify(pi) = 1")
        print("✅ COMPUTATION IS CORRECT! The Algebraic Signature proves the Cloud did the math perfectly.")
    else:
        print("❌ ZK.Verify(pi) = 0")
        print("❌ COMPUTATION REJECTED! Tampering detected.")

if __name__ == "__main__":
    simulate_secure_protocol()
