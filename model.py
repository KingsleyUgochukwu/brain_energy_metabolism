import pandas as pd

# Neuronal Energy Metabolism Model
# Version 4: Glucose-dependent ATP simulation


# ATP demand for different activity levels
activity_levels = {
    "Resting": 50,
    "Moderate": 70,
    "High": 95
}

# Store all simulation results
results = []

# Different glucose availability conditions
glucose_conditions = [1.0, 0.8, 0.6, 0.4, 0.2]


# Simulate each glucose condition
for glucose_availability in glucose_conditions:

    # Glycolysis
    glycolysis_capacity = 100
    glycolysis_rate = glycolysis_capacity * glucose_availability

    # Glycolysis produces pyruvate
    pyruvate_production = glycolysis_rate

    # Fraction of pyruvate entering the TCA cycle
    tca_conversion = 0.8
    tca_flux = pyruvate_production * tca_conversion

    # TCA cycle produces NADH and FADH2
    NADH_production = tca_flux * 3
    FADH2_production = tca_flux * 1

    # Mitochondrial efficiency
    mitochondrial_efficiency = 0.5

    # Oxidative phosphorylation
    oxidative_phosphorylation = (
        (NADH_production * 2.5) +
        (FADH2_production * 1.5)
    ) * mitochondrial_efficiency

    # Final ATP production
    ATP_production = oxidative_phosphorylation

    print("Glucose availability:", glucose_availability)
    print("Glycolysis rate:", glycolysis_rate)
    print("ATP production:", ATP_production)
    print()


    # Simulate each activity level
    for activity, ATP_demand in activity_levels.items():

        # Starting ATP level
        ATP_level = 100

        print("Activity level:", activity)

        # Record starting ATP
        print("Minute: 0 | ATP level:", ATP_level)

        # Simulate minutes 1 to 10
        for minute in range(1, 11):

            # Calculate ATP balance
            ATP_balance = ATP_production - ATP_demand
            # ATP supply relative to neuronal ATP demand
            ATP_ratio = ATP_production / ATP_demand
            # Update ATP level
            ATP_level = max(0, ATP_level + (ATP_balance * 0.1))

            print(
                "Minute:", minute,
                "| ATP demand:", ATP_demand,
                "| ATP balance:", ATP_balance,
                "| ATP level:", ATP_level
            )

            # Store result
            results.append({
                "glucose": glucose_availability,
                "minute": minute,
                "activity": activity,
                "ATP_demand": ATP_demand,
                "ATP_production": ATP_production,
                "ATP_balance": ATP_balance,
                "ATP_ratio": ATP_ratio,
                "ATP_level": ATP_level
            })

        print()


# Convert results into a DataFrame
results_df = pd.DataFrame(results)

print(results_df)

# Save results
results_df.to_csv("simulation_results.csv", index=False)
import matplotlib.pyplot as plt
import os

# Create figures folder if it does not exist
os.makedirs("results/figures", exist_ok=True)

# Use one value per glucose/activity condition
ratio_data = results_df[results_df["minute"] == 1]
summary_table = ratio_data[
    [
        "glucose",
        "activity",
        "ATP_production",
        "ATP_demand",
        "ATP_balance",
        "ATP_ratio"
    ]
]

summary_table.to_csv(
    "results/glucose_activity_summary.csv",
    index=False
)

print("\nGlucose-Activity Summary:")
print(summary_table)

for activity in activity_levels.keys():

    activity_data = ratio_data[
        ratio_data["activity"] == activity
    ]

    plt.plot(
        activity_data["glucose"],
        activity_data["ATP_ratio"],
        marker="o",
        label=activity
    )

# Threshold where ATP production equals ATP demand
plt.axhline(
    y=1,
    linestyle="--",
    label="Supply = Demand"
)

plt.xlabel("Relative Glucose Availability")
plt.ylabel("ATP Supply / Demand Ratio")
plt.title("Effect of Glucose Availability on Neuronal Energy Balance")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "results/figures/atp_supply_demand.png",
    dpi=300
)

plt.show()