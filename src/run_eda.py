import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_loader import UnifiedDataLoader

def run_exploratory_analysis():
    # Initialize the data loader
    loader = UnifiedDataLoader(data_dir="data/raw")
    
    try:
        df = loader.load_raw_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Split dataset into subsets based on the unified schema structure
    obs, envs, links, targets = loader.split_by_record_type(df)
    
    print("--- Dataset Quality Assessment ---")
    print(f"Total Records: {len(df)}")
    print(f"- Observations: {len(obs)}")
    print(f"- Events: {len(envs)}")
    print(f"- Impact Links: {len(links)}")
    print(f"- Targets: {len(targets)}\n")
    
    # Ensure reports/figures directory exists
    os.makedirs("reports/figures", exist_ok=True)
    
    # Setup plotting style
    sns.set_theme(style="whitegrid")
    
    # --- Visualization 1: Access (Account Ownership Rate Trajectory) ---
    acc_df = loader.get_indicator_subset(obs, "ACC_OWNERSHIP")
    
    if not acc_df.empty:
        plt.figure(figsize=(8, 5))
        plt.plot(acc_df['observation_date'], acc_df['value_numeric'], marker='o', linewidth=2.5, color='#1f77b4')
        plt.title("Ethiopia Account Ownership Rate Trajectory (Findex)", fontsize=14, pad=15)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Account Ownership Rate (%)", fontsize=12)
        plt.ylim(0, 100)
        
        # Annotate points to emphasize the 2021-2024 slowdown paradox
        for _, row in acc_df.iterrows():
            plt.annotate(f"{row['value_numeric']}%", 
                         (row['observation_date'], row['value_numeric']),
                         textcoords="offset points", xytext=(0,10), ha='center', weight='bold')
            
        plt.tight_layout()
        plt.savefig("reports/figures/01_account_ownership_trajectory.png")
        plt.close()
        print("[Saved] reports/figures/01_account_ownership_trajectory.png")
    else:
        print("[Warning] ACC_OWNERSHIP data missing from observations.")

    # --- Visualization 2: Temporal Coverage Map ---
    plt.figure(figsize=(10, 6))
    obs_summary = obs.groupby(['indicator_code', obs['observation_date'].dt.year]).size().unstack(fill_value=0)
    if not obs_summary.empty:
        sns.heatmap(obs_summary, cmap="YlGnBu", cbar=False, linewidths=0.5, annot=True)
        plt.title("Data Sparsity & Temporal Coverage Profile", fontsize=14, pad=15)
        plt.xlabel("Observation Year", fontsize=12)
        plt.ylabel("Indicator Code", fontsize=12)
        plt.tight_layout()
        plt.savefig("reports/figures/02_temporal_coverage_profile.png")
        plt.close()
        print("[Saved] reports/figures/02_temporal_coverage_profile.png")

if __name__ == "__main__":
    run_exploratory_analysis()
