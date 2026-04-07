from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from app.calculators import analyze_deal

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Real Estate Deal Analyzer is running"}


@app.get("/real-estate-ui", response_class=HTMLResponse)
def ui():
    return """
    <html>
        <head>
            <title>Real Estate Deal Analyzer</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    color: #1f2937;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    max-width: 1050px;
                    margin: 40px auto;
                    background: white;
                    border-radius: 14px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                    overflow: hidden;
                }
                .header {
                    background: linear-gradient(135deg, #16324f, #1f5b8f);
                    color: white;
                    padding: 32px;
                }
                .header h1 {
                    margin: 0 0 8px 0;
                    font-size: 32px;
                }
                .header p {
                    margin: 0;
                    opacity: 0.95;
                }
                .content {
                    padding: 32px;
                }
                .grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 18px;
                }
                .field {
                    margin-bottom: 16px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                }
                input {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #d1d5db;
                    border-radius: 8px;
                    box-sizing: border-box;
                }
                .section-title {
                    margin-top: 28px;
                    margin-bottom: 16px;
                    font-size: 20px;
                    color: #16324f;
                }
                button {
                    background: #1f5b8f;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 14px 22px;
                    font-size: 16px;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover {
                    background: #16324f;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Real Estate Deal Analyzer</h1>
                    <p>Enter property and financing details to evaluate a rental deal.</p>
                </div>
                <div class="content">
                    <form action="/analyze-deal" method="post">
                        <div class="section-title">Property Details</div>
                        <div class="grid">
                            <div class="field">
                                <label>Property Address</label>
                                <input type="text" name="property_address" placeholder="123 Main St, Akron, OH">
                            </div>
                            <div class="field">
                                <label>Purchase Price</label>
                                <input type="number" step="0.01" name="purchase_price" required>
                            </div>
                            <div class="field">
                                <label>Monthly Rent</label>
                                <input type="number" step="0.01" name="monthly_rent" required>
                            </div>
                            <div class="field">
                                <label>Closing Costs</label>
                                <input type="number" step="0.01" name="closing_costs" value="0">
                            </div>
                        </div>

                        <div class="section-title">Financing</div>
                        <div class="grid">
                            <div class="field">
                                <label>Down Payment %</label>
                                <input type="number" step="0.01" name="down_payment_percent" value="20" required>
                            </div>
                            <div class="field">
                                <label>Interest Rate %</label>
                                <input type="number" step="0.01" name="interest_rate" value="7" required>
                            </div>
                            <div class="field">
                                <label>Loan Term (Years)</label>
                                <input type="number" name="loan_term_years" value="30" required>
                            </div>
                        </div>

                        <div class="section-title">Expenses</div>
                        <div class="grid">
                            <div class="field">
                                <label>Annual Property Taxes</label>
                                <input type="number" step="0.01" name="annual_property_taxes" value="0" required>
                            </div>
                            <div class="field">
                                <label>Annual Insurance</label>
                                <input type="number" step="0.01" name="annual_insurance" value="0" required>
                            </div>
                            <div class="field">
                                <label>Monthly HOA</label>
                                <input type="number" step="0.01" name="monthly_hoa" value="0" required>
                            </div>
                            <div class="field">
                                <label>Monthly Maintenance</label>
                                <input type="number" step="0.01" name="monthly_maintenance" value="0" required>
                            </div>
                            <div class="field">
                                <label>Vacancy %</label>
                                <input type="number" step="0.01" name="vacancy_percent" value="5" required>
                            </div>
                            <div class="field">
                                <label>Property Management %</label>
                                <input type="number" step="0.01" name="property_management_percent" value="8" required>
                            </div>
                        </div>

                        <button type="submit">Analyze Deal</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """


