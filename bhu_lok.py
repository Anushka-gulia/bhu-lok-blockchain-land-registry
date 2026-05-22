import hashlib
import datetime
import pandas as pd


# ================= PRICE CLEANING =================
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
        return 0


# ================= BLOCK =================
class Block:
    def __init__(self, index, property_id, owner, price, previous_hash):
        self.index = index
        self.property_id = property_id
        self.owner = owner
        self.price = price
        self.timestamp = str(datetime.datetime.now())
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (
            str(self.index)
            + str(self.property_id)
            + str(self.owner)
            + str(self.price)
            + self.timestamp
            + self.previous_hash
        )
        return hashlib.sha256(data.encode()).hexdigest()


# ================= BLOCKCHAIN =================
class BhuLokBlockchain:
    def __init__(self):
        self.property_map = {}

    def create_genesis_block(self, property_id, owner, price):
        block = Block(0, property_id, owner, price, "0")
        self.property_map[property_id] = [block]
        print(f"Genesis created for {property_id}")

    def transfer_ownership(self, property_id, new_owner, price):
        if property_id not in self.property_map:
            print("Property not found")
            return

        last_block = self.property_map[property_id][-1]

        new_block = Block(
            len(self.property_map[property_id]),
            property_id,
            new_owner,
            price,
            last_block.hash,
        )

        self.property_map[property_id].append(new_block)
        print(f"Transferred to {new_owner}")

    def validate_chain(self):
        print("\nValidating Blockchain...")

        for prop, blocks in self.property_map.items():
            print(f"Checking chain for {prop}")

            for i in range(1, len(blocks)):
                curr = blocks[i]
                prev = blocks[i - 1]

                if curr.hash != curr.calculate_hash():
                    print(f"Tampering detected in {prop} at block {i}")
                    return False

                if curr.previous_hash != prev.hash:
                    print(f"Chain broken in {prop} at block {i}")
                    return False

        print("Blockchain is valid")
        return True

    def display_chain(self):
        print("\nFULL BLOCKCHAIN")
        for prop, blocks in self.property_map.items():
            print(f"\nProperty: {prop}")
            for block in blocks:
                print(vars(block))

    def get_property_history(self, property_id):
        print(f"\nHistory for {property_id}")
        for block in self.property_map[property_id]:
            print(f"{block.owner} | {block.price} | {block.timestamp}")


# ================= LOAD DATA =================
def load_data():
    print("\nLoading datasets...")

    df = pd.read_csv("Real Estate Data V21.csv")
    tx_df = pd.read_csv("transactions.csv")

    print("Columns in Real Estate:", df.columns)
    print("Columns in Transactions:", tx_df.columns)

    # Clean price column
    if "Price" in df.columns:
        df["Price"] = df["Price"].apply(clean_price)

    return df.head(5), tx_df.head(5)


# ================= ANALYTICS =================
def price_analysis(df):
    print("\nPrice Analysis")

    if "Price" in df.columns:
        print(df["Price"].describe())
    else:
        print("Price column not found")


# ================= FRAUD =================
def detect_fraud(blockchain):
    print("\nFraud Detection")

    for prop, blocks in blockchain.property_map.items():
        if len(blocks) > 3:
            print(f"Suspicious activity in {prop} (too many transfers)")


# ================= SEARCH =================
def search_property(df):
    print("\nSample Search")

    if "Price" in df.columns:
        avg_price = df["Price"].mean()
        result = df[df["Price"] < avg_price]
        print(result.head())
    else:
        print(df.head())


# ================= MAIN =================
if __name__ == "__main__":
    df, tx_df = load_data()

    blockchain = BhuLokBlockchain()

    # 1. Genesis blocks
    for i, row in df.iterrows():
        property_id = f"PROP-{i}"
        price = row["Price"] if "Price" in df.columns else row.iloc[0]
        blockchain.create_genesis_block(property_id, "Owner_A", price)

    # 2. Transfers (demo on PROP-0)
    for i, row in tx_df.iterrows():
        try:
            buyer = str(row.iloc[0])
            price = row.iloc[1]
            blockchain.transfer_ownership("PROP-0", buyer, price)
        except:
            continue

    # 3. Display blockchain
    blockchain.display_chain()

    # 4. History
    blockchain.get_property_history("PROP-0")

    # 5. Validate
    blockchain.validate_chain()

    # 6. Tampering test
    print("\nTampering Simulation")
    blockchain.property_map["PROP-0"][1].owner = "HACKER"
    blockchain.validate_chain()

    # 7. Analytics
    price_analysis(df)

    # 8. Fraud detection
    detect_fraud(blockchain)

    # 9. Search
    search_property(df)