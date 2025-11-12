import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TourSplit - Expense Manager",
    layout="wide",
    page_icon="🏖️",
)

# --- STYLING ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #f8fbff 0%, #e4ecfa 100%);
        padding-top: 0rem;
    }
    section.main > div {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 1200px;
        margin: auto;
    }
    h1, h3 {
        color: #222a38 !important;
        font-weight: 800;
        margin: 0 !important;
    }
    h1 {
        text-align: center;
        font-size: 26px !important;
    }
    h3 {
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 700;
        background: #558cf6;
        color: #fff;
        border: none;
        padding: 0.4rem 0.8rem;
    }
    .stButton>button:hover {
        background: #355CAB;
    }
    .stDataFrame, .stMarkdown {
        border-radius: 0.6rem;
        padding: 0.4rem 0.6rem;
    }
    ul {
        margin: 0;
        padding-left: 16px;
    }
    hr {
        margin: 0.6rem 0;
        border: none;
        border-top: 1px solid #ccd;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<h1>🏖️ TourSplit - Expense Manager</h1>
<p style='text-align:center; font-size:13px; color:#385; margin-top:-6px;'>
Split expenses fairly with your travel buddies 💸
</p>
""", unsafe_allow_html=True)

# --- APP STATE ---
if "friends" not in st.session_state:
    st.session_state.friends = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --- 3 COLUMN LAYOUT ---
col1, col2, col3 = st.columns([1.1, 1.1, 1.3])

# --- FRIEND MANAGEMENT ---
with col1:
    st.markdown("<h3>👥 Create Your Group</h3>", unsafe_allow_html=True)
    name = st.text_input("Friend's name", key="friend_input", label_visibility="collapsed", placeholder="Enter friend's name")
    add = st.button("➕ Add Friend", use_container_width=True)
    if add and name:
        if name not in st.session_state.friends:
            st.session_state.friends.append(name)
        else:
            st.warning(f"{name} already exists")
    elif add:
        st.error("Enter a valid name")

    if st.session_state.friends:
        st.markdown("**Friends:**")
        st.markdown("<ul>" +
                    "".join([f"<li>{f}</li>" for f in st.session_state.friends]) +
                    "</ul>", unsafe_allow_html=True)
        if st.button("🧹 Reset Group", use_container_width=True):
            st.session_state.friends.clear()
            st.session_state.expenses.clear()
            st.info("Group reset!")

# --- ADD EXPENSE ---
with col2:
    st.markdown("<h3>💰 Add Expense</h3>", unsafe_allow_html=True)
    if len(st.session_state.friends) < 2:
        st.info("Add at least two friends.")
    else:
        with st.form("add_expense", clear_on_submit=True):
            desc = st.text_input("Description", placeholder="e.g., Lunch, Tickets")
            amt = st.number_input("Amount (₹)", min_value=0.01, step=0.01)
            payer = st.selectbox("Paid by", st.session_state.friends)
            submitted = st.form_submit_button("Add Expense")
            if submitted:
                st.session_state.expenses.append({"description": desc, "amount": amt, "payer": payer})
                st.success(f"{payer} paid ₹{amt:.2f} for {desc}")

# --- SUMMARY + SETTLE UP ---
with col3:
    st.markdown("<h3>📊 Summary</h3>", unsafe_allow_html=True)
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.markdown("**Expense History:**")
        st.dataframe(df, use_container_width=True, hide_index=True, height=150)

        # Balances
        balances = {f: 0.0 for f in st.session_state.friends}
        n = len(st.session_state.friends)
        for exp in st.session_state.expenses:
            share = exp["amount"] / n
            for f in balances:
                balances[f] -= share
            balances[exp["payer"]] += exp["amount"]

        st.markdown("**Balances:**")
        bal_df = pd.DataFrame(list(balances.items()), columns=["Friend", "Balance (₹)"])
        st.dataframe(bal_df, use_container_width=True, hide_index=True, height=120)

        # Divider before Settle Up
        st.markdown("<hr>", unsafe_allow_html=True)

        # Settlement
        st.markdown("<h3>🤝 Settle Up</h3>", unsafe_allow_html=True)
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

        if transactions:
            for t in transactions:
                st.markdown(f"💸 <b>{t['from']}</b> → <b>{t['to']}</b> ₹{t['amount']:.2f}", unsafe_allow_html=True)
        else:
            st.info("Everyone is settled up! 🎉")

        if st.button("🗑️ Clear Expenses", use_container_width=True):
            st.session_state.expenses.clear()
            st.success("Expenses cleared!")
    else:
        st.info("No expenses yet.")
