import pandas as pd
import matplotlib.pyplot as plt
import os


# -----------------------------------------
# Neuronal Energy Metabolism
# Local Sensitivity Analysis
# -----------------------------------------

# Baseline model parameters
baseline_parameters = {
    "glucose_availability": 0.5,
    "tca_conversion": 0.8,
    "mitochondrial_efficiency": 0.5
}

glycolysis_capacity = 100


def calculate_atp(
    glucose_availability,
    tca_conversion,
    mitochondrial_efficiency
):
    """Calculate ATP production from model parameters."""

    glycolysis_rate = (
        glycolysis_capacity * glucose_availability
    )

    pyruvate_production = glycolysis_rate

    tca_flux = (
        pyruvate_production * tca_conversion
    )

    NADH_production = tca_flux * 3
    FADH2_production = tca_flux * 1

    ATP_production = (
        (NADH_production * 2.5) +
        (FADH2_production * 1.5)
    ) * mitochondrial_efficiency

    return ATP_production


# Calculate baseline ATP production
baseline_ATP = calculate_atp(
    baseline_parameters["glucose_availability"],
    baseline_parameters["tca_conversion"],
    baseline_parameters["mitochondrial_efficiency"]
)

print("Baseline ATP production:", baseline_ATP)
print()


# Percentage change used for sensitivity analysis
change = 0.10

results = []


# Test each parameter individually
for parameter, baseline_value in baseline_parameters.items():

    for direction in [-1, 1]:

        modified_parameters = baseline_parameters.copy()

        modified_value = baseline_value * (
            1 + direction * change
        )

        modified_parameters[parameter] = modified_value

        new_ATP = calculate_atp(
            modified_parameters["glucose_availability"],
            modified_parameters["tca_conversion"],
            modified_parameters["mitochondrial_efficiency"]
        )

        percent_ATP_change = (
            (new_ATP - baseline_ATP) /
            baseline_ATP
        ) * 100

        sensitivity_coefficient = (
            percent_ATP_change /
            (direction * change * 100)
        )

        results.append({
            "parameter": parameter,
            "parameter_change_percent":
                direction * change * 100,
            "ATP_production": new_ATP,
            "ATP_change_percent":
                percent_ATP_change,
            "sensitivity_coefficient":
                sensitivity_coefficient
        })


# Convert to DataFrame
results_df = pd.DataFrame(results)

print(results_df)


# Create results directories if necessary
os.makedirs("results/figures", exist_ok=True)


# Save sensitivity results
results_df.to_csv(
    "results/sensitivity_analysis.csv",
    index=False
)


# Calculate average absolute sensitivity
summary = (
    results_df
    .groupby("parameter")["sensitivity_coefficient"]
    .apply(lambda x: x.abs().mean())
    .reset_index()
)

summary.columns = [
    "parameter",
    "mean_absolute_sensitivity"
]

print()
print("Sensitivity summary:")
print(summary)


# Plot sensitivity coefficients
plt.figure(figsize=(8, 5))

plt.bar(
    summary["parameter"],
    summary["mean_absolute_sensitivity"]
)

plt.xlabel("Model Parameter")
plt.ylabel("Mean Absolute Sensitivity Coefficient")
plt.title("Sensitivity of ATP Production to Model Parameters")

plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    "results/figures/sensitivity_analysis.png",
    dpi=300
)

plt.show()