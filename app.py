import streamlit as st
import pandas as pd
import hashlib

st.set_page_config(page_title="Bhu-Lok", layout="wide")

# ================= USERS =================
users = {
    "officer": {"password": "123", "role": "Government"},
    "seller": {"password": "123", "role": "Seller"},
    "buyer": {"password": "123", "role": "Buyer"}
}

# ================= LOGIN =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.logged_in:

    st.title("Bhu-Lok Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            st.success(f"Logged in as {st.session_state.role}")
            st.rerun()

        else:
            st.error("Invalid Credentials")

    st.stop()

# ================= LOGOUT =================
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = None

    st.rerun()

# ================= PRICE CLEAN =================
def clean_price(value):
    try:
        value = str(value).replace("₹", "").strip()

        if "Cr" in value:
            return float(value.replace("Cr", "").strip()) * 10000000

        elif "L" in value:
            return float(value.replace("L", "").strip()) * 100000

        else:
            return float(value)

    except:
        return 0.0


# ================= BLOCK =================
class Block:

    def __init__(
        self,
        index,
        property_id,
        owner,
        price,
        previous_hash,
        timestamp
    ):

        self.index = index
        self.property_id = property_id
        self.owner = owner
        self.price = price
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):

        data = (
            str(self.index)
            + str(self.property_id)
            + str(self.owner)
            + str(self.price)
            + str(self.timestamp)
            + str(self.previous_hash)
        )

        return hashlib.sha256(data.encode()).hexdigest()


# ================= BLOCKCHAIN =================
class BhuLokBlockchain:

    def __init__(self):
        self.property_map = {}

    def create_genesis_block(
        self,
        property_id,
        owner,
        price,
        timestamp
    ):

        block = Block(
            0,
            property_id,
            owner,
            price,
            "0",
            timestamp
        )

        self.property_map[property_id] = [block]

    def transfer_ownership(
        self,
        property_id,
        new_owner,
        price,
        timestamp
    ):

        last_block = self.property_map[property_id][-1]

        new_block = Block(
            len(self.property_map[property_id]),
            property_id,
            new_owner,
            price,
            last_block.hash,
            timestamp
        )

        self.property_map[property_id].append(new_block)

    def validate_chain(self):

        for prop, blocks in self.property_map.items():

            for i in range(1, len(blocks)):

                curr = blocks[i]
                prev = blocks[i - 1]

                if curr.hash != curr.calculate_hash():
                    return False

                if curr.previous_hash != prev.hash:
                    return False

        return True


# ================= LOAD DATA =================
@st.cache_data
def load_data():

    df = pd.read_csv("Real Estate Data V21.csv")
    tx_df = pd.read_csv("transactions.csv")

    if "Price" in df.columns:
        df["Price"] = df["Price"].apply(clean_price)

    return df.head(5), tx_df.head(10)


df, tx_df = load_data()

# ================= SESSION =================
if "blockchain" not in st.session_state:
    st.session_state.blockchain = BhuLokBlockchain()

if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "transactions_done" not in st.session_state:
    st.session_state.transactions_done = False

blockchain = st.session_state.blockchain

# ================= UI =================
st.title("Bhu-Lok: Blockchain Land Registry System")

st.sidebar.header("Controls")

st.sidebar.write(f"Logged in as: {st.session_state.role}")

# ================= INITIALIZE =================
if st.sidebar.button("Initialize Properties"):

    if not st.session_state.initialized:

        for i, row in df.iterrows():

            property_id = f"PROP-{i}"

            owner = (
                row["Name"]
                if "Name" in df.columns
                else "Unknown"
            )

            price = (
                row["Price"]
                if "Price" in df.columns
                else 0
            )

            blockchain.create_genesis_block(
                property_id,
                owner,
                price,
                f"GENESIS-{i}"
            )

        st.session_state.initialized = True

        st.sidebar.success("Properties Initialized")

    else:
        st.sidebar.warning("Already initialized")

