import streamlit as st
import pandas as pd
import time

# Load the orders data from a CSV file
orders_df = pd.read_csv("orders.csv")

# Define the Streamlit app
def app():
    st.set_page_config(page_title="Pizza Ordering System", page_icon=":pizza:")
    st.markdown(
    """
    <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)


    # Add a title
    st.title("Pizza Ordering System")

    # Show the menu
    st.header("Menu")
    pizza_menu = {
        "Margherita": {"Small": 8, "Medium": 10, "Large": 12},
        "Pepperoni": {"Small": 10, "Medium": 12, "Large": 14},
        "Vegetarian": {"Small": 9, "Medium": 11, "Large": 13},
        "Hawaiian": {"Small": 11, "Medium": 13, "Large": 15},
    }
    selected_pizza = st.selectbox("Select a pizza", list(pizza_menu.keys()))
    selected_size = st.selectbox("Select a size", ["Small", "Medium", "Large"])
    toppings = st.multiselect("Select toppings (50 cents each)", ["Mushrooms", "Peppers", "Onions", "Olives"])
    cost = pizza_menu[selected_pizza][selected_size] + 0.5 * len(toppings)
    st.write("Cost:", "$", cost)

    # Take the customer's details
    st.header("Customer Details")
    order_id = str(int(time.time()))
    name = st.text_input("Name")
    phone_number = st.text_input("Phone number")
    Address = st.text_input("Address")
    st.write(f'Your Order ID is: {order_id}')

    # Place the order
    if st.button("Place Order"):
        # Add the order to the orders dataframe
        order = {
            "order_id": order_id,
            "Name": name,
            "Address":Address,
            "Phone": phone_number,
            "Pizza": selected_pizza,
            "Size": selected_size,
            "Toppings": toppings,
            "Quantity": 1,
            "Cost": cost,
            "Status": "Placed",
        }
        global orders_df
        orders_df = orders_df.append(order, ignore_index=True)
        orders_df.to_csv("orders.csv", index=False)
        st.success("Order placed successfully!")
    
    # Track the order status
    st.header("Track Order Status")
    order_id1 = st.text_input("Order ID")
    if st.button("Track"):
        order_found = False
        for i, order in orders_df.iterrows():
            if str(order['order_id']) == order_id1:
                order_found = True
                order_index = i
                st.write(f"Order ID:{order['order_id']}")
                st.write(f"Name: {order['Name']}")
                st.write(f"Phone: {order['Phone']}")
                st.write(f"Pizza: {order['Pizza']}")
                st.write(f"Size: {order['Size']}")
                st.write(f"Toppings: {list(map(str.strip, order['Toppings'].split(','))) if order['Toppings'] else 'None'}")
                st.write(f"Quantity: {order['Quantity']}")
                st.write(f"Cost: {order['Cost']}")
                st.write(f"Status: {order['Status']}")
                if order["Status"] == "Placed":
                    if st.button("Start Preparation"):
                        update_order_status(orders_df, order_index, "Preparation")
                elif order["Status"] == "Preparation":
                    if st.button("Out for delivery"):
                        update_order_status(orders_df, order_index, "Out for delivery")
                elif order["Status"] == "Out for delivery":
                    if st.button("Delivered"):
                        update_order_status(orders_df, order_index, "Delivered")
        if not order_found:
            st.warning("Order not found")
    # Show the orders
    st.header("Orders")
    st.dataframe(orders_df)

    # Accounting
    st.header("Accounting")
    total_revenue = orders_df["Cost"].sum()
    st.write("Total revenue:", "$", total_revenue)

    # CRM
    st.header("CRM")
    st.write("Customer list:")
    customer_list = orders_df["Name"].unique()
    st.write(customer_list)

    st.write("Order history by customer:")
    selected_customer = st.selectbox("Select a customer", customer_list)
    customer_orders = orders_df[orders_df["Name"] == selected_customer]
    st.dataframe(customer_orders)
if __name__ == "__main__":
    app()

