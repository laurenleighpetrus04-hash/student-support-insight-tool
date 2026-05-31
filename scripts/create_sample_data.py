from pathlib import Path
import random

import pandas as pd


random.seed(7)
## Sample data generation for 50 learners in the Learn to Code program
AGE_BANDS = ["18-24", "25-29", "30-35"]
PROVINCES = [
    "Western Cape",
    "Gauteng",
    "KZN",
    "Eastern Cape",
    "Limpopo",
    "Free State",
    "Northern Cape",
]
DEVICES = ["Laptop", "Shared laptop", "Phone only"]
INTERNET = ["Reliable", "Unstable", "Limited"]
EMPLOYMENT = ["Unemployed", "Under-employed", "Employed part-time"]
SUPPORT_NEEDS = ["Data", "Transport", "Academic support", "Mentoring"]
ATTENDANCE_RISK = ["Low", "Medium", "High"]

NOTES_BY_SUPPORT = {
    "Data": "Needs data support for online learning.",
    "Transport": "May need transport support to attend sessions.",
    "Academic support": "Needs extra help with programming fundamentals.",
    "Mentoring": "Would benefit from mentoring and career guidance.",
}

## Function to make weighted random choices based on specified probabilities
def weighted_choice(options: list[str], weights: list[int]) -> str:
    return random.choices(options, weights=weights, k=1)[0]

## Function to build a single learner's data based on defined distributions and logic
def build_learner(index: int) -> dict:
    support_need = weighted_choice(SUPPORT_NEEDS, [35, 20, 30, 15])

    device_access = weighted_choice(DEVICES, [40, 30, 30])
    internet_access = weighted_choice(INTERNET, [35, 35, 30])
    attendance_risk = weighted_choice(ATTENDANCE_RISK, [35, 35, 30])

    if device_access == "Phone only" or internet_access == "Limited":
        digital_confidence = random.randint(1, 3)
        programming_confidence = random.randint(1, 3)
        ai_familiarity = random.randint(1, 3)
    else:
        digital_confidence = random.randint(2, 5)
        programming_confidence = random.randint(1, 5)
        ai_familiarity = random.randint(1, 5)

    return {
        "learner_id": f"L{index:03}",
        "age_band": random.choice(AGE_BANDS),
        "province_area": random.choice(PROVINCES),
        "device_access": device_access,
        "internet_access": internet_access,
        "digital_confidence": digital_confidence,
        "programming_confidence": programming_confidence,
        "ai_familiarity": ai_familiarity,
        "employment_status": weighted_choice(EMPLOYMENT, [55, 30, 15]),
        "support_need": support_need,
        "attendance_risk": attendance_risk,
        "notes": NOTES_BY_SUPPORT[support_need],
    }


## Main function to generate the synthetic learners data and save it as a CSV file
def main() -> None:
    output_path = Path("data/synthetic_learners.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [build_learner(index) for index in range(1, 51)]
    df = pd.DataFrame(rows)

    df.to_csv(output_path, index=False)

    print(f"Created {output_path}")
    print(f"Rows: {len(df)}")


if __name__ == "__main__":
    main()