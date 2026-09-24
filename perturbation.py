import pandas as pd
import matplotlib.pyplot as plt
import os

# Mitochondrial efficiency conditions
efficiency_conditions = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

# Neuronal activity demands
activity_levels = {
    "Resting": 50,
    "Moderate": 70,
    "High": 95
}

# Keep glucose availability constant for this experiment
glucose_availability = 0.5

results = []

for mitochondrial_efficiency in efficiency_conditions:

    # Glycolysis
    glycolysis_capacity = 100
    glycolysis_rate = glycolysis_capacity * glucose_availability

    # Pyruvate and TCA cycle
    pyruvate_production = glycolysis_rate
    tca_conversion = 0.8
    tca_flux = pyruvate_production * tca_conversion

    # Electron carriers
    NADH_production = tca_flux * 3
    FADH2_production = tca_flux * 1

    # Oxidative phosphorylation
    ATP_production = (
        (NADH_production * 2.5) +
        (FADH2_production * 1.5)
    ) * mitochondrial_efficiency

    for activity, ATP_demand in activity_levels.items():

        ATP_balance = ATP_production - ATP_demand
        ATP_ratio = ATP_production / ATP_demand

        results.append({
            "mitochondrial_efficiency": mitochondrial_efficiency,
            "activity": activity,
            "ATP_production": ATP_production,
            "ATP_demand": ATP_demand,
            "ATP_balance": ATP_balance,
            "ATP_ratio": ATP_ratio
        })

# Convert results to table
results_df = pd.DataFrame(results)

print(results_df)

# Save results
os.makedirs("results/figures", exist_ok=True)

results_df.to_csv(
    "results/mitochondrial_perturbation.csv",
    index=False
)

# Plot perturbation results
for activity in activity_levels:

    activity_data = results_df[
        results_df["activity"] == activity
    ]

    plt.plot(
        activity_data["mitochondrial_efficiency"],
        activity_data["ATP_ratio"],
        marker="o",
        label=activity
    )

# ATP supply = ATP demand threshold
plt.axhline(
    y=1,
    linestyle="--",
    label="Supply = Demand"
)

plt.xlabel("Mitochondrial Efficiency")
plt.ylabel("ATP Supply / Demand Ratio")
plt.title("Effect of Mitochondrial Efficiency on Neuronal Energy Balance")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/figures/mitochondrial_perturbation.png",
    dpi=300
)

plt.show()