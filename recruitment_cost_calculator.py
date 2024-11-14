import streamlit as st
import requests

# Exchange rate API URL
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


# Fetch exchange rate from USD to EGP
def get_exchange_rate():
    try:
        response = requests.get(EXCHANGE_RATE_API_URL)
        data = response.json()
        return data["rates"]["EGP"]
    except Exception as e:
        st.warning("Could not fetch exchange rates. Defaulting to 1 USD = 15.7 EGP.")
        return 15.7  # Default exchange rate if API fails


# Get the latest USD to EGP exchange rate
usd_to_egp = get_exchange_rate()

# Streamlit app with tabs
st.title("Recruitment Cost Calculator")

# Currency selection with radio button at the top
currency = st.radio("Select Currency", ("USD", "EGP"))

# Create tabs
tab1, tab2 = st.tabs(["AI Screening Cost", "Human Recruiter Cost"])

# Tab 1: AI Screening Cost
with tab1:
    st.header("AI Screening Cost Calculator")

    # Input fields with sliders
    num_candidates = st.slider("Number of Candidates", min_value=1, max_value=50000, step=100, value=100)
    num_requests = st.slider("Number of Requests per Candidate", min_value=5, max_value=20, step=1, value=10)
    markup = st.slider("Markup Percentage", min_value=0, max_value=100, step=5, value=45)

    # Calculate AI cost
    cost_per_request = 0.008  # Cost per API request in USD
    base_cost_per_candidate = num_requests * cost_per_request
    final_cost_per_candidate = base_cost_per_candidate * (1 + markup / 100)
    total_cost_usd = final_cost_per_candidate * num_candidates

    # Convert to selected currency
    if currency == "EGP":
        final_cost_per_candidate *= usd_to_egp
        total_cost = total_cost_usd * usd_to_egp
    else:
        total_cost = total_cost_usd

    # Display results
    st.write(f"**Cost per Candidate (with {markup}% markup):** {final_cost_per_candidate:.2f} {currency}")
    st.write(f"**Total Cost for {num_candidates} Candidates:** {total_cost:.2f} {currency}")

# Tab 2: Human Recruiter Cost
with tab2:
    st.header("Human Recruiter Cost Calculator")

    # Input fields with sliders
    salary_egp = st.slider("Monthly Salary per Recruiter (in EGP)", min_value=5000, max_value=30000, step=1000,
                           value=12000)
    working_hours_per_day = st.slider("Working Hours per Day", min_value=1, max_value=12, step=1, value=8)
    team_size = st.slider("Number of Recruiters in the Team", min_value=1, max_value=20, step=1, value=5)
    processing_time_per_candidate = st.slider("Processing Time per Candidate (minutes)", min_value=1, max_value=30,
                                              step=1, value=5)

    # Calculate hourly wage in EGP
    workdays_per_month = 22  # Assuming 22 working days in a month
    total_monthly_hours = workdays_per_month * working_hours_per_day
    hourly_wage_egp = salary_egp / total_monthly_hours

    # Calculate cost per candidate
    processing_time_hours = processing_time_per_candidate / 60  # Convert minutes to hours
    cost_per_candidate_egp = hourly_wage_egp * processing_time_hours
    total_cost_egp = cost_per_candidate_egp * num_candidates * team_size

    # Convert costs to USD
    cost_per_candidate_usd = cost_per_candidate_egp / usd_to_egp
    total_cost_usd_recruiter = total_cost_egp / usd_to_egp

    # Display results in EGP and USD
    st.subheader("Cost Breakdown")
    st.write(f"**Hourly Wage per Recruiter:** {hourly_wage_egp:.2f} EGP ({hourly_wage_egp / usd_to_egp:.2f} USD)")
    st.write(f"**Cost per Candidate:** {cost_per_candidate_egp:.2f} EGP ({cost_per_candidate_usd:.2f} USD)")
    st.write(
        f"**Total Cost for {num_candidates} Candidates (for {team_size} Recruiters):** {total_cost_egp:.2f} EGP ({total_cost_usd_recruiter:.2f} USD)")
