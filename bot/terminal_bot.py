import sys
import os

# Add the parent directory to the Python path so we can import from ml_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.advisory_agent import generate_advisory

def main():
    print("==================================================")
    print("🌾 Welcome to the AgTech Mandi Terminal Bot! 🌾")
    print("==================================================")
    print("I can help you with real-time prices, profit calculations, and forecasts.")
    print("Try typing something like: 'District: Nashik, Crop: Onion'")
    print("(Type 'exit' or 'quit' to close)")
    print("--------------------------------------------------\n")

    while True:
        try:
            text = input("Farmer (You): ")
            if text.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if "nashik" in text.lower() and "onion" in text.lower():
                # Mocking incoming data pipeline for Nashik Onion
                crop_quality_data = {"quality_score": 0.85, "defect_grade": "B"}
                spatial_data = {
                    "usable_quantity": 20, # quintals
                    "spoilage_decay_rate": {"Nashik Local": 0, "Mumbai APMC": 0.5, "Pune Mandi": 0.2},
                    "transit_times": {"Nashik Local": 1, "Mumbai APMC": 4, "Pune Mandi": 3},
                    "base_prices": {"Nashik Local": 1500, "Mumbai APMC": 2100, "Pune Mandi": 1800},
                    "distances": {"Nashik Local": 10, "Mumbai APMC": 160, "Pune Mandi": 210},
                    "fuel_rate": 15, # ₹/km
                    "tolls": {"Nashik Local": 0, "Mumbai APMC": 400, "Pune Mandi": 250},
                    "wages": {"Nashik Local": 200, "Mumbai APMC": 1000, "Pune Mandi": 800}
                }
                
                reply = generate_advisory(
                    farmer_query=text,
                    crop_quality_data=crop_quality_data,
                    spatial_data=spatial_data,
                    local_market_name="Nashik Local"
                )
            else:
                reply = "I couldn't find data for that combination. Please specify 'District: [Name], Crop: [Name]'."
                
            print(f"\nAgTech Bot: {reply}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == '__main__':
    main()
