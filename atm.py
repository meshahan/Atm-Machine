import streamlit as st
import datetime

# Sample data to simulate user accounts and bank balances
accounts = {
    '2024': {'password': '123456', 'balance': 500000.00, 'transactions': []}
}

def print_statement(transactions):
    total_amount = sum(transaction['amount'] for transaction in transactions)
    st.write('<div class="statement">Transaction Statement (in PKR):</div>', unsafe_allow_html=True)
    for transaction in transactions:
        amount = f"PKR {transaction['amount']:.2f}"
        st.write(f'<div class="transaction">{transaction["date"]} - {transaction["type"]}: {amount}</div>', unsafe_allow_html=True)
    st.write(f'<div class="statement">Print successfully! The total amount is: PKR {total_amount:.2f}</div>', unsafe_allow_html=True)

def atm_operations(account_id):
    user_account = accounts[account_id]
    transactions = user_account['transactions']
    
    option = st.selectbox("Select an option:", ("Balance Inquiry", "Withdrawal", "Deposit", "Transfer", "Exit"))

    if option == "Balance Inquiry":
        st.write(f'<div class="balance">Your current balance is: PKR {user_account["balance"]:.2f}</div>', unsafe_allow_html=True)

    elif option == "Withdrawal":
        withdrawal_amount = st.number_input("Enter the amount to withdraw (in PKR):", min_value=0.00, step=0.01)
        if st.button("Withdraw"):
            if withdrawal_amount <= user_account['balance']:
                user_account['balance'] -= withdrawal_amount
                transactions.append({'type': 'Withdrawal', 'amount': withdrawal_amount, 'date': str(datetime.date.today())})
                st.write(f'<div class="transaction">Withdrawal successful! Your new balance is: PKR {user_account["balance"]:.2f}</div>', unsafe_allow_html=True)
            else:
                st.write('<div class="error">Insufficient funds!</div>', unsafe_allow_html=True)

    elif option == "Deposit":
        deposit_amount = st.number_input("Enter the amount to deposit (in PKR):", min_value=0.00, step=0.01)
        if st.button("Deposit"):
            user_account['balance'] += deposit_amount
            transactions.append({'type': 'Deposit', 'amount': deposit_amount, 'date': str(datetime.date.today())})
            st.write(f'<div class="transaction">Deposit successful! Your new balance is: PKR {user_account["balance"]:.2f}</div>', unsafe_allow_html=True)

    elif option == "Transfer":
        transfer_amount = st.number_input("Enter the amount to transfer (in PKR):", min_value=0.00, step=0.01)
        iban = st.text_input("Enter beneficiary's IBAN number:")
        bank_details = st.text_input("Enter beneficiary's bank details:")
        
        if st.button("Transfer"):
            if transfer_amount <= user_account['balance'] and iban and bank_details:
                user_account['balance'] -= transfer_amount
                transactions.append({
                    'type': 'Transfer', 
                    'amount': transfer_amount, 
                    'date': str(datetime.date.today()),
                    'iban': iban,
                    'bank_details': bank_details
                })
                st.write(f'<div class="transaction">Transfer successful to IBAN {iban} at {bank_details}! Your new balance is: PKR {user_account["balance"]:.2f}</div>', unsafe_allow_html=True)
            else:
                st.write('<div class="error">Transfer failed. Please check your balance and provide valid IBAN and bank details.</div>', unsafe_allow_html=True)

    elif option == "Exit":
        st.write('<div class="exit">Thank you for using the ATM. You have successfully logged out.</div>', unsafe_allow_html=True)
        st.session_state.logged_in = False

    # Display current date and time at the bottom
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f'<div class="date-time">Current Date and Time: {current_time}</div>', unsafe_allow_html=True)

def main():
    st.title("ATM Machine")

    # Custom CSS
    st.markdown("""
        <style>
        .statement {
            background-color: green;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
        }
        .transaction {
            background-color: green;
            color: white;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
        }
        .balance {
            background-color: green;
            color: white;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
        }
        .error {
            background-color: red;
            color: white;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
        }
        .date-time {
            background-color: pink;
            color: black;
            font-weight: bold;
            padding: 5px;
            border-radius: 5px;
            text-align: center;
            margin-top: 20px;
        }
        .exit {
            background-color: lightgray;
            color: black;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_id = None

    if not st.session_state.logged_in:
        # User ID and Password authentication
        user_id = st.text_input("Enter your User ID:")
        password = st.text_input("Enter your Password:", type="password")
        
        if st.button("Login"):
            if user_id in accounts and accounts[user_id]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.success("Login successful!")
            else:
                st.error("Invalid User ID or Password.")
    else:
        atm_operations(st.session_state.user_id)

if __name__ == "__main__":
    main()
