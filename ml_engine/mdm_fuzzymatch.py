import pandas as pd
from rapidfuzz import process, fuzz

def standardize_names(raw_names, master_list, threshold=80):
    standardized = []
    for name in raw_names:
        match = process.extractOne(name, master_list, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= threshold:
            standardized.append(match[0])
        else:
            standardized.append(name) # fallback
    return standardized

if __name__ == "__main__":
    # Mock data demonstration
    master_commodities = ["Potato", "Onion", "Tomato", "Wheat", "Rice"]
    raw_data = ["Aloo", "Potato", "Alu", "Onions", "Pyaz", "Tomatos"]
    
    # In a real scenario, this would map synonmys or translate before fuzzing, 
    # but for simple typo correction:
    print("Standardizing names:")
    print(standardize_names(["Potatos", "Onionn"], master_commodities))