# ================= TRANSACTIONS =================
if st.sidebar.button("Run Transactions"):

    if (
        st.session_state.initialized
        and not st.session_state.transactions_done
    ):

        properties = list(blockchain.property_map.keys())

        for i, row in tx_df.iterrows():

            try:

                buyer = str(row.iloc[0])

                price = float(row.iloc[1])

                property_id = properties[i % len(properties)]

                blockchain.transfer_ownership(
                    property_id,
                    buyer,
                    price,
                    f"TX-{i}"
                )

            except:
                continue

        st.session_state.transactions_done = True

        st.sidebar.success("Transactions Added")

# ================= PROPERTY VIEW =================
property_list = list(blockchain.property_map.keys())

if property_list:

    selected_property = st.selectbox(
        "Select Property",
        property_list
    )

    selected_index = int(selected_property.split("-")[1])

    st.subheader("Property Details")

    st.dataframe(df.iloc[[selected_index]])

    st.subheader("Current Owner")

    current_owner = blockchain.property_map[selected_property][-1].owner

    st.write(current_owner)

    # ================= SMART CONTRACT =================
    st.subheader("Smart Contract Transfer")

    seller_name = st.text_input("Seller Name")

    buyer_name = st.text_input("Buyer Name")

    payment = st.number_input(
        "Payment Amount",
        min_value=0
    )

    if st.button("Execute Smart Contract"):

        # GOVERNMENT CHECK
        if st.session_state.role != "Government":

            st.error(
                "Only Government Officer can approve transfers"
            )

        # SELLER VALIDATION
        elif seller_name != current_owner:

            st.error(
                "Seller is not current property owner"
            )

        # PAYMENT VALIDATION
        elif payment <= 0:

            st.error("Invalid Payment")

        else:

            blockchain.transfer_ownership(
                selected_property,
                buyer_name,
                payment,
                f"SMART-CONTRACT-{buyer_name}"
            )

            st.success(
                "Smart Contract Executed Successfully"
            )

    # ================= HISTORY =================
    st.subheader("Ownership History")

    blocks = blockchain.property_map[selected_property]

    for block in blocks:

        st.write({
            "Index": block.index,
            "Owner": block.owner,
            "Price": block.price,
            "Timestamp": block.timestamp
        })

    # ================= STRUCTURE =================
    st.subheader("Blockchain Structure")

    for block in blocks:

        st.json({
            "Index": block.index,
            "Prev Hash": block.previous_hash,
            "Hash": block.hash
        })

# ================= VALIDATION =================
st.subheader("Validate Blockchain")

if st.button("Validate"):

    if blockchain.validate_chain():

        st.success("Blockchain is Valid")

    else:

        st.error("Blockchain Tampered")

# ================= MODIFY PAST BLOCK =================
st.subheader("Tampering Simulation")

if st.button("Modify Past Block"):

    blocks = blockchain.property_map[selected_property]

    if len(blocks) > 1:

        blocks[1].owner = "HACKER"

        st.warning(
            "Past block modified successfully"
        )

        st.rerun()

# ================= INSERT FAKE BLOCK =================
st.subheader("Insert Fake Block (Middle Attack)")

if st.button("Insert Fake Block"):

    blocks = blockchain.property_map[selected_property]

    if len(blocks) > 1:

        prev_block = blocks[0]

        fake_block = Block(
            index=999,
            property_id=selected_property,
            owner="FAKE_OWNER",
            price=999999,
            previous_hash=prev_block.hash,
            timestamp="FAKE-BLOCK"
        )

        blocks.insert(1, fake_block)

        st.error(
            "Fake Block Inserted in Middle"
        )

        st.rerun()

# ================= ANALYTICS =================
st.subheader("Price Analysis")

if "Price" in df.columns:

    st.write(df["Price"].describe())

    st.bar_chart(df["Price"])