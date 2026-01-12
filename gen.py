import os
import csv
import random

def generate_ads_csv():
    # 1. Setup Paths (Creates /data folder in the same directory as this script)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(SCRIPT_DIR, "data")
    CSV_PATH = os.path.join(DATA_DIR, "ads.csv")

    # 2. Define Sample Data Components
    products = [
        ("SmartWatch X", "Tech"), ("Eco Bottle", "Lifestyle"), ("FastRunner Shoes", "Sports"),
        ("NoiseCancel Pro", "Tech"), ("Organic Green Tea", "Food"), ("Yoga Mat Ultra", "Sports"),
        ("Gaming Laptop Z", "Tech"), ("Minimalist Desk Lamp", "Home"), ("Vitamin C Serum", "Beauty"),
        ("Wireless Charger Pad", "Tech"), ("Chef's Knife Set", "Home"), ("Hiking Backpack", "Travel"),
        ("Aura Smart Ring", "Tech"), ("PureMist Humidifier", "Home"), ("Velocity Bike", "Sports")
    ]

    ad_templates = [
        "Experience the future of {category}. {product} is here, and it's life-changing.",
        "Stay ahead with {product}. The ultimate choice for {category} lovers!",
        "Don't compromise on quality; choose {product} for your daily {category} needs.",
        "Transform your routine with the all-new {product}. It's sleek, fast, and reliable.",
        "Eco-friendly, durable, and stylish. This is the {product} you've been waiting for.",
        "Get more done with {product}. Where performance meets modern {category} style.",
        "The perfect gift for yourself: {product} is now available in all stores.",
        "Upgrade your {category} game with {product}. Order today for a special discount!",
        "Simple. Elegant. Powerful. Meet the new {product}.",
        "Join the revolution. {product} changes everything you know about {category}."
    ]

    # 3. Generate 150 rows of data
    rows = []
    for _ in range(150):
        prod_name, category = random.choice(products)
        template = random.choice(ad_templates)
        
        # Fill in the template
        ad_copy = template.format(product=prod_name, category=category)
        rows.append([prod_name, ad_copy])

    # 4. Create directory and Write to CSV
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created directory: {DATA_DIR}")

        # QUOTE_ALL prevents the "Expected 2 fields, saw 3" error in Pandas
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Product", "Ad"]) # Header
            writer.writerows(rows)

        print("-" * 30)
        print(f"✅ SUCCESS: 'ads.csv' generated with {len(rows)} rows.")
        print(f"📍 Location: {CSV_PATH}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ Error generating CSV: {e}")

if __name__ == "__main__":
    generate_ads_csv()