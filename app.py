# import sqlite3
# from pathlib import Path
# from urllib.parse import quote
# import streamlit as st

# st.set_page_config(
#     page_title="Mukesh Fastfood Shop",
#     page_icon="🍔",
#     layout="wide"
# )

# # Admin Password
# ADMIN_PASSWORD = "mukesh@fastfood"

# # Load CSS design
# def load_css():
#     css_file = Path("style.css")
#     if css_file.exists():
#         st.markdown(
#             f"<style>{css_file.read_text(encoding='utf-8')}</style>",
#             unsafe_allow_html=True
#         )

# load_css()

# # Shop WhatsApp number
# SHOP_WHATSAPP = "918683868939"

# # Default food images
# DEFAULT_FOOD_IMAGES = {
#     "Burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600",
#     "Noodles": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600",
#     "Pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
#     "Patties": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",
#     "Momos": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600",
#     "Simple Samosa": "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=600",
#     "chola Samosa": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",
# }

# # Database connection
# conn = sqlite3.connect("fastfood.db", check_same_thread=False)
# cursor = conn.cursor()

# # Menu table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS menu (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE NOT NULL,
#     price REAL NOT NULL,
#     image_url TEXT,
#     available INTEGER DEFAULT 1
# )
# """)

# # Settings table (Shop Open/Closed state)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS settings (
#     key TEXT PRIMARY KEY,
#     value TEXT NOT NULL
# )
# """)

# # Default shop status = Open (1)
# cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('is_shop_open', '1')")
# conn.commit()

# # Ensure image_url column exists
# try:
#     cursor.execute("ALTER TABLE menu ADD COLUMN image_url TEXT")
#     conn.commit()
# except sqlite3.OperationalError:
#     pass

# # Default items data
# default_items = [
#     ("Burger", 25, DEFAULT_FOOD_IMAGES["Burger"]),
#     ("Noodles", 20, DEFAULT_FOOD_IMAGES["Noodles"]),
#     ("Pizza", 100, DEFAULT_FOOD_IMAGES["Pizza"]),
#     ("Patties", 25, DEFAULT_FOOD_IMAGES["Patties"]),
#     ("Momos", 50, DEFAULT_FOOD_IMAGES["Momos"]),
#     ("Simple Samosa", 20, DEFAULT_FOOD_IMAGES["Simple Samosa"]),
#     ("chola Samosa", 25, DEFAULT_FOOD_IMAGES["chola Samosa"]),
# ]

# # Sync images and initial data in database
# for item_name, price, img_url in default_items:
#     cursor.execute("SELECT id, image_url FROM menu WHERE name = ?", (item_name,))
#     row = cursor.fetchone()
#     if row:
#         if not row[1]:
#             cursor.execute("UPDATE menu SET image_url = ? WHERE id = ?", (img_url, row[0]))
#     else:
#         cursor.execute(
#             "INSERT INTO menu (name, price, image_url, available) VALUES (?, ?, ?, 1)",
#             (item_name, price, img_url)
#         )

# cursor.execute("DELETE FROM menu WHERE name IN ('Resole', 'Proper Samosa')")
# conn.commit()

# # Helper function to get shop open/close status
# def get_shop_status():
#     cursor.execute("SELECT value FROM settings WHERE key = 'is_shop_open'")
#     res = cursor.fetchone()
#     return res[0] == "1" if res else True

# def set_shop_status(is_open):
#     cursor.execute("UPDATE settings SET value = ? WHERE key = 'is_shop_open'", ("1" if is_open else "0",))
#     conn.commit()

# is_shop_open = get_shop_status()

# # Session States
# if "cart" not in st.session_state:
#     st.session_state.cart = {}
# if "is_admin" not in st.session_state:
#     st.session_state.is_admin = False

# # ==============================================================================
# # 1. ADMIN INTERFACE
# # ==============================================================================
# if st.session_state.is_admin:
#     st.sidebar.success("🛡️ Logged in as Admin")
#     if st.sidebar.button("🚪 Logout (Customer View)", use_container_width=True):
#         st.session_state.is_admin = False
#         st.rerun()

#     st.title("⚙️ Admin Management Dashboard")
#     st.caption("Yeh panel sirf dukan ke owner ke liye hai.")

#     # Shop Open/Close toggle section
#     with st.container(border=True):
#         c_status, c_btn = st.columns([3, 1])
#         with c_status:
#             if is_shop_open:
#                 st.success("🟢 **Shop Status: OPEN** (Customer orders le sakte hain)")
#             else:
#                 st.error("🔴 **Shop Status: CLOSED** (Aaj shop band hai, koi order nahi hoga)")
#         with c_btn:
#             if is_shop_open:
#                 if st.button("🛑 Close Shop Today", use_container_width=True):
#                     set_shop_status(False)
#                     st.rerun()
#             else:
#                 if st.button("✅ Open Shop", use_container_width=True):
#                     set_shop_status(True)
#                     st.rerun()

#     admin_tabs = st.tabs(["📋 Menu Item Management", "➕ Add New Item to Menu"])

#     # Tab 1: Edit & Delete Items
#     with admin_tabs[0]:
#         st.subheader("Manage Current Items")
#         cursor.execute("SELECT id, name, price, available, image_url FROM menu ORDER BY id DESC")
#         all_menu_items = cursor.fetchall()

#         if not all_menu_items:
#             st.info("Abhi menu mein koi item nahi hai.")
#         else:
#             for item_id, item_name, item_price, is_avail, img_url in all_menu_items:
#                 display_img = img_url or DEFAULT_FOOD_IMAGES.get(item_name)

#                 with st.container(border=True):
#                     col_img, col_details, col_price, col_stock, col_actions = st.columns([1.5, 3, 2, 2, 2.5])

#                     with col_img:
#                         if display_img:
#                             st.image(display_img, width=90)
#                         else:
#                             st.write("📷 No image")

#                     with col_details:
#                         st.subheader(item_name)
#                         status_badge = "🟢 In Stock" if is_avail else "🔴 Out of Stock"
#                         st.caption(f"Status: {status_badge}")

#                     with col_price:
#                         updated_price = st.number_input(
#                             "Price (₹)",
#                             min_value=1.0,
#                             value=float(item_price),
#                             step=5.0,
#                             key=f"adm_price_{item_id}"
#                         )

#                     with col_stock:
#                         new_avail = st.checkbox(
#                             "Available?",
#                             value=bool(is_avail),
#                             key=f"adm_avail_{item_id}"
#                         )

#                     with col_actions:
#                         st.write("##")
#                         b1, b2 = st.columns(2)
#                         with b1:
#                             if st.button("💾 Save", key=f"save_{item_id}", use_container_width=True):
#                                 cursor.execute(
#                                     "UPDATE menu SET price = ?, available = ? WHERE id = ?",
#                                     (updated_price, 1 if new_avail else 0, item_id)
#                                 )
#                                 conn.commit()
#                                 st.success("Updated!")
#                                 st.rerun()
#                         with b2:
#                             if st.button("🗑️ Delete", key=f"del_{item_id}", use_container_width=True):
#                                 cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
#                                 conn.commit()
#                                 if item_id in st.session_state.cart:
#                                     del st.session_state.cart[item_id]
#                                 st.warning("Deleted!")
#                                 st.rerun()

#     # Tab 2: Add New Item
#     with admin_tabs[1]:
#         st.subheader("Add a New Food Item")
#         with st.form("admin_add_item_form", clear_on_submit=True):
#             new_food_name = st.text_input("Item Name (e.g., Paneer Burger, Cold Drink)")
#             new_food_price = st.number_input("Selling Price (₹)", min_value=1.0, value=30.0, step=5.0)
#             new_food_image = st.text_input("Image Web Link (URL)")
#             add_button = st.form_submit_button("➕ Save Item to Menu", use_container_width=True)

#             if add_button:
#                 if not new_food_name.strip():
#                     st.error("Item name khali nahi ho sakta.")
#                 else:
#                     try:
#                         cursor.execute(
#                             "INSERT INTO menu (name, price, image_url, available) VALUES (?, ?, ?, 1)",
#                             (new_food_name.strip(), new_food_price, new_food_image.strip())
#                         )
#                         conn.commit()
#                         st.success(f"'{new_food_name}' menu mein add ho gaya!")
#                         st.rerun()
#                     except sqlite3.IntegrityError:
#                         st.error(f"'{new_food_name}' pehle se maujood hai.")

# # ==============================================================================
# # 2. CUSTOMER INTERFACE
# # ==============================================================================
# else:
#     st.title("🍔 Mukesh Fastfood Shop")
#     st.markdown("### Fresh Food • Tasty Food • Happy Customers")

#     # Banner agar shop closed hai
#     if not is_shop_open:
#         st.error("🚫 **Notice: Today shop is not open! No orders are being accepted at the moment.**")

#     customer_page = st.sidebar.radio(
#         "📌 Navigation",
#         ["🍽️ Home & Menu", "🛒 My Cart"]
#     )

#     # ---------------- CUSTOMER MENU PAGE ----------------
#     if customer_page == "🍽️ Home & Menu":
#         st.header("🍽️ Today's Special Menu")

#         cursor.execute("""
#             SELECT id, name, price, image_url
#             FROM menu
#             WHERE available = 1
#             ORDER BY id
#         """)
#         foods = cursor.fetchall()

#         if not foods:
#             st.info("Abhi dukan par items prepare ho rahe hain.")
#         else:
#             cols = st.columns(3)
#             for idx, (food_id, name, price, img_url) in enumerate(foods):
#                 display_img = img_url or DEFAULT_FOOD_IMAGES.get(name)

#                 with cols[idx % 3]:
#                     with st.container(border=True):
#                         if display_img:
#                             st.image(display_img, use_container_width=True)

#                         st.subheader(f"🍴 {name}")
#                         st.markdown(f"**Price: ₹{price:g}**")

#                         quantity = st.number_input(
#                             "Quantity",
#                             min_value=1,
#                             max_value=20,
#                             value=1,
#                             step=1,
#                             key=f"cust_qty_{food_id}",
#                             disabled=not is_shop_open
#                         )

#                         if is_shop_open:
#                             if st.button("➕ Add to Cart", key=f"add_{food_id}", use_container_width=True):
#                                 st.session_state.cart[food_id] = (
#                                     st.session_state.cart.get(food_id, 0) + quantity
#                                 )
#                                 st.success(f"{name} cart mein add ho gaya!")
#                         else:
#                             st.button("🔒 Shop Closed", key=f"add_{food_id}", use_container_width=True, disabled=True)

#     # ---------------- CUSTOMER CART PAGE ----------------
#     elif customer_page == "🛒 My Cart":
#         st.header("🛒 Your Shopping Cart")

#         cursor.execute("SELECT id, name, price FROM menu")
#         all_foods = {f_id: (f_name, f_price) for f_id, f_name, f_price in cursor.fetchall()}

#         total = 0

#         if not st.session_state.cart:
#             st.info("Tumhara cart abhi empty hai. Menu se kuch tasty add karo!")
#         else:
#             for food_id, quantity in list(st.session_state.cart.items()):
#                 if food_id not in all_foods:
#                     continue

#                 name, price = all_foods[food_id]
#                 subtotal = price * quantity
#                 total += subtotal

#                 col1, col2, col3 = st.columns([3, 2, 2])
#                 col1.write(f"**{name}**")
#                 col2.write(f"₹{price:g} × {quantity}")
#                 col3.write(f"**₹{subtotal:g}**")

#                 if st.button("❌ Remove", key=f"rem_{food_id}"):
#                     del st.session_state.cart[food_id]
#                     st.rerun()

#             st.divider()
#             st.subheader(f"Total Amount: ₹{total:g}")

#             st.markdown("### 🧾 Delivery Details")
#             customer_name = st.text_input("Your Full Name", disabled=not is_shop_open)
#             phone = st.text_input("Mobile Number", disabled=not is_shop_open)
#             address = st.text_area("Delivery Address / Table No.", disabled=not is_shop_open)

#             if is_shop_open:
#                 if st.button("📲 Place Order via WhatsApp", use_container_width=True):
#                     if not customer_name.strip() or not phone.strip() or not address.strip():
#                         st.error("Please naam, number aur address pura bharein.")
#                     elif not st.session_state.cart:
#                         st.error("Cart empty hai.")
#                     else:
#                         order_lines = [
#                             f"{all_foods[f_id][0]} x {qty} = Rs. {all_foods[f_id][1] * qty:g}"
#                             for f_id, qty in st.session_state.cart.items()
#                             if f_id in all_foods
#                         ]

#                         message = (
#                             "Hello Mukesh Fastfood Shop!\n"
#                             f"Name: {customer_name}\n"
#                             f"Phone: {phone}\n"
#                             f"Address: {address}\n\n"
#                             "Order Summary:\n"
#                             + "\n".join(order_lines)
#                             + f"\n\nTotal: Rs. {total:g}"
#                         )

#                         whatsapp_url = f"https://wa.me/{SHOP_WHATSAPP}?text={quote(message)}"

#                         st.link_button(
#                             "Open WhatsApp & Send Order",
#                             whatsapp_url,
#                             use_container_width=True
#                         )
#                         st.caption("WhatsApp khulne par message check karke Send dabana.")
#             else:
#                 st.error("❌ Today shop is closed. New orders cannot be placed or confirmed.")

#     # ---------------- HIDDEN OWNER LOGIN ----------------
#     st.sidebar.divider()
#     with st.sidebar.expander("🔒 Owner Login"):
#         admin_pass_input = st.text_input("Enter Passkey", type="password", key="admin_key_input")
#         if st.button("Login as Owner", use_container_width=True):
#             if admin_pass_input == ADMIN_PASSWORD:
#                 st.session_state.is_admin = True
#                 st.rerun()
#             else:
#                 st.error("Galat password!")

# st.sidebar.caption("© Mukesh Fastfood Shop")





from urllib.parse import quote
import streamlit as st

st.set_page_config(
    page_title="Mukesh Fastfood Shop",
    page_icon="🍔",
    layout="wide"
)

# Shop Details
SHOP_WHATSAPP = "918683868939"
SHOP_UPI_ID = "8683868939@axl"
SHOP_OWNER_NAME = "Hemant"
ADMIN_PASSWORD = "mukesh@fastfood"

