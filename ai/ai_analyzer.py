def analyze_product(ingredients, allergens, nutrition, user_profile):
    risk_score = 100
    reasons = []

    user_allergies = user_profile.get("allergies", [])
    conditions = user_profile.get("conditions", [])

    ingredients_lower = ingredients.lower()
    allergens_lower = allergens.lower()
    nutrition_lower = nutrition.lower()

    # Allergy check
    for allergy in user_allergies:
        if allergy.lower() in ingredients_lower or allergy.lower() in allergens_lower:
            risk_score -= 40
            reasons.append(f"Contains {allergy}, which you are allergic to.")

    # Diabetes check
    if "diabetes" in conditions and "sugar" in ingredients_lower:
        risk_score -= 25
        reasons.append("High sugar content is risky for diabetes.")

    # BP / Hypertension
    if "bp" in conditions or "hypertension" in conditions:
        if "sodium" in ingredients_lower or "salt" in ingredients_lower:
            risk_score -= 20
            reasons.append("High salt content is risky for blood pressure.")

    # Cholesterol
    if "cholesterol" in conditions:
        if "palm oil" in ingredients_lower or "trans fat" in nutrition_lower:
            risk_score -= 20
            reasons.append("Unhealthy fats may increase cholesterol.")

    # Final decision
    if risk_score >= 75:
        status = "🟢 Safe"
    elif risk_score >= 50:
        status = "🟡 Moderate Risk"
    else:
        status = "🔴 Unsafe"

    return status, risk_score, reasons
