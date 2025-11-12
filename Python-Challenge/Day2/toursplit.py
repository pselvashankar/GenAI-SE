import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TourSplit - Expense Manager",
    layout="wide",
    page_icon="🏖️",
)

# --- BEAUTIFUL STYLE ---
st.markdown("""
    <style>
    body {
        color: #223;
        background: #f8fbff;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #f8fbff 0%, #e4ecfa 100%);
    }
    .section-card {
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        box-shadow: 0 3px 16px 0 rgba(50,50,90,0.10), 0 1.5px 8px 0 rgba(150,150,200,0.13);
        padding: 15px 15px 10px 15px;
        margin-bottom: 5px;
        transition: box-shadow 0.23s;
    }
    h1, h3 {
        color: #222a38 !important;
        font-weight: 800;
        text-shadow: 0px 2px 12px rgba(200,220,255,0.11);
        margin: 0 !important;
        padding: 5px 0 !important;
    }
    h3 {
        font-size: 1.1rem !important;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
        background: #558cf6;
        color: #fff;
        border: none;
    }
    .stButton>button:hover {
        background: #355CAB;
        color: #ffe;
    }
    .stDataFrame, .stMarkdown {
        background: rgba(245,248,255,0.91);
        border-radius: 1rem;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- PAGE HEADER ---
st.markdown("""
<h1 style='text-align:center; margin-bottom:5px; margin-top:-50px; font-size:28px;'>🏖️ TourSplit <span style="font-weight:500;">- Expense Manager</span></h1>
<p style='text-align:center; font-size:14px; color:#385; margin-top:2px; margin-bottom:10px;'>Split expenses fairly with your travel buddies 💸</p>
""", unsafe_allow_html=True)

# --- APP STATE ---
if "friends" not in st.session_state:
    st.session_state.friends = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []

col1, col2, col3 = st.columns(3)

# --- FRIEND MANAGEMENT ---
with col1:
    st.markdown("<h3>👥 Create Your Group</h3>", unsafe_allow_html=True)
    name = st.text_input("Enter a friend's name", key="friend_input")
    add = st.button("➕ Add Friend")
    if add and name:
        if name not in st.session_state.friends:
            st.session_state.friends.append(name)
        else:
            st.warning(f"{name} already exists")
    elif add:
        st.error("Enter a valid name")
    if st.session_state.friends:
        st.markdown("**Friends in Group:**")
        st.markdown("<ul style='padding-left:20px'>" +
                    "".join([f"<li style='margin:0 0 3px 3px;'>{f}</li>" for f in st.session_state.friends]) +
                    "</ul>", unsafe_allow_html=True)
        if st.button("🧹 Reset Group"):
            st.session_state.friends.clear()
            st.session_state.expenses.clear()
            st.info("Group reset!")

# --- ADD EXPENSE ---
with col2:
    st.markdown("<h3>💰 Add a New Expense</h3>", unsafe_allow_html=True)
    if len(st.session_state.friends) < 2:
        st.info("Add at least two friends to start.")
    else:
        with st.form("add_expense", clear_on_submit=True):
            desc = st.text_input("Description", placeholder="e.g., Lunch, Tickets")
            amt = st.number_input("Amount (₹)", min_value=0.01, step=0.01)
            payer = st.selectbox("Paid by", st.session_state.friends)
            submitted = st.form_submit_button("Add Expense")
            if submitted:
                st.session_state.expenses.append({"description": desc, "amount": amt, "payer": payer})
                st.success(f"{payer} paid ₹{amt:.2f} for {desc}")

# --- SUMMARY ---
with col3:
    st.markdown("<h3>📊 Summary</h3>", unsafe_allow_html=True)
    if st.session_state.expenses:
            df = pd.DataFrame(st.session_state.expenses)
            st.markdown("**Expense History:**")
            st.dataframe(df, use_container_width=True, hide_index=True)
            # Calculate balances
            balances = {f: 0.0 for f in st.session_state.friends}
            n = len(st.session_state.friends)
            for exp in st.session_state.expenses:
                share = exp["amount"] / n
                for f in balances:
                    balances[f] -= share
                balances[exp["payer"]] += exp["amount"]
            st.markdown("**Current Balances:**")
            bal_df = pd.DataFrame(list(balances.items()), columns=["Friend", "Balance (₹)"])
            st.dataframe(bal_df, use_container_width=True, hide_index=True)

            # Settlement logic
            creditors = [{"name": f, "amount": b} for f, b in balances.items() if b > 0.01]
            debtors = [{"name": f, "amount": -b} for f, b in balances.items() if b < -0.01]
            transactions = []
            while debtors and creditors:
                debtors.sort(key=lambda x: -x["amount"])
                creditors.sort(key=lambda x: -x["amount"])
                d = debtors[0]
                c = creditors[0]
                payment = min(d["amount"], c["amount"])
                transactions.append({"from": d["name"], "to": c["name"], "amount": round(payment, 2)})
                d["amount"] -= payment
                c["amount"] -= payment
                if d["amount"] < 0.01: debtors.pop(0)
                if c["amount"] < 0.01: creditors.pop(0)
            st.markdown("**Settle Up:**")
            if transactions:
                for t in transactions:
                    st.markdown(f"💸 <b>{t['from']}</b> → <b>{t['to']}</b> ₹{t['amount']:.2f}", unsafe_allow_html=True)
            else:
                st.info("Everyone is settled up! 🎉")
            if st.button("🗑️ Clear Expenses"):
                st.session_state.expenses.clear()
                st.success("Expenses cleared!")
    else:
        st.info("No expenses yet.")