@app.post("/analyze-deal", response_class=HTMLResponse)
def analyze_deal_route(
    property_address: str = Form(""),
    purchase_price: float = Form(...),
    down_payment_percent: float = Form(...),
    interest_rate: float = Form(...),
    loan_term_years: int = Form(...),
    monthly_rent: float = Form(...),
    annual_property_taxes: float = Form(...),
    annual_insurance: float = Form(...),
    monthly_hoa: float = Form(...),
    monthly_maintenance: float = Form(...),
    vacancy_percent: float = Form(...),
    property_management_percent: float = Form(...),
    closing_costs: float = Form(...),
):
    result = analyze_deal(
        purchase_price=purchase_price,
        down_payment_percent=down_payment_percent,
        interest_rate=interest_rate,
        loan_term_years=loan_term_years,
        monthly_rent=monthly_rent,
        annual_property_taxes=annual_property_taxes,
        annual_insurance=annual_insurance,
        monthly_hoa=monthly_hoa,
        monthly_maintenance=monthly_maintenance,
        vacancy_percent=vacancy_percent,
        property_management_percent=property_management_percent,
        closing_costs=closing_costs,
    )

    rating_color = "#15803d" if result["rating"] == "Strong deal" else "#b45309" if result["rating"] == "Average deal" else "#b91c1c"

    def money(value: float) -> str:
        return f"${value:,.2f}"

    def percent(value: float) -> str:
        return f"{value:.2f}%"

    return f"""
    <html>
        <head>
            <title>Deal Analysis Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    color: #1f2937;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 1100px;
                    margin: 30px auto;
                    background: white;
                    border-radius: 14px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #16324f, #1f5b8f);
                    color: white;
                    padding: 28px 32px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 30px;
                }}
                .sub {{
                    margin-top: 8px;
                    opacity: 0.95;
                }}
                .content {{
                    padding: 28px 32px 40px 32px;
                }}
                .verdict {{
                    border-left: 6px solid {rating_color};
                    background: #f8fafc;
                    border-radius: 10px;
                    padding: 18px;
                    margin-bottom: 24px;
                }}
                .cards {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 16px;
                    margin-bottom: 28px;
                }}
                .card {{
                    background: #f8fafc;
                    border: 1px solid #dbe4ee;
                    border-radius: 12px;
                    padding: 18px;
                }}
                .card-title {{
                    font-size: 14px;
                    color: #64748b;
                    margin-bottom: 8px;
                }}
                .card-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #16324f;
                }}
                h2 {{
                    margin-top: 30px;
                    margin-bottom: 12px;
                    font-size: 20px;
                    color: #16324f;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 24px;
                }}
                th, td {{
                    border: 1px solid #dbe4ee;
                    padding: 10px 12px;
                    text-align: left;
                }}
                th {{
                    background: #eef4fa;
                    width: 40%;
                }}
                .back-link {{
                    display: inline-block;
                    margin-top: 12px;
                    text-decoration: none;
                    color: #1f5b8f;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Deal Analysis Results</h1>
                    <div class="sub">{property_address or "Property address not provided"}</div>
                </div>

                <div class="content">
                    <div class="verdict">
                        <strong>Deal Rating:</strong> {result["rating"]}
                    </div>

                    <div class="cards">
                        <div class="card">
                            <div class="card-title">Monthly Cash Flow</div>
                            <div class="card-value">{money(result["monthly_cash_flow"])}</div>
                        </div>
                        <div class="card">
                            <div class="card-title">Cap Rate</div>
                            <div class="card-value">{percent(result["cap_rate"])}</div>
                        </div>
                        <div class="card">
                            <div class="card-title">Cash-on-Cash Return</div>
                            <div class="card-value">{percent(result["cash_on_cash"])}</div>
                        </div>
                    </div>

                    <h2>Financing</h2>
                    <table>
                        <tr><th>Purchase Price</th><td>{money(result["purchase_price"])}</td></tr>
                        <tr><th>Down Payment</th><td>{money(result["down_payment_amount"])}</td></tr>
                        <tr><th>Loan Amount</th><td>{money(result["loan_amount"])}</td></tr>
                        <tr><th>Monthly Mortgage Payment</th><td>{money(result["monthly_mortgage_payment"])}</td></tr>
                        <tr><th>Cash Invested</th><td>{money(result["cash_invested"])}</td></tr>
                    </table>

                    <h2>Monthly Expense Breakdown</h2>
                    <table>
                        <tr><th>Monthly Taxes</th><td>{money(result["monthly_taxes"])}</td></tr>
                        <tr><th>Monthly Insurance</th><td>{money(result["monthly_insurance"])}</td></tr>
                        <tr><th>Monthly HOA</th><td>{money(result["monthly_hoa"])}</td></tr>
                        <tr><th>Monthly Maintenance</th><td>{money(result["monthly_maintenance"])}</td></tr>
                        <tr><th>Vacancy Cost</th><td>{money(result["vacancy_cost"])}</td></tr>
                        <tr><th>Management Cost</th><td>{money(result["management_cost"])}</td></tr>
                        <tr><th>Total Monthly Expenses</th><td>{money(result["total_monthly_expenses"])}</td></tr>
                    </table>

                    <h2>Performance</h2>
                    <table>
                        <tr><th>Monthly Cash Flow</th><td>{money(result["monthly_cash_flow"])}</td></tr>
                        <tr><th>Annual Cash Flow</th><td>{money(result["annual_cash_flow"])}</td></tr>
                        <tr><th>NOI</th><td>{money(result["noi"])}</td></tr>
                        <tr><th>Cap Rate</th><td>{percent(result["cap_rate"])}</td></tr>
                        <tr><th>Cash-on-Cash Return</th><td>{percent(result["cash_on_cash"])}</td></tr>
                    </table>

                    <a class="back-link" href="/real-estate-ui">← Analyze another property</a>
                </div>
            </div>
        </body>
    </html>
    """