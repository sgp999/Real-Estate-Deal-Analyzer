import streamlit as st

import requests


def get_schools(zip_code: str):
    app_id = st.secrets.get("SCHOOLDIGGER_APP_ID", "")
    app_key = st.secrets.get("SCHOOLDIGGER_APP_KEY", "")

    if not app_id or not app_key:
        return [
            {
                "name": "API keys missing",
                "rating": "N/A",
                "distance": "N/A",
            }
        ]

    url = "https://api.schooldigger.com/v2.0/autocomplete/schools"
    params = {
        "st": "OH",
        "q": zip_code,
        "appID": app_id,
        "appKey": app_key,
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        schools = []
        for item in data.get("schoolMatches", [])[:3]:
            school = item.get("school", {})
            schools.append(
                {
                    "name": school.get("schoolName", "Unknown School"),
                    "rating": str(school.get("rankHistory", [{}])[0].get("rankStars", "N/A")) + "/5",
                    "distance": school.get("city", "N/A"),
                }
            )

        if not schools:
            return [
                {
                    "name": "No schools found",
                    "rating": "N/A",
                    "distance": "N/A",
                }
            ]

        return schools

    except Exception:
        return [
            {
                "name": "Could not load school data",
                "rating": "N/A",
                "distance": "N/A",
            }
        ]

st.set_page_config(page_title="REAL-ESTATE-DEAL-ANALYZER", layout="wide")

# Remove top spacing + header
st.markdown(
    """
    <style>
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_schools(zip_code: str):
    return [
        {"name": "Lincoln Elementary", "rating": "8/10", "distance": "1.2 mi"},
        {"name": "Roberts Middle School", "rating": "7/10", "distance": "2.1 mi"},
        {"name": "Cuyahoga Falls High School", "rating": "7/10", "distance": "2.8 mi"},
    ]


def calculate_monthly_payment(loan_amount: float, annual_rate: float, years: int) -> float:
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12

    if loan_amount <= 0:
        return 0.0

    if monthly_rate == 0:
        return loan_amount / num_payments

    return loan_amount * (
        monthly_rate * (1 + monthly_rate) ** num_payments
    ) / ((1 + monthly_rate) ** num_payments - 1)


# Title
st.markdown(
    """
    <h1 style="margin-top:0;">REAL-ESTATE-DEAL-ANALYZER</h1>
    """,
    unsafe_allow_html=True,
)

st.write("Analyze a deal and view school data for the area.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Property / Deal Inputs")

    zip_code = st.text_input("ZIP Code")

    purchase_price = st.number_input(
        "Purchase Price", min_value=0.0, value=300000.0, step=1000.0
    )
    down_payment = st.number_input(
        "Down Payment", min_value=0.0, value=60000.0, step=1000.0
    )
    interest_rate = st.number_input(
        "Interest Rate (%)", min_value=0.0, value=6.5, step=0.1
    )
    loan_term = st.selectbox("Loan Term (Years)", [15, 20, 30], index=2)

    annual_taxes = st.number_input(
        "Annual Property Taxes", min_value=0.0, value=3600.0, step=100.0
    )
    annual_insurance = st.number_input(
        "Annual Insurance", min_value=0.0, value=1200.0, step=100.0
    )
    monthly_pmi = st.number_input(
        "Monthly PMI", min_value=0.0, value=150.0, step=10.0
    )
    monthly_rent = st.number_input(
        "Expected Monthly Rent", min_value=0.0, value=2500.0, step=50.0
    )
    monthly_repairs = st.number_input(
        "Monthly Repairs / Maintenance", min_value=0.0, value=150.0, step=10.0
    )
    monthly_other = st.number_input(
        "Other Monthly Expenses", min_value=0.0, value=100.0, step=10.0
    )

    analyze = st.button("Analyze Deal")

with col2:
    st.subheader("Schools in This Area")

    if zip_code:
        schools = get_schools(zip_code)

        for school in schools:
            st.markdown(
                f"""
<div style="font-size:13px; padding:6px; border:1px solid #eee; border-radius:6px; margin-bottom:6px;">
<b>{school['name']}</b><br>
⭐ {school['rating']} &nbsp;&nbsp; 📍 {school['distance']}
</div>
""",
                unsafe_allow_html=True,
            )
    else:
        st.info("Enter ZIP code to see nearby schools.")


if analyze:
    loan_amount = purchase_price - down_payment

    monthly_mortgage = calculate_monthly_payment(
        loan_amount, interest_rate, loan_term
    )

    monthly_taxes = annual_taxes / 12
    monthly_insurance = annual_insurance / 12

    total_monthly_expenses = (
        monthly_mortgage
        + monthly_taxes
        + monthly_insurance
        + monthly_pmi
        + monthly_repairs
        + monthly_other
    )

    monthly_cash_flow = monthly_rent - total_monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12

    total_cash_invested = down_payment

    if total_cash_invested > 0:
        cash_on_cash_roi = (annual_cash_flow / total_cash_invested) * 100
    else:
        cash_on_cash_roi = 0.0

    st.divider()
    st.subheader("Deal Summary")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Loan Amount", f"${loan_amount:,.2f}")
        st.metric("Monthly Mortgage", f"${monthly_mortgage:,.2f}")
        st.metric("Monthly Taxes", f"${monthly_taxes:,.2f}")

    with col_b:
        st.metric("Monthly Insurance", f"${monthly_insurance:,.2f}")
        st.metric("Total Expenses", f"${total_monthly_expenses:,.2f}")
        st.metric("Monthly Rent", f"${monthly_rent:,.2f}")

    with col_c:
        st.metric("Cash Flow", f"${monthly_cash_flow:,.2f}")
        st.metric("Annual Cash Flow", f"${annual_cash_flow:,.2f}")
        st.metric("ROI", f"{cash_on_cash_roi:.2f}%")

    st.subheader("Expense Breakdown")
    st.write(f"Mortgage: ${monthly_mortgage:,.2f}")
    st.write(f"Taxes: ${monthly_taxes:,.2f}")
    st.write(f"Insurance: ${monthly_insurance:,.2f}")
    st.write(f"PMI: ${monthly_pmi:,.2f}")
    st.write(f"Repairs: ${monthly_repairs:,.2f}")
    st.write(f"Other: ${monthly_other:,.2f}")