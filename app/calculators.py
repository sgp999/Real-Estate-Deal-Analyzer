from math import pow


def monthly_mortgage_payment(
    purchase_price: float,
    down_payment_percent: float,
    interest_rate: float,
    loan_term_years: int,
) -> tuple[float, float]:
    down_payment_amount = purchase_price * (down_payment_percent / 100)
    loan_amount = purchase_price - down_payment_amount

    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term_years * 12

    if monthly_rate == 0:
        payment = loan_amount / num_payments if num_payments else 0
    else:
        payment = loan_amount * (
            monthly_rate * pow(1 + monthly_rate, num_payments)
        ) / (pow(1 + monthly_rate, num_payments) - 1)

    return payment, loan_amount


def analyze_deal(
    purchase_price: float,
    down_payment_percent: float,
    interest_rate: float,
    loan_term_years: int,
    monthly_rent: float,
    annual_property_taxes: float,
    annual_insurance: float,
    monthly_hoa: float,
    monthly_maintenance: float,
    vacancy_percent: float,
    property_management_percent: float,
    closing_costs: float,
) -> dict:
    mortgage_payment, loan_amount = monthly_mortgage_payment(
        purchase_price,
        down_payment_percent,
        interest_rate,
        loan_term_years,
    )

    monthly_taxes = annual_property_taxes / 12
    monthly_insurance = annual_insurance / 12
    vacancy_cost = monthly_rent * (vacancy_percent / 100)
    management_cost = monthly_rent * (property_management_percent / 100)

    total_monthly_expenses = (
        mortgage_payment
        + monthly_taxes
        + monthly_insurance
        + monthly_hoa
        + monthly_maintenance
        + vacancy_cost
        + management_cost
    )

    monthly_cash_flow = monthly_rent - total_monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12

    operating_expenses_monthly = (
        monthly_taxes
        + monthly_insurance
        + monthly_hoa
        + monthly_maintenance
        + vacancy_cost
        + management_cost
    )

    noi = (monthly_rent * 12) - (operating_expenses_monthly * 12)
    cap_rate = (noi / purchase_price * 100) if purchase_price else 0

    down_payment_amount = purchase_price * (down_payment_percent / 100)
    cash_invested = down_payment_amount + closing_costs
    cash_on_cash = (annual_cash_flow / cash_invested * 100) if cash_invested else 0

    rating = deal_rating(monthly_cash_flow, cap_rate, cash_on_cash)

    return {
        "purchase_price": round(purchase_price, 2),
        "down_payment_amount": round(down_payment_amount, 2),
        "loan_amount": round(loan_amount, 2),
        "monthly_mortgage_payment": round(mortgage_payment, 2),
        "monthly_taxes": round(monthly_taxes, 2),
        "monthly_insurance": round(monthly_insurance, 2),
        "monthly_hoa": round(monthly_hoa, 2),
        "monthly_maintenance": round(monthly_maintenance, 2),
        "vacancy_cost": round(vacancy_cost, 2),
        "management_cost": round(management_cost, 2),
        "total_monthly_expenses": round(total_monthly_expenses, 2),
        "monthly_cash_flow": round(monthly_cash_flow, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "noi": round(noi, 2),
        "cap_rate": round(cap_rate, 2),
        "cash_invested": round(cash_invested, 2),
        "cash_on_cash": round(cash_on_cash, 2),
        "rating": rating,
    }


def deal_rating(monthly_cash_flow: float, cap_rate: float, cash_on_cash: float) -> str:
    score = 0

    if monthly_cash_flow > 200:
        score += 2
    elif monthly_cash_flow > 0:
        score += 1

    if cap_rate >= 8:
        score += 2
    elif cap_rate >= 6:
        score += 1

    if cash_on_cash >= 10:
        score += 2
    elif cash_on_cash >= 6:
        score += 1

    if score >= 5:
        return "Strong deal"
    if score >= 3:
        return "Average deal"
    return "Weak deal"