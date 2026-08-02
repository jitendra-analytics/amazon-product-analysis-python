"""
Amazon Product Analysis Pipeline
Author : Jitendra More
"""

import os
import subprocess
import sys

print("=" * 60)
print(" AMAZON PRODUCT DATA ANALYSIS PIPELINE ")
print("=" * 60)

scripts = [
    "load_data.py",
    "clean_data.py",
    "analysis.py",
    "visualization.py"
    # "database.py"  # MySQL import करायचा असल्यास uncomment करा
]

for script in scripts:

    path = os.path.join("scripts", script)

    print("\n" + "=" * 60)
    print(f"Running : {script}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, path]
    )

    if result.returncode != 0:
        print(f"\n❌ ERROR in {script}")
        break

print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nOutputs Created:")

print("✓ output/cleaned_data.csv")
print("✓ output/charts/")
print("✓ output/reports/")
