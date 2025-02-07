import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from matplotlib.patches import Patch
import matplotlib

# Use a non-interactive backend
matplotlib.use('Agg')

# Load JSON data
with open("c:/Users/zusakhe_gradesmatch/Downloads/School_Counts_By_Category(2024).json", "r") as file:
    data = json.load(file)

# Define categories and extract schools as sets
categories = [
    ("CombinedTimeMinutes < 1", set(school["School"] for school in data["CombinedTimeMinutes < 1"]["Schools"] if isinstance(school, dict))),
    ("7 <= CombinedTimeMinutes < 20", set(school["School"] for school in data["7 <= CombinedTimeMinutes < 20"]["Schools"] if isinstance(school, dict))),
    ("20 <= CombinedTimeMinutes < 40", set(school["School"] for school in data["20 <= CombinedTimeMinutes < 40"]["Schools"] if isinstance(school, dict))),
    ("40 <= CombinedTimeMinutes < 60", set(school["School"] for school in data["40 <= CombinedTimeMinutes < 60"]["Schools"] if isinstance(school, dict))),
    ("60 <= CombinedTimeMinutes < 80", set(school["School"] for school in data["60 <= CombinedTimeMinutes < 80"]["Schools"] if isinstance(school, dict))),
    ("80 <= CombinedTimeMinutes < 100", set(school["School"] for school in data["80 <= CombinedTimeMinutes < 100"]["Schools"] if isinstance(school, dict))),
    ("100 <= CombinedTimeMinutes < 180", set(school["School"] for school in data["100 <= CombinedTimeMinutes < 180"]["Schools"] if isinstance(school, dict))),
    ("CombinedTimeMinutes >= 180", set(school["School"] for school in data["CombinedTimeMinutes >= 180"]["Schools"] if isinstance(school, dict))),
]

# Define colors for each category
category_colors = {
    "CombinedTimeMinutes < 1": "blue",
    "7 <= CombinedTimeMinutes < 20": "green",
    "20 <= CombinedTimeMinutes < 40": "orange",
    "40 <= CombinedTimeMinutes < 60": "purple",
    "60 <= CombinedTimeMinutes < 80": "yellow",
    "80 <= CombinedTimeMinutes < 100": "cyan",
    "100 <= CombinedTimeMinutes < 180": "brown",
    "CombinedTimeMinutes >= 180": "pink",
}

# Extract pairwise duplicate counts from the JSON
pairwise_duplicates = data.get("PairwiseDuplicateSchoolCounts", {})

# Generate Venn diagrams for all categories in groups of three
output_diagram_paths = []
for i in range(0, len(categories), 3):
    # Select up to three categories for this Venn diagram
    category_chunk = categories[i:i + 3]
    labels = [cat[0] for cat in category_chunk]
    sets = [cat[1] for cat in category_chunk]

    # Pad labels and sets to ensure exactly 3 elements
    while len(labels) < 3:
        labels.append("")
        sets.append(set())

    # Create the Venn diagram
    fig, ax = plt.subplots(figsize=(12, 8))
    venn = venn3(subsets=sets, set_labels=labels)

    # Apply colors to the diagram regions
    region_ids = ['100', '010', '001', '110', '101', '011', '111']
    for idx, subset_id in enumerate(region_ids):
        patch = venn.get_patch_by_id(subset_id)
        if patch:
            # Check if it's a disjunction or intersection and assign appropriate counts
            if subset_id in ['100', '010', '001']:  # Unique regions (disjunction)
                patch.set_color(category_colors.get(labels[idx % 3], 'gray'))
                count = len(sets[idx % 3]) - sum(
                    len(pairwise_duplicates.get(f"{labels[idx % 3]}, {labels[j]}", {}).get("SharedSchools", []))
                    for j in range(len(labels)) if j != idx % 3
                )
            else:  # Shared regions (intersection)
                shared_labels = [labels[k] for k in range(len(labels)) if subset_id[k] == '1']
                count = len(
                    set.intersection(*(sets[k] for k in range(len(labels)) if subset_id[k] == '1'))
                )
                patch.set_color("gray")  # Neutral color for shared regions

            patch.set_alpha(0.5)
            # Label each region with the count of schools
            label = venn.get_label_by_id(subset_id)
            if label:
                label.set_text(f"{count}")
                label.set_fontsize(10)

    # Add a legend for the colors
    legend_patches = [
        Patch(color=category_colors[label], label=label)
        for label in labels if label  # Skip empty labels
    ]
    plt.legend(
        handles=legend_patches,
        loc="upper right",
        title="Categories and Colors"
    )

    # Add a title
    plt.title("Venn Diagram of Schools by Combined Time Minutes (2024)")

    # Save the Venn diagram
    output_diagram_path = f"c:/Users/zusakhe_gradesmatch/Downloads/VennDiagram_Schools_{i // 3 + 1}.png"
    plt.savefig(output_diagram_path, dpi=300)
    plt.close()
    output_diagram_paths.append(output_diagram_path)

print(f"Venn diagrams saved to: {', '.join(output_diagram_paths)}")