# Load CSS
try:
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Food Items (Hardcoded In-Memory Menu - No DB Needed)
MENU_ITEMS = [
    {"id": 1, "name": "Burger", "price": 25, "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600"},
    {"id": 2, "name": "Noodles", "price": 20, "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=600"},
    {"id": 3, "name": "Pizza", "price": 100, "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600"},
    {"id": 4, "name": "Patties", "price": 25, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600"},
    {"id": 5, "name": "Momos", "price": 50, "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=600"},
    {"id": 6, "name": "Simple Samosa", "price": 20, "image": "https://images.unsplash.com/photo-1601050690117-94f5f6fa8bd7?w=600"},
    {"id": 7, "name": "chola Samosa", "price": 25, "image": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600"},
]

# Session States
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "shop_open" not in st.session_state:
    st.session_state.shop_open = True
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ==============================================================================
# 1. ADMIN MODE (Shop Open/Close Toggle Only)
# ==============================================================================
if st.session_state.is_admin:
    st.sidebar.success("🛡️ Logged in as Owner")
    if st.sidebar.button("🚪 Logout to Customer View", use_container_width=True):
        st.session_state.is_admin = False
        st.rerun()

    st.title("⚙️ Owner Control Panel")
    with st.container(border=True):
        st.subheader("Shop Status Control")
        if st.session_state.shop_open:
            st.success("🟢 Shop currently OPEN hai.")
            if st.button("🛑 Shop Close Karein Aaj Ke Liye", use_container_width=True):
                st.session_state.shop_open = False
                st.rerun()
        else:
            st.error("🔴 Shop currently CLOSED hai.")
            if st.button("✅ Shop Open Karein", use_container_width=True):
                st.session_state.shop_open = True
                st.rerun()

# ==============================================================================
# 2. CUSTOMER INTERFACE
# ==============================================================================
else:
    st.title("🍔 Mukesh Fastfood Shop")
    st.markdown("### Fresh Food • Tasty Food • Happy Customers")

    if not st.session_state.shop_open:
        st.error("🚫 **Notice: Today shop is closed! No orders are being accepted at the moment.**")

    page = st.sidebar.radio("📌 Menu", ["🍽️ Food Menu", "🛒 My Cart"])

    # ---------------- MENU PAGE ----------------
    if page == "🍽️ Food Menu":
        st.header("🍽️ Our Special Menu")
        cols = st.columns(3)

        for index, item in enumerate(MENU_ITEMS):
            with cols[index % 3]:
                with st.container(border=True):
                    st.image(item["image"], use_container_width=True)
                    st.subheader(f"🍴 {item['name']}")
                    st.markdown(f"**Price: ₹{item['price']}**")

                    qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=20,
                        value=1,
                        key=f"qty_{item['id']}",
                        disabled=not st.session_state.shop_open
                    )

                    if st.session_state.shop_open:
                        if st.button("➕ Add to Cart", key=f"add_{item['id']}", use_container_width=True):
                            st.session_state.cart[item["id"]] = st.session_state.cart.get(item["id"], 0) + qty
                            st.success(f"{item['name']} cart mein add ho gaya!")
                    else:
                        st.button("🔒 Shop Closed", key=f"add_{item['id']}", use_container_width=True, disabled=True)

    # ---------------- CART & CHECKOUT PAGE ----------------
    elif page == "🛒 My Cart":
        st.header("🛒 Your Cart & Checkout")

        total = 0
        menu_lookup = {item["id"]: item for item in MENU_ITEMS}

        if not st.session_state.cart:
            st.info("Tumhara cart abhi empty hai. Menu se kuch add karo!")
        else:
            for item_id, quantity in list(st.session_state.cart.items()):
                item = menu_lookup.get(item_id)
                if not item:
                    continue
                subtotal = item["price"] * quantity
                total += subtotal

                c1, c2, c3 = st.columns([3, 2, 2])
                c1.write(f"**{item['name']}**")
                c2.write(f"₹{item['price']} × {quantity}")
                c3.write(f"**₹{subtotal}**")
                if st.button("❌ Remove", key=f"del_{item_id}"):
                    del st.session_state.cart[item_id]
                    st.rerun()

            st.divider()
            st.subheader(f"Total Amount: ₹{total}")

            st.markdown("### 🧾 Customer Details")
            c_name = st.text_input("Your Full Name", disabled=not st.session_state.shop_open)
            c_phone = st.text_input("Mobile Number", disabled=not st.session_state.shop_open)
            c_address = st.text_area("Delivery Address / Table No.", disabled=not st.session_state.shop_open)
            c_notes = st.text_area("Special Cooking Instruction (Optional):", placeholder="e.g. Mirchi kam rakhna", disabled=not st.session_state.shop_open)

            st.markdown("### 💳 Select Payment Method")
            payment_choice = st.radio(
                "Payment Mode:",
                [
                    "💵 Cash on Delivery / Counter Pay",
                    "🔗 Direct UPI Payment Link (8683868939@axl)"
                ],
                disabled=not st.session_state.shop_open
            )

            is_online = payment_choice != "💵 Cash on Delivery / Counter Pay"
            utr_number = ""
            receipt_file = None

            if is_online:
                st.info(f"👉 **Total Payable Amount: ₹{total}**")
                
                # Direct UPI link for mobile payment
                direct_upi_link = f"upi://pay?pa={SHOP_UPI_ID}&pn={quote(SHOP_OWNER_NAME)}&am={total}&cu=INR&tn={quote('Mukesh Fastfood Order')}"

                with st.container(border=True):
                    st.markdown("#### 📲 Step 1: Click Link to Pay")
                    st.write(f"• **UPI ID:** `{SHOP_UPI_ID}`")
                    st.write(f"• **Payee Name:** **{SHOP_OWNER_NAME}**")
                    st.write(f"• **Amount:** **₹{total}**")

                    st.link_button(
                        f"👉 Click Here to Pay ₹{total} ({SHOP_UPI_ID})",
                        direct_upi_link,
                        use_container_width=True
                    )
                    st.caption("Yeh link direct aapka GPay / PhonePe / Paytm kholega payment ke liye.")

                st.markdown("#### 🧾 Step 2: Payment Proof")
                utr_number = st.text_input("12-Digit UPI Ref / UTR Number *", placeholder="e.g. 428910284712")
                receipt_file = st.file_uploader("Upload Payment Screenshot / Receipt *", type=["jpg", "jpeg", "png"])

                if receipt_file is not None:
                    st.image(receipt_file, caption="Receipt Preview", width=160)

            st.write("---")

            if st.session_state.shop_open:
                if st.button("📲 Place Order via WhatsApp", use_container_width=True):
                    if not c_name.strip() or not c_phone.strip() or not c_address.strip():
                        st.error("Please naam, number aur address pura bharein.")
                    elif not st.session_state.cart:
                        st.error("Cart empty hai.")
                    elif is_online and not utr_number.strip():
                        st.error("❌ Kripya apna 12-digit UPI UTR number daalein.")
                    elif is_online and receipt_file is None:
                        st.error("❌ Kripya payment ka screenshot / receipt upload karein.")
                    else:
                        order_lines = [
                            f"{menu_lookup[i_id]['name']} x {q} = Rs. {menu_lookup[i_id]['price'] * q}"
                            for i_id, q in st.session_state.cart.items()
                            if i_id in menu_lookup
                        ]

                        pay_info = "CASH ON DELIVERY"
                        receipt_note = ""
                        if is_online:
                            pay_info = f"ONLINE UPI LINK ({SHOP_UPI_ID})\nUTR No: {utr_number.strip()}"
                            receipt_note = (
                                f"\n\n📎 RECEIPT PROOF:\n"
                                f"• UTR Number: {utr_number.strip()}\n"
                                f"• Main neeche WhatsApp chat mein payment screenshot bhej raha hoon."
                            )

                        notes_line = f"\nNote: {c_notes.strip()}" if c_notes.strip() else ""

                        message = (
                            "Hello Mukesh Fastfood Shop!\n"
                            f"Name: {c_name}\n"
                            f"Phone: {c_phone}\n"
                            f"Address: {c_address}\n\n"
                            "Order Summary:\n"
                            + "\n".join(order_lines)
                            + f"\n\nTotal Amount: Rs. {total}\n"
                            + f"Payment Mode: {pay_info}"
                            + notes_line
                            + receipt_note
                        )

                        whatsapp_url = f"https://wa.me/{SHOP_WHATSAPP}?text={quote(message)}"

                        st.success("✅ Order details ready! WhatsApp kholne ke liye button dabayein.")
                        st.link_button(
                            "Open WhatsApp & Send Order",
                            whatsapp_url,
                            use_container_width=True
                        )
                        st.caption("WhatsApp khulne par order send karein aur sath mein apni receipt photo zaroor share karein.")
            else:
                st.error("❌ Today shop is closed.")

    # ---------------- OWNER LOGIN (SIDEBAR BOTTOM) ----------------
    st.sidebar.divider()
    with st.sidebar.expander("🔒 Owner Login"):
        pwd = st.text_input("Enter Passkey", type="password")
        if st.button("Login as Owner", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Galat password!")

st.sidebar.caption("© Mukesh Fastfood Shop")