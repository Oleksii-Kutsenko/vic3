def calculate_target_debt_to_gdp(interest_rate, primary_surplus, gdp_growth_rate=None):
    """
    Calculate the target debt-to-GDP ratio based on the interest rate and fiscal factors.

    Parameters:
    interest_rate (float): The interest rate on the country's debt (as a decimal).
    primary_surplus (float): The primary surplus or deficit (negative if deficit).
    gdp_growth_rate (float, optional): The GDP growth rate (as a decimal). If not provided, defaults to 0.

    Returns:
    float: The target debt-to-GDP ratio.
    """
    if gdp_growth_rate is None:
        gdp_growth_rate = 0  # Default to 0 if growth rate isn't provided

    # Calculate the target debt-to-GDP ratio
    if interest_rate > gdp_growth_rate:
        target_debt_to_gdp = primary_surplus / (interest_rate - gdp_growth_rate)
        return target_debt_to_gdp
    else:
        return "Interest rate must be higher than GDP growth rate for sustainable debt."


INTEREST_RATE = 0.33
PRIMARY_SURPLUS = -3.88
GDP_GROWTH_RATE = 0

print(calculate_target_debt_to_gdp(INTEREST_RATE, PRIMARY_SURPLUS, GDP_GROWTH_RATE))
