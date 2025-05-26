import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import time

# ========== CONSTANTS ==========
IMAGE_URL = "https://i.ibb.co/1YxH9ZSC/Offical-Logo-June-2024.jpg"

# ========== UTILITY FUNCTIONS ==========
def to_float_safe(val):
    try:
        return float(val) if val not in [None, ""] else 0.0
    except:
        return 0.0

def to_int_safe(val):
    try:
        return int(val) if val not in [None, ""] else 0
    except:
        return 0

# ========== FORM INPUTS ==========
def create_numeric_input(label, key, step=0.01):
    # Initialize with None to show empty field
    if key not in st.session_state:
        st.session_state[key] = None

    custom_placeholder = "Ignore fuel paid with Fuel Card" if key == "fuel_expense" else ""
    
    # Convert existing values to float (handles both None and string cases)
    current_value = float(st.session_state[key]) if st.session_state[key] not in [None, ""] else None
    
    try:
        value = st.number_input(
            label,
            key=f"input_{key}",
            value=current_value,
            min_value=0.0,
            max_value=10000.0,
            step=step,
            format="%f",
            placeholder=""
        )
        st.session_state[key] = value if value is not None else ""
        return value if value is not None else ""
    except Exception as e:
        st.error("Please enter a valid number between 0 and 10000")
        st.session_state[key] = ""
        return ""

