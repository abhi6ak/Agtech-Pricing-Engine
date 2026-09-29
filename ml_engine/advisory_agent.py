import json
import logging

logger = logging.getLogger(__name__)

def calculate_spatial_arbitrage_matrix(usable_quantity, spoilage_decay_rate, transit_times, base_prices, quality_score, distances, fuel_rate, tolls, wages):
    """
    Calculates the Net Profit across different markets to generate a Spatial Arbitrage Matrix.
    
    Formula:
    Net Profit = (Usable Quantity - Spoilage Decay) * (Base Price * Quality Score) - (Distance * Fuel Rate + Tolls + Wages)
    
    Args:
        usable_quantity: float, initial usable quantity in quintals or tons
        spoilage_decay_rate: dict, market_name -> decay amount based on transit
        transit_times: dict, market_name -> transit time in hours
        base_prices: dict, market_name -> base price per unit
        quality_score: float, visual quality score (0.0 to 1.0)
        distances: dict, market_name -> distance in km
        fuel_rate: float, cost of fuel per km
        tolls: dict, market_name -> total toll cost
        wages: dict, market_name -> driver/helper wages for the trip
        
    Returns:
        list of dicts containing market details and calculated net profit, sorted by net profit descending.
    """
    matrix = []
    
    for market in base_prices.keys():
        decay = spoilage_decay_rate.get(market, 0)
        base_price = base_prices.get(market, 0)
        dist = distances.get(market, 0)
        toll = tolls.get(market, 0)
        wage = wages.get(market, 0)
        transit_time = transit_times.get(market, 0)
        
        # Calculate logistics cost
        logistics_cost = (dist * fuel_rate) + toll + wage
        
        # Calculate revenue
        effective_quantity = max(0, usable_quantity - decay)
        revenue = effective_quantity * (base_price * quality_score)
        
        # Calculate net profit
        net_profit = revenue - logistics_cost
        
        matrix.append({
            "market_name": market,
            "net_profit": round(net_profit, 2),
            "distance_km": dist,
            "transit_time_hrs": transit_time,
            "logistics_cost": round(logistics_cost, 2),
            "revenue": round(revenue, 2)
        })
        
    # Rank by net profit descending
    return sorted(matrix, key=lambda x: x["net_profit"], reverse=True)


def synthesize_advisory_recommendation(farmer_query, quality_score, defect_grade, spatial_matrix, local_market_name):
    """
    Synthesizes the complex spatial data into a simple, encouraging, actionable recommendation for the farmer.
    
    RULES:
    1. Speak directly to the farmer in clear, jargon-free prose.
    2. Name the single BEST market option explicitly and state the exact extra net profit (in ₹).
    3. Briefly mention WHY this market was selected.
    4. Keep the output under 4 sentences.
    """
    if not spatial_matrix:
        return "I'm sorry, I don't have enough market data to make a recommendation right now."
        
    best_market = spatial_matrix[0]
    
    # Find local market to compare
    local_market = next((m for m in spatial_matrix if m["market_name"].lower() == local_market_name.lower()), None)
    
    if not local_market or best_market["market_name"] == local_market["market_name"]:
        return (
            f"Hello! Based on the {quality_score*100:.0f}% quality score of your crop, selling locally at {local_market_name} is your best bet. "
            f"You stand to make a net profit of ₹{best_market['net_profit']}. "
            f"Other markets are too far and the transport costs would eat into your profits. "
            f"Good luck with your local sale!"
        )
        
    extra_profit = best_market["net_profit"] - local_market["net_profit"]
    
    # Generate the synthesis
    recommendation = (
        f"Hello! Based on the quality of your crop, I highly recommend taking your harvest to {best_market['market_name']}. "
        f"You will earn an extra ₹{extra_profit:.2f} in net profit compared to selling locally at {local_market_name}. "
        f"Even though it's a bit further, the higher market price there easily outweighs the ₹{best_market['logistics_cost']} transport cost. "
        f"Pack your crop carefully to avoid spoilage and have a safe, profitable trip!"
    )
    
    return recommendation

def generate_advisory(farmer_query, crop_quality_data, spatial_data, local_market_name):
    """
    Main entry point for the AI Agricultural Logistics & Advisory Agent.
    """
    matrix = calculate_spatial_arbitrage_matrix(
        usable_quantity=spatial_data['usable_quantity'],
        spoilage_decay_rate=spatial_data['spoilage_decay_rate'],
        transit_times=spatial_data['transit_times'],
        base_prices=spatial_data['base_prices'],
        quality_score=crop_quality_data['quality_score'],
        distances=spatial_data['distances'],
        fuel_rate=spatial_data['fuel_rate'],
        tolls=spatial_data['tolls'],
        wages=spatial_data['wages']
    )
    
    recommendation = synthesize_advisory_recommendation(
        farmer_query=farmer_query,
        quality_score=crop_quality_data['quality_score'],
        defect_grade=crop_quality_data['defect_grade'],
        spatial_matrix=matrix,
        local_market_name=local_market_name
    )
    
    return recommendation