# ========== IMAGE LOADING ==========
@st.cache_data
def load_image_with_retry(url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/webp,*/*"
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(
                f"{url}?cache={time.time()}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            if attempt == retries - 1:
                st.warning(f"Couldn't load image after {retries} attempts")
            time.sleep(1)
    
    return None

# ========== MAIN APP ==========
def main():
    # --- Header Section ---
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    
    img = load_image_with_retry(IMAGE_URL)
    if img:
        st.image(img, 
               use_container_width=True,
               output_format="auto")
    else:
        st.markdown("""
        <h1 style='text-align: center; color: #2a6fdb; 
                   font-family: Arial; margin-bottom: 20px;'>
            Shift Summary Calculator
        </h1>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # --- Main Form ---
    st.title("Shift Summary Calculator")

    # Initialize session state
    keys = [
        "fuel_expense", "car_wash", "live_eftpos", "net_amount", "tolls", "govt_levy",
        "booking_fee", "tips", "rank_hail_jobs", "dispatched_jobs", "card",
        "cabcharge", "app_pay", "subsidy", "paper_ttss", "account", "off_meter_jobs",
    ]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = ""

    with st.form("shift_summary_form"):
        # Create all numeric inputs
        fuel_expense = create_numeric_input("Fuel (ignore Fuel Card purchases)", "fuel_expense", 0.01)
        car_wash = create_numeric_input("Car Wash", "car_wash", 0.01)
        live_eftpos = create_numeric_input("Live EFTPOS", "live_eftpos", 0.01)
        net_amount = create_numeric_input("Net Amount", "net_amount", 0.01)
        tolls = create_numeric_input("Tolls", "tolls", 0.01)
        govt_levy = create_numeric_input("Govt Levy", "govt_levy", 0.01)
        booking_fee = create_numeric_input("Booking Fee", "booking_fee", 0.01)
        tips = create_numeric_input("Tips", "tips", 0.01)
        rank_hail_jobs = create_numeric_input("Rank/Hail Jobs", "rank_hail_jobs", 0.01)
        dispatched_jobs = create_numeric_input("Dispatched Jobs", "dispatched_jobs", 0.01)
        card = create_numeric_input("Card", "card", 0.01)
        cabcharge = create_numeric_input("Cabcharge", "cabcharge", 0.01)
        app_pay = create_numeric_input("App-Pay", "app_pay", 0.01)
        subsidy = create_numeric_input("Subsidy", "subsidy", 0.01)
        paper_ttss = create_numeric_input("Paper TTSS", "paper_ttss", 0.01)
        account = create_numeric_input("Account", "account", 0.01)
        off_meter_jobs = create_numeric_input("Off-meter Jobs", "off_meter_jobs", 0.01)

        submitted = st.form_submit_button("Submit")
        clear_all = st.form_submit_button("Clear All")

        if clear_all:
            for key in keys:
                st.session_state[key] = None
                st.session_state[f"input_{key}"] = None

        if submitted:
            # Convert inputs safely
            fe = to_float_safe(fuel_expense)
            carw = to_float_safe(car_wash)
            live_ep = to_float_safe(live_eftpos)
            net_amt = to_float_safe(net_amount)
            tolls_v = to_float_safe(tolls)
            govt_levy_v = to_float_safe(govt_levy)
            booking_fee_v = to_float_safe(booking_fee)
            tips_v = to_float_safe(tips)
            rank_hail = to_float_safe(rank_hail_jobs)
            dispatched = to_float_safe(dispatched_jobs)
            card_v = to_float_safe(card)
            cabcharge_v = to_float_safe(cabcharge)
            app_pay_v = to_float_safe(app_pay)
            subsidy_v = to_float_safe(subsidy)
            paper_ttss_v = to_float_safe(paper_ttss)
            account_v = to_float_safe(account)
            off_meter_v = to_float_safe(off_meter_jobs)



            # Calculations (example, adjust as needed)
            meter_totals = net_amt + tolls_v + govt_levy_v + booking_fee_v
            shift_totals = meter_totals + tips_v
            eftpos = live_ep + card_v
            subtotal1 = card_v + cabcharge_v + app_pay_v
            subtotal2 = subtotal1 + subsidy_v
            txn_totals = subtotal2 + account_v
            ttss_subsidy = subsidy_v + paper_ttss_v
            sub_total = txn_totals + paper_ttss_v + fe + live_ep
            gross_total = meter_totals
            correct_m7s = ttss_subsidy + account_v
            cash = meter_totals - txn_totals - govt_levy_v
            deduct_levy = (rank_hail + dispatched) * 1.32
            total1 = fe + carw + eftpos + paper_ttss_v + account_v
            less_comm45 = round(gross_takings * 0.45, 2)
            gross_takings = total1 + cash
            total2 = gross_takings - less_comm45
            total_pay_gst = total2 -total1 + govt_levy_v

                       # Display results using st.write()
            st.markdown("<h3 style='font-weight:bold; text-decoration:underline;'>Results</h3>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("<h4 style='font-weight:bold; text-decoration:underline;'>End of Shift Summary</h4>", unsafe_allow_html=True)
                st.write(f"**NET AMT:** ${net_amt:.2f}")
                st.write(f"**TOLLS:** ${tolls_v:.2f}")
                st.write(f"**GOVT LEVY:** ${govt_levy_v:.2f}")
                st.write(f"**BOOKING F:** ${booking_fee_v:.2f}")
                st.write("")  # Empty line
                st.write(f"**METER TOTALS:** ${meter_totals:.2f}")
                st.write(f"**TIPS:** ${tips_v:.2f}")
                st.write(f"**Shift Totals:** ${shift_totals:.2f}")
                st.write(f"**RANK/HAIL JOBS:** {rank_hail}")
                st.write(f"**DISPATCHED JOBS:** {dispatched}")
                st.write("")  # Empty line
                st.markdown("**TRANSACTION SUMMARY**")
                st.write(f"**CARD:** ${card_v:.2f}")
                st.write(f"**CABCHARGE:** ${cabcharge_v:.2f}")
                st.write(f"**APP-PAY:** ${app_pay_v:.2f}")
                st.write("")  # Empty line
                st.write(f"**SUBTOTAL1:** ${subtotal1:.2f}")
                st.write(f"**SUBSIDY:** ${subsidy_v:.2f}")
                st.write("")  # Empty line
                st.write(f"**SUBTOTAL2:** ${subtotal2:.2f}")
                st.write(f"**ACCOUNT:** ${account_v:.2f}")
                st.write("")  # Empty line
                st.write(f"**TXN TOTALS:** ${txn_totals:.2f}")

            with c2:
                st.markdown("<h4 style='font-weight:bold; text-decoration:underline;'>Pay-In</h4>", unsafe_allow_html=True)
                st.write(f"**Fuel:** ${fe:.2f}")
                st.write(f"**Car Wash:** ${carw:.2f}")
                st.write(f"**Correct M7s:** ${correct_m7s:.2f}")
                st.write(f"**Total(1):** ${total1:.2f}")
                st.write(f"**Cash:** ${cash:.2f}")
                st.write(f"**GROSS TAKINGS:** ${gross_takings:.2f}")
                st.write(f"**Commission 45%:** ${less_comm45:.2f}")    
                st.write(f"**Hire Charge 55%:** ${total2:.2f}")
                st.write(f"**-Total(1):** ${gross_total:.2f}")
                st.write(f"**+Levy:** ${govt_levy_v:.2f}")
                st.write(f"**TOTAL CASH PAY-IN:** ${total_pay_gst:.2f}")
                

if __name__ == "__main__":
    main()
