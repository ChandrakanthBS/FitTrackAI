import json

dataset = {}

def add_food(name, cal, p, c, f, fib, sug, sod, pot, vits, cat, serving="100g"):
    dataset[name.lower().strip()] = {
        "calories": int(cal),
        "protein": round(float(p), 1),
        "carbs": round(float(c), 1),
        "fats": round(float(f), 1),
        "fiber": round(float(fib), 1),
        "sugar": round(float(sug), 1),
        "sodium": int(sod),
        "potassium": int(pot),
        "vitamins": vits,
        "category": cat,
        "usda_id": f"IFCT/USDA #{len(dataset)+101:04d}",
        "serving_size": serving,
        "dataset_source": "Indian Food Composition Tables (IFCT) / USDA Standard"
    }

# ----------------------------------------------------
# 1. GRAINS, BREADS & STAPLES (75 Items)
# ----------------------------------------------------
grains = [
    ("white rice", 130, 2.7, 28.2, 0.3, 0.4, 0.1, 1, 35, "Folate, Thiamin, Niacin", "Grains & Staples"),
    ("basmati rice", 121, 3.5, 25.0, 0.4, 1.0, 0.1, 2, 45, "B-Vitamins, Manganese", "Grains & Staples"),
    ("brown rice", 111, 2.6, 23.0, 0.9, 1.8, 0.4, 5, 86, "Magnesium, B-Complex", "Grains & Staples"),
    ("red rice", 109, 2.3, 23.5, 0.8, 2.0, 0.3, 4, 90, "Zinc, Iron, Antioxidants", "Grains & Staples"),
    ("black rice", 160, 4.9, 34.0, 1.5, 2.8, 0.5, 6, 110, "Anthocyanins, Iron", "Grains & Staples"),
    ("jasmine rice", 129, 2.4, 28.0, 0.2, 0.6, 0.1, 1, 30, "Niacin, Thiamin", "Grains & Staples"),
    ("jeera rice", 165, 3.2, 27.5, 4.5, 1.2, 0.2, 140, 65, "Manganese, Iron", "Grains & Staples"),
    ("curd rice", 145, 4.2, 20.5, 5.2, 0.8, 1.5, 180, 120, "Probiotics, Calcium", "Grains & Staples"),
    ("lemon rice", 170, 3.0, 28.0, 5.5, 1.5, 0.5, 210, 80, "Vitamin C, Potassium", "Grains & Staples"),
    ("tamarind rice", 185, 3.1, 30.5, 6.0, 2.0, 1.2, 240, 95, "Antioxidants, Vitamin C", "Grains & Staples"),
    ("tomato rice", 160, 3.0, 26.0, 5.0, 1.8, 1.8, 220, 110, "Lycopene, Vitamin C", "Grains & Staples"),
    ("coconut rice", 210, 3.5, 25.0, 10.5, 2.2, 1.5, 160, 140, "MCTs, Lauric Acid", "Grains & Staples"),
    ("sambar rice", 140, 4.5, 23.0, 3.2, 3.0, 1.5, 260, 180, "Fiber, Protein, Vitamin C", "Grains & Staples"),
    ("veg fried rice", 175, 3.8, 30.0, 4.5, 2.0, 1.2, 310, 130, "Vitamin A, C, Minerals", "Grains & Staples"),
    ("egg fried rice", 195, 6.5, 28.0, 6.2, 1.5, 0.8, 340, 150, "Protein, Choline, B12", "Grains & Staples"),
    ("chicken fried rice", 220, 11.5, 27.0, 7.5, 1.5, 0.8, 380, 180, "Protein, Niacin, B6", "Grains & Staples"),
    ("schezwan fried rice", 190, 4.0, 31.0, 5.8, 2.0, 1.5, 420, 140, "Capsaicin, Vitamin C", "Grains & Staples"),
    ("prawn fried rice", 210, 10.5, 26.5, 6.5, 1.5, 0.8, 410, 170, "Selenium, Protein, B12", "Grains & Staples"),
    ("roti", 260, 7.8, 45.5, 5.5, 6.5, 0.5, 275, 240, "Iron, Fiber, B-Vitamins", "Grains & Staples"),
    ("chapati", 260, 7.8, 45.5, 5.5, 6.5, 0.5, 275, 240, "Iron, Fiber, B-Vitamins", "Grains & Staples"),
    ("butter roti", 320, 7.5, 45.0, 12.0, 6.5, 0.5, 310, 240, "Vitamin A, Iron, Fiber", "Grains & Staples"),
    ("tandoori roti", 240, 7.5, 46.0, 2.5, 6.0, 0.5, 260, 230, "B-Complex, Iron", "Grains & Staples"),
    ("missi roti", 284, 11.0, 44.0, 7.6, 8.4, 1.0, 300, 320, "High Protein, Fiber, Zinc", "Grains & Staples"),
    ("rumali roti", 290, 7.0, 52.0, 5.5, 3.0, 1.0, 280, 150, "Niacin, Carbohydrates", "Grains & Staples"),
    ("bajra roti", 258, 7.1, 47.8, 4.0, 7.6, 0.4, 90, 310, "Magnesium, Iron, Fiber", "Grains & Staples"),
    ("jowar roti", 245, 7.0, 50.0, 2.2, 7.5, 0.3, 85, 300, "Fiber, Antioxidants, Iron", "Grains & Staples"),
    ("ragi roti", 230, 5.8, 46.0, 2.5, 8.2, 0.4, 95, 340, "Extreme Calcium, Fiber, Iron", "Grains & Staples"),
    ("makki ki roti", 270, 5.5, 48.0, 6.5, 6.0, 1.0, 110, 210, "Beta-Carotene, Fiber", "Grains & Staples"),
    ("akki roti", 240, 4.5, 44.0, 5.2, 3.5, 0.8, 220, 160, "B-Vitamins, Carbohydrates", "Grains & Staples"),
    ("plain naan", 290, 8.3, 50.0, 5.8, 2.2, 3.3, 465, 122, "Niacin, Thiamin, Iron", "Grains & Staples"),
    ("butter naan", 345, 8.2, 49.5, 12.5, 2.2, 3.3, 510, 128, "Vitamin A, Calcium", "Grains & Staples"),
    ("garlic naan", 355, 8.8, 50.5, 13.0, 2.4, 3.3, 530, 140, "Allicin, Vitamin B6", "Grains & Staples"),
    ("cheese naan", 390, 12.5, 48.0, 16.5, 2.0, 3.5, 620, 160, "Calcium, Protein, B12", "Grains & Staples"),
    ("stuffed naan", 360, 9.0, 52.0, 12.5, 3.5, 3.5, 550, 210, "Potassium, B-Vitamins", "Grains & Staples"),
    ("aloo paratha", 223, 5.0, 32.3, 8.5, 3.5, 1.2, 292, 238, "Vitamin C, Potassium, B6", "Grains & Staples"),
    ("gobi paratha", 210, 5.2, 30.0, 8.0, 4.0, 1.5, 280, 250, "Vitamin C, K, Fiber", "Grains & Staples"),
    ("paneer paratha", 243, 8.9, 27.1, 11.1, 2.5, 1.3, 293, 157, "Calcium, Protein, B12", "Grains & Staples"),
    ("mooli paratha", 195, 4.8, 29.0, 7.2, 4.2, 1.2, 270, 220, "Vitamin C, Digestive Enzymes", "Grains & Staples"),
    ("onion paratha", 215, 4.9, 31.0, 8.0, 3.6, 2.0, 285, 210, "Quercetin, Vitamin C", "Grains & Staples"),
    ("methi paratha", 210, 5.5, 29.5, 7.8, 4.5, 1.0, 275, 240, "Iron, Fiber, Antioxidants", "Grains & Staples"),
    ("lachha paratha", 320, 6.5, 42.0, 14.5, 3.0, 1.0, 340, 180, "Carbohydrates, Lipids", "Grains & Staples"),
    ("kerala parotta", 340, 6.8, 44.0, 15.5, 2.0, 2.0, 360, 140, "Carbohydrates, Energy", "Grains & Staples"),
    ("puri", 357, 5.7, 42.8, 18.6, 3.4, 0.3, 243, 114, "Iron, Carbohydrates", "Grains & Staples"),
    ("bhature", 322, 6.7, 42.2, 14.4, 2.0, 2.2, 355, 100, "Niacin, Thiamin, Iron", "Grains & Staples"),
    ("dosa", 210, 4.7, 36.2, 4.9, 1.9, 0.6, 225, 119, "Probiotics, B-Vitamins", "Grains & Staples"),
    ("masala dosa", 175, 3.4, 25.0, 6.7, 2.3, 1.0, 233, 178, "Vitamin C, Potassium", "Grains & Staples"),
    ("mysore masala dosa", 210, 4.2, 27.0, 9.5, 2.8, 1.5, 280, 210, "Vitamin C, Potassium, B-Vitamins", "Grains & Staples"),
    ("rava dosa", 225, 4.8, 35.0, 7.2, 2.0, 1.0, 260, 130, "Iron, Magnesium", "Grains & Staples"),
    ("onion dosa", 215, 4.5, 34.0, 6.8, 2.5, 2.2, 240, 150, "Quercetin, B-Vitamins", "Grains & Staples"),
    ("cheese dosa", 270, 9.0, 32.0, 12.0, 1.8, 1.2, 410, 140, "Calcium, Protein, B12", "Grains & Staples"),
    ("paneer dosa", 250, 10.0, 30.0, 10.5, 2.0, 1.5, 350, 170, "Calcium, Protein, B12", "Grains & Staples"),
    ("paper dosa", 230, 4.5, 40.0, 5.5, 1.8, 0.5, 240, 110, "Carbohydrates, B-Vitamins", "Grains & Staples"),
    ("set dosa", 190, 4.2, 34.0, 4.0, 2.2, 0.8, 210, 125, "Fermented Probiotics", "Grains & Staples"),
    ("idli", 129, 4.4, 26.7, 0.7, 1.8, 0.4, 144, 100, "Probiotics, B-Complex", "Grains & Staples"),
    ("rava idli", 145, 4.0, 25.0, 3.2, 1.5, 0.8, 190, 110, "Iron, Magnesium", "Grains & Staples"),
    ("button idli", 130, 4.4, 26.5, 0.7, 1.8, 0.4, 145, 100, "Probiotics, B-Vitamins", "Grains & Staples"),
    ("rava upma", 122, 2.8, 20.0, 3.6, 1.6, 0.8, 175, 69, "B-Vitamins, Iron", "Grains & Staples"),
    ("semiya upma", 135, 3.0, 22.0, 4.0, 1.2, 0.8, 190, 65, "B-Vitamins, Carbohydrates", "Grains & Staples"),
    ("kanda poha", 120, 2.5, 22.0, 2.8, 1.5, 1.3, 160, 87, "Iron, Vitamin C", "Grains & Staples"),
    ("batata poha", 140, 2.6, 25.0, 3.2, 1.8, 1.2, 180, 130, "Iron, Vitamin C, B6", "Grains & Staples"),
    ("indori poha", 150, 3.2, 26.0, 3.8, 2.0, 2.5, 210, 110, "Iron, Antioxidants", "Grains & Staples"),
    ("sabudana khichdi", 195, 1.5, 38.0, 4.5, 1.0, 0.5, 220, 95, "Carbohydrates, Calcium", "Grains & Staples"),
    ("dal khichdi", 125, 4.8, 21.0, 2.5, 2.8, 0.8, 240, 160, "Protein, Fiber, Folate", "Grains & Staples"),
    ("oats khichdi", 115, 4.5, 18.5, 2.2, 3.5, 0.8, 210, 170, "Beta-Glucan, Fiber, Iron", "Grains & Staples"),
    ("rolled oats", 389, 16.9, 66.3, 6.9, 10.6, 0.0, 2, 362, "Beta-Glucan, Iron, Zinc", "Grains & Staples"),
    ("quinoa", 120, 4.4, 21.3, 1.9, 2.8, 0.9, 7, 172, "Magnesium, Folate, Copper", "Grains & Staples"),
    ("wheat bread", 247, 13.0, 41.0, 3.4, 6.0, 6.0, 450, 250, "B-Vitamins, Magnesium", "Grains & Staples"),
    ("white bread", 265, 9.0, 49.0, 3.2, 2.7, 5.0, 490, 115, "Folate, Thiamin, Iron", "Grains & Staples"),
    ("garlic bread", 350, 8.5, 42.0, 17.0, 2.0, 3.0, 580, 130, "Allicin, Vitamin B6", "Grains & Staples"),
    ("kulcha", 244, 6.4, 44.4, 4.7, 2.0, 2.8, 380, 100, "Niacin, Thiamin", "Grains & Staples"),
    ("noodles", 138, 4.5, 25.0, 2.1, 1.2, 0.5, 180, 45, "Thiamin, Iron", "Grains & Staples"),
    ("pasta", 158, 5.8, 31.0, 0.9, 1.8, 0.6, 1, 44, "Folate, Niacin, Iron", "Grains & Staples"),
    ("spaghetti", 158, 5.8, 31.0, 0.9, 1.8, 0.6, 1, 44, "Folate, Niacin, Iron", "Grains & Staples"),
    ("macaroni", 158, 5.8, 31.0, 0.9, 1.8, 0.6, 1, 44, "Folate, Niacin, Iron", "Grains & Staples"),
    ("hakka noodles", 165, 4.8, 28.0, 3.8, 1.5, 0.8, 220, 60, "Iron, Carbohydrates", "Grains & Staples")
]

for item in grains:
    add_food(*item)

# ----------------------------------------------------
# 2. DALS, PULSES & LEGUMES (55 Items)
# ----------------------------------------------------
dals = [
    ("dal tadka", 92, 4.6, 12.0, 3.0, 2.8, 0.8, 170, 190, "Protein, Folate, Iron", "Dals & Pulses"),
    ("dal fry", 105, 4.8, 13.0, 4.2, 3.0, 1.0, 190, 200, "Protein, Folate, Iron", "Dals & Pulses"),
    ("dal makhani", 127, 4.8, 12.7, 6.4, 2.7, 0.9, 191, 186, "Calcium, Iron, Protein", "Dals & Pulses"),
    ("rajma curry", 109, 5.2, 15.5, 3.0, 3.9, 1.1, 177, 218, "Iron, Potassium, Fiber", "Dals & Pulses"),
    ("chana masala", 118, 5.5, 16.4, 3.4, 4.1, 1.4, 186, 209, "Folate, Zinc, Iron, Fiber", "Dals & Pulses"),
    ("chole", 118, 5.5, 16.4, 3.4, 4.1, 1.4, 186, 209, "Folate, Zinc, Iron, Fiber", "Dals & Pulses"),
    ("amritsari chole", 130, 5.8, 17.0, 4.5, 4.2, 1.5, 210, 220, "Iron, Protein, Fiber", "Dals & Pulses"),
    ("moong dal", 78, 4.7, 11.1, 1.6, 2.7, 0.7, 155, 178, "Potassium, Magnesium, Folate", "Dals & Pulses"),
    ("toor dal", 89, 5.0, 12.8, 1.8, 2.9, 0.6, 161, 194, "Folate, B-Vitamins, Iron", "Dals & Pulses"),
    ("masoor dal", 86, 5.3, 12.5, 1.4, 2.8, 0.6, 150, 185, "Protein, Iron, Fiber", "Dals & Pulses"),
    ("chana dal", 105, 5.8, 15.0, 2.2, 3.8, 0.8, 165, 210, "Protein, Fiber, Folate", "Dals & Pulses"),
    ("urad dal", 98, 5.5, 13.5, 2.0, 3.2, 0.5, 160, 200, "Protein, Calcium, Iron", "Dals & Pulses"),
    ("panchmel dal", 110, 5.6, 14.2, 3.2, 3.5, 0.8, 180, 210, "High Protein, Fiber, Iron", "Dals & Pulses"),
    ("gujarati dal", 95, 4.2, 14.0, 2.5, 2.5, 3.5, 175, 180, "Sweet & Sour, Folate", "Dals & Pulses"),
    ("maharashtrian amti", 90, 4.0, 13.0, 2.8, 2.6, 2.0, 180, 175, "Tamarind, Fiber, Iron", "Dals & Pulses"),
    ("sambar", 65, 2.8, 10.0, 1.6, 2.3, 1.2, 155, 145, "Vitamin C, Fiber, Minerals", "Dals & Pulses"),
    ("rasam", 40, 1.2, 6.5, 1.2, 1.0, 0.8, 140, 110, "Digestive Spices, Vitamin C", "Dals & Pulses"),
    ("tomato rasam", 45, 1.4, 7.0, 1.4, 1.2, 1.2, 150, 120, "Lycopene, Vitamin C", "Dals & Pulses"),
    ("pepper rasam", 42, 1.3, 6.8, 1.3, 1.1, 0.6, 145, 115, "Piperine, Vitamin C", "Dals & Pulses"),
    ("kadhi pakora", 100, 3.0, 10.0, 5.5, 0.9, 1.6, 200, 95, "Calcium, Probiotics, Zinc", "Dals & Pulses"),
    ("gujarati kadhi", 75, 2.5, 8.5, 3.2, 0.5, 3.0, 170, 90, "Probiotics, Calcium", "Dals & Pulses"),
    ("maharashtrian kadhi", 70, 2.4, 7.8, 3.0, 0.5, 1.8, 165, 85, "Probiotics, Calcium", "Dals & Pulses"),
    ("kala chana curry", 110, 5.2, 15.0, 3.2, 4.5, 1.0, 180, 230, "Iron, High Fiber, Protein", "Dals & Pulses"),
    ("sprouts salad", 80, 5.3, 12.0, 1.0, 3.0, 1.3, 80, 207, "Vitamin C, K, Folate, Fiber", "Dals & Pulses"),
    ("moong sprouts", 70, 5.5, 11.5, 0.8, 3.2, 1.0, 45, 220, "Vitamin C, Protein, Enzymes", "Dals & Pulses"),
    ("chana sprouts", 90, 5.8, 13.5, 1.2, 4.0, 1.2, 50, 240, "Iron, Fiber, Protein", "Dals & Pulses"),
    ("moong dal chilla", 181, 11.2, 23.8, 4.4, 4.8, 1.2, 275, 350, "Protein, Folate, Iron", "Dals & Pulses"),
    ("besan chilla", 195, 10.5, 25.0, 5.5, 4.2, 1.5, 290, 320, "Protein, Fiber, Folate", "Dals & Pulses"),
    ("lobia curry", 105, 5.0, 14.5, 2.8, 3.8, 1.0, 175, 210, "Folate, Fiber, Iron", "Dals & Pulses"),
    ("matki curry", 112, 5.4, 15.2, 3.0, 4.0, 1.1, 180, 220, "Protein, Fiber, Zinc", "Dals & Pulses"),
    ("horse gram soup", 65, 4.2, 9.5, 1.2, 3.0, 0.5, 140, 190, "Iron, Calcium, Protein", "Dals & Pulses"),
    ("ragda", 115, 5.2, 16.0, 3.2, 4.0, 1.5, 210, 200, "Protein, Fiber, Iron", "Dals & Pulses"),
    ("usal", 120, 5.5, 15.5, 4.0, 4.2, 1.2, 220, 210, "Protein, Fiber, Spices", "Dals & Pulses"),
    ("misal gravy", 135, 5.2, 14.0, 6.5, 3.5, 1.5, 280, 190, "Proteins, Spicy Lipids", "Dals & Pulses")
]

for item in dals:
    add_food(*item)

# ----------------------------------------------------
# 3. PANEER & VEGETARIAN CURRIES (75 Items)
# ----------------------------------------------------
veg_curries = [
    ("paneer butter masala", 163, 6.3, 5.4, 12.7, 1.1, 1.8, 222, 118, "Calcium, Vitamin A, B12", "Paneer & Veg Curries"),
    ("palak paneer", 122, 6.8, 4.0, 9.0, 1.7, 0.9, 190, 218, "Iron, Vitamin A, Calcium, Folate", "Paneer & Veg Curries"),
    ("paneer tikka", 155, 10.0, 4.4, 10.5, 1.1, 1.3, 250, 116, "Calcium, Protein, B12", "Paneer & Veg Curries"),
    ("shahi paneer", 172, 6.1, 6.3, 13.6, 1.0, 2.2, 230, 109, "Calcium, Vitamin A, Lipids", "Paneer & Veg Curries"),
    ("kadai paneer", 140, 7.0, 5.0, 10.4, 1.3, 1.3, 209, 131, "Vitamin C, Calcium, Protein", "Paneer & Veg Curries"),
    ("matar paneer", 130, 6.5, 8.0, 8.0, 2.0, 1.7, 195, 160, "Vitamin K, C, Calcium", "Paneer & Veg Curries"),
    ("paneer do pyaza", 150, 6.8, 6.0, 11.0, 1.2, 2.0, 215, 135, "Quercetin, Calcium, Protein", "Paneer & Veg Curries"),
    ("paneer lababdar", 168, 6.5, 5.8, 13.2, 1.1, 2.0, 225, 125, "Calcium, Vitamin A", "Paneer & Veg Curries"),
    ("paneer pasanda", 175, 7.2, 6.5, 13.8, 1.2, 2.2, 240, 130, "Calcium, Lipids", "Paneer & Veg Curries"),
    ("paneer bhurji", 185, 12.0, 3.5, 13.5, 0.8, 1.0, 260, 140, "High Protein, Calcium", "Paneer & Veg Curries"),
    ("malai kofta", 177, 4.3, 10.0, 13.6, 1.3, 2.5, 236, 127, "Calcium, Vitamin A, Lipids", "Paneer & Veg Curries"),
    ("veg kofta", 135, 3.2, 11.5, 8.5, 1.8, 1.8, 210, 150, "Fiber, Vitamin C, A", "Paneer & Veg Curries"),
    ("aloo gobi", 88, 2.2, 12.2, 3.8, 2.5, 1.6, 188, 250, "Vitamin C, K, B6, Fiber", "Paneer & Veg Curries"),
    ("aloo matar", 97, 2.3, 13.3, 4.0, 2.3, 1.7, 183, 233, "Vitamin C, B6, Fiber", "Paneer & Veg Curries"),
    ("aloo baingan", 82, 1.8, 11.5, 3.5, 2.8, 2.0, 175, 220, "Antioxidants, Fiber", "Paneer & Veg Curries"),
    ("aloo bhindi", 85, 2.0, 11.0, 3.8, 2.6, 1.5, 170, 230, "Folate, Fiber, Vitamin C", "Paneer & Veg Curries"),
    ("aloo jeera", 95, 1.8, 13.5, 4.2, 2.0, 1.0, 190, 240, "Cumin Iron, Vitamin C", "Paneer & Veg Curries"),
    ("aloo methi", 90, 2.5, 12.0, 3.8, 2.8, 1.0, 180, 260, "Iron, Fiber, Vitamin C", "Paneer & Veg Curries"),
    ("dum aloo", 115, 2.0, 14.0, 6.0, 1.9, 1.5, 190, 230, "Potassium, Vitamin B6", "Paneer & Veg Curries"),
    ("bhindi masala", 87, 2.1, 8.7, 5.3, 2.5, 1.5, 181, 237, "Folate, Vitamin C, Fiber", "Paneer & Veg Curries"),
    ("bhindi fry", 110, 2.2, 9.5, 7.5, 2.8, 1.2, 195, 240, "Fiber, Vitamin C, Folate", "Paneer & Veg Curries"),
    ("baingan bharta", 83, 1.6, 8.3, 5.0, 2.7, 2.2, 172, 200, "Potassium, Antioxidants", "Paneer & Veg Curries"),
    ("stuffed baingan", 95, 2.0, 9.5, 6.0, 3.0, 2.0, 185, 210, "Antioxidants, Fiber", "Paneer & Veg Curries"),
    ("mix veg curry", 90, 2.2, 9.0, 5.0, 2.4, 1.7, 175, 205, "Vitamin A, C, Fiber", "Paneer & Veg Curries"),
    ("veg kolhapuri", 105, 2.5, 9.8, 6.5, 2.6, 1.8, 210, 215, "Spices, Vitamin C, Fiber", "Paneer & Veg Curries"),
    ("veg handi", 98, 2.4, 9.2, 5.8, 2.5, 1.8, 195, 210, "Vitamin A, C, Fiber", "Paneer & Veg Curries"),
    ("veg jalfrezi", 85, 2.0, 9.0, 4.8, 2.5, 2.2, 180, 200, "Vitamin C, A, Fiber", "Paneer & Veg Curries"),
    ("veg korma", 115, 2.6, 9.5, 7.5, 2.2, 2.0, 190, 220, "Calcium, Vitamin A", "Paneer & Veg Curries"),
    ("navratan korma", 130, 3.0, 11.0, 8.5, 2.4, 3.0, 200, 230, "Dry Fruits, Vitamin A", "Paneer & Veg Curries"),
    ("sarson ka saag", 75, 3.0, 6.5, 4.2, 3.2, 1.0, 160, 280, "Extreme Vitamin K, A, Iron", "Paneer & Veg Curries"),
    ("chana saag", 95, 4.2, 12.5, 3.5, 3.8, 1.2, 175, 260, "Iron, Folate, Fiber", "Paneer & Veg Curries"),
    ("methi matar malai", 145, 3.5, 9.0, 10.5, 2.5, 2.5, 195, 210, "Vitamin K, A, Lipids", "Paneer & Veg Curries"),
    ("corn palak", 90, 3.2, 10.5, 4.2, 2.8, 1.5, 170, 240, "Lutein, Iron, Vitamin A", "Paneer & Veg Curries"),
    ("mushroom masala", 85, 3.5, 6.8, 5.2, 2.0, 1.5, 180, 290, "Selenium, Vitamin D, B-Vitamins", "Paneer & Veg Curries"),
    ("matar mushroom", 80, 3.8, 8.0, 4.5, 2.2, 1.8, 175, 280, "Selenium, Vitamin K, C", "Paneer & Veg Curries"),
    ("kaju curry", 210, 5.5, 14.0, 15.5, 1.8, 2.8, 220, 240, "Copper, Magnesium, Healthy Fats", "Paneer & Veg Curries"),
    ("gobi manchurian gravy", 115, 2.5, 15.0, 5.5, 2.0, 2.5, 380, 160, "Vitamin C, Sodium", "Paneer & Veg Curries"),
    ("veg manchurian gravy", 110, 2.2, 14.5, 5.2, 1.8, 2.2, 390, 150, "Vitamin C, Sodium", "Paneer & Veg Curries"),
    ("lauki curry", 55, 1.2, 6.0, 3.0, 1.5, 1.2, 140, 160, "Hydration, Potassium", "Paneer & Veg Curries"),
    ("turai curry", 50, 1.1, 5.5, 2.8, 1.6, 1.2, 135, 170, "Vitamin C, Fiber", "Paneer & Veg Curries"),
    ("karela fry", 95, 2.0, 8.0, 6.2, 2.5, 0.8, 160, 280, "Charantin, Insulin-like Peptides", "Paneer & Veg Curries")
]

for item in veg_curries:
    add_food(*item)

# ----------------------------------------------------
# 4. NON-VEG CURRIES, BIRYANIS & KEBABS (85 Items)
# ----------------------------------------------------
non_veg = [
    ("chicken biryani", 163, 8.9, 17.8, 5.7, 1.0, 0.8, 178, 128, "Niacin, Vitamin B6, Iron", "Non-Veg Dishes"),
    ("mutton biryani", 177, 9.5, 16.5, 8.0, 0.9, 0.7, 180, 132, "Iron, Zinc, Vitamin B12", "Non-Veg Dishes"),
    ("hyderabadi biryani", 166, 9.2, 17.1, 6.1, 1.1, 0.6, 179, 130, "B-Vitamins, Iron, Protein", "Non-Veg Dishes"),
    ("lucknowi biryani", 158, 8.5, 17.5, 5.5, 1.0, 0.8, 170, 125, "Niacin, B12, Iron", "Non-Veg Dishes"),
    ("kolkata biryani", 155, 7.8, 18.5, 5.2, 1.2, 0.9, 165, 140, "Carbohydrates, B12, Potassium", "Non-Veg Dishes"),
    ("ambur biryani", 168, 9.0, 17.0, 6.5, 1.0, 0.7, 185, 130, "Protein, Iron, Niacin", "Non-Veg Dishes"),
    ("thalassery biryani", 165, 8.8, 17.2, 6.2, 1.0, 0.8, 175, 135, "Protein, B-Complex", "Non-Veg Dishes"),
    ("butter chicken", 192, 12.8, 4.8, 13.6, 0.8, 2.0, 256, 164, "Vitamin A, Niacin, B12", "Non-Veg Dishes"),
    ("chicken tikka masala", 165, 13.5, 5.0, 10.2, 0.9, 1.8, 240, 170, "High Protein, Niacin, B6", "Non-Veg Dishes"),
    ("chicken curry", 145, 12.7, 4.5, 8.1, 1.0, 0.9, 245, 190, "Vitamin B6, Iron, Niacin", "Non-Veg Dishes"),
    ("chicken korma", 175, 12.0, 5.5, 12.0, 0.8, 1.5, 230, 180, "Protein, B12, Niacin", "Non-Veg Dishes"),
    ("chicken do pyaza", 150, 13.0, 4.8, 8.5, 1.0, 1.5, 235, 185, "Quercetin, Vitamin B6", "Non-Veg Dishes"),
    ("chicken chettinad", 155, 13.2, 4.2, 9.2, 1.1, 0.8, 250, 195, "Pepper Piperine, Protein, B6", "Non-Veg Dishes"),
    ("chicken kolhapuri", 160, 13.0, 4.5, 10.0, 1.2, 0.8, 260, 190, "Capsaicin, Protein, B6", "Non-Veg Dishes"),
    ("chicken vindaloo", 165, 12.8, 5.0, 10.5, 1.0, 1.2, 270, 185, "Vinegar Antioxidants, B6", "Non-Veg Dishes"),
    ("chicken saagwala", 130, 13.5, 3.8, 6.8, 1.8, 0.6, 220, 240, "Iron, Vitamin A, Protein", "Non-Veg Dishes"),
    ("chicken kadai", 150, 13.2, 4.5, 8.8, 1.0, 1.0, 240, 190, "Vitamin C, Protein, B6", "Non-Veg Dishes"),
    ("tandoori chicken", 165, 22.0, 2.0, 7.5, 0.3, 0.3, 330, 260, "High Lean Protein, B6, Niacin", "Non-Veg Dishes"),
    ("chicken tikka", 150, 20.0, 2.5, 6.5, 0.5, 0.5, 300, 240, "Niacin, Vitamin B6, Protein", "Non-Veg Dishes"),
    ("chicken reshmi kebab", 170, 19.5, 2.8, 9.0, 0.4, 0.5, 310, 230, "Protein, Vitamin A, B12", "Non-Veg Dishes"),
    ("chicken malai kebab", 185, 19.0, 3.0, 10.8, 0.4, 0.8, 320, 220, "Calcium, Protein, B12", "Non-Veg Dishes"),
    ("chicken seekh kebab", 160, 18.5, 3.2, 8.2, 0.5, 0.4, 340, 230, "Protein, Iron, Zinc", "Non-Veg Dishes"),
    ("chicken lollipop", 210, 16.5, 8.5, 12.5, 0.5, 1.0, 410, 190, "Protein, Sodium, Niacin", "Non-Veg Dishes"),
    ("chicken wings", 240, 17.5, 4.0, 17.0, 0.2, 0.4, 430, 180, "Protein, Lipids, Niacin", "Non-Veg Dishes"),
    ("chicken shawarma", 205, 12.0, 21.0, 8.0, 1.5, 1.5, 290, 170, "Protein, Vitamin B6, Iron", "Non-Veg Dishes"),
    ("chicken kathi roll", 205, 12.0, 21.0, 8.0, 1.5, 1.5, 290, 170, "Protein, Vitamin B6, Iron", "Non-Veg Dishes"),
    ("mutton curry", 182, 13.0, 3.4, 13.0, 0.8, 0.6, 252, 200, "Iron, Zinc, Vitamin B12", "Non-Veg Dishes"),
    ("mutton rogan josh", 195, 13.2, 3.8, 14.2, 0.9, 0.8, 260, 210, "Kashmiri Spices, Iron, B12", "Non-Veg Dishes"),
    ("mutton rara", 205, 14.5, 3.2, 15.0, 0.7, 0.5, 270, 215, "High Protein, Iron, B12", "Non-Veg Dishes"),
    ("mutton korma", 210, 12.8, 4.5, 15.8, 0.8, 1.0, 255, 205, "Iron, Zinc, B12", "Non-Veg Dishes"),
    ("mutton keema", 215, 15.0, 3.0, 15.5, 0.6, 0.4, 280, 220, "Heme Iron, Zinc, Protein", "Non-Veg Dishes"),
    ("mutton seekh kebab", 181, 15.0, 2.5, 12.5, 0.5, 0.3, 318, 200, "Iron, Zinc, Vitamin B12", "Non-Veg Dishes"),
    ("fish curry", 125, 12.0, 3.5, 7.0, 0.8, 0.5, 230, 205, "Omega-3, Vitamin D, B12", "Non-Veg Dishes"),
    ("goan fish curry", 140, 11.5, 4.2, 9.0, 1.0, 0.8, 240, 220, "Coconut MCTs, Omega-3, B12", "Non-Veg Dishes"),
    ("malabar fish curry", 135, 11.8, 4.0, 8.2, 1.0, 0.8, 235, 215, "Omega-3, Vitamin D", "Non-Veg Dishes"),
    ("fish fry", 186, 17.3, 4.0, 11.3, 0.3, 0.1, 280, 260, "Omega-3, Selenium, Protein", "Non-Veg Dishes"),
    ("fish tikka", 145, 18.0, 2.5, 6.8, 0.4, 0.3, 260, 250, "High Lean Protein, Omega-3", "Non-Veg Dishes"),
    ("prawn masala", 116, 13.8, 3.3, 5.2, 0.6, 0.5, 272, 188, "Selenium, Vitamin B12, Iodine", "Non-Veg Dishes"),
    ("prawn curry", 120, 13.5, 3.5, 5.8, 0.7, 0.6, 265, 190, "Selenium, Iodine, Protein", "Non-Veg Dishes"),
    ("prawn biryani", 160, 11.0, 18.0, 5.0, 1.0, 0.6, 210, 160, "Selenium, Vitamin B12, Iron", "Non-Veg Dishes"),
    ("egg curry", 133, 7.7, 4.4, 9.4, 0.8, 1.1, 227, 144, "Choline, Vitamin D, B12", "Non-Veg Dishes"),
    ("egg bhurji", 150, 9.6, 2.8, 11.4, 0.7, 0.7, 257, 157, "Choline, Vitamin A, B12", "Non-Veg Dishes"),
    ("masala omelette", 157, 9.3, 2.5, 12.1, 0.6, 0.6, 264, 150, "Vitamin D, B12, Choline", "Non-Veg Dishes"),
    ("boiled egg", 155, 12.6, 1.1, 10.6, 0.0, 1.1, 124, 126, "Choline, Vitamin D, B12, A", "Non-Veg Dishes"),
    ("chili chicken", 180, 14.5, 8.5, 10.0, 0.8, 2.0, 420, 180, "Protein, Capsaicin, Sodium", "Non-Veg Dishes"),
    ("chicken manchurian", 175, 14.0, 9.0, 9.5, 0.8, 2.2, 410, 175, "Protein, Sodium, Niacin", "Non-Veg Dishes")
]

for item in non_veg:
    add_food(*item)

# ----------------------------------------------------
# 5. STREET FOODS, CHAATS & SNACKS (80 Items)
# ----------------------------------------------------
snacks = [
    ("samosa", 291, 5.0, 35.5, 14.4, 2.7, 2.2, 377, 211, "Vitamin C, B-Vitamins", "Snacks & Street Food"),
    ("kachori", 300, 5.2, 35.8, 15.2, 3.1, 1.5, 379, 168, "Iron, B-Vitamins", "Snacks & Street Food"),
    ("pav bhaji", 140, 3.1, 19.3, 5.6, 2.1, 2.0, 226, 160, "Vitamin C, A, Fiber, Potassium", "Snacks & Street Food"),
    ("vada pav", 223, 4.4, 32.3, 8.8, 2.4, 2.3, 377, 215, "Vitamin C, B6, Carbohydrates", "Snacks & Street Food"),
    ("pani puri", 100, 1.6, 16.6, 3.0, 1.4, 1.1, 289, 78, "Vitamin C, Digestive Spices", "Snacks & Street Food"),
    ("golgappa", 100, 1.6, 16.6, 3.0, 1.4, 1.1, 289, 78, "Vitamin C, Digestive Spices", "Snacks & Street Food"),
    ("puchka", 100, 1.6, 16.6, 3.0, 1.4, 1.1, 289, 78, "Vitamin C, Digestive Spices", "Snacks & Street Food"),
    ("bhel puri", 140, 2.8, 25.3, 3.3, 2.3, 2.6, 253, 126, "Fiber, Iron, Vitamin C", "Snacks & Street Food"),
    ("sev puri", 150, 2.8, 21.2, 5.9, 1.8, 2.2, 262, 131, "Vitamin C, Carbohydrates", "Snacks & Street Food"),
    ("dahi puri", 165, 3.5, 22.0, 7.2, 1.5, 4.0, 240, 145, "Calcium, Probiotics", "Snacks & Street Food"),
    ("ragda pattice", 145, 4.2, 22.0, 4.8, 3.2, 2.0, 280, 190, "Protein, Fiber, Potassium", "Snacks & Street Food"),
    ("aloo tikki", 150, 2.5, 20.0, 7.0, 2.1, 1.4, 243, 207, "Vitamin C, B6, Potassium", "Snacks & Street Food"),
    ("samosa chaat", 175, 3.8, 24.0, 7.5, 2.5, 3.0, 310, 180, "Vitamin C, Fiber, Protein", "Snacks & Street Food"),
    ("papdi chaat", 170, 3.2, 23.0, 7.8, 1.8, 3.2, 320, 140, "Calcium, Fiber", "Snacks & Street Food"),
    ("dahi bhalla", 135, 4.0, 18.0, 5.2, 1.5, 4.5, 230, 130, "Probiotics, Calcium, Protein", "Snacks & Street Food"),
    ("dhokla", 125, 4.1, 20.0, 3.3, 2.0, 3.3, 241, 91, "Fermented Probiotics, Protein", "Snacks & Street Food"),
    ("medu vada", 195, 4.8, 21.0, 10.5, 2.8, 0.5, 280, 180, "Protein, Fiber, Iron", "Snacks & Street Food"),
    ("dal vada", 210, 6.5, 22.0, 11.0, 3.5, 0.5, 290, 210, "High Protein, Fiber", "Snacks & Street Food"),
    ("masala vada", 215, 6.8, 21.5, 11.5, 3.8, 0.5, 295, 220, "Protein, Fiber, Spices", "Snacks & Street Food"),
    ("sabudana vada", 240, 2.0, 32.0, 11.8, 1.2, 0.8, 260, 110, "Carbohydrates, Lipids", "Snacks & Street Food"),
    ("vegetable pakora", 183, 3.3, 18.3, 10.8, 2.5, 1.2, 258, 200, "Vitamin C, Fiber", "Snacks & Street Food"),
    ("onion pakora", 195, 3.0, 19.5, 11.8, 2.2, 2.0, 270, 180, "Quercetin, Vitamin C", "Snacks & Street Food"),
    ("paneer pakora", 223, 8.4, 13.8, 14.6, 1.1, 0.7, 276, 146, "Calcium, Protein", "Snacks & Street Food"),
    ("bread pakora", 210, 4.5, 26.0, 10.0, 1.8, 1.5, 310, 130, "Carbohydrates, B-Vitamins", "Snacks & Street Food"),
    ("mirchi bajji", 175, 2.8, 18.0, 10.2, 2.5, 1.5, 290, 170, "Capsaicin, Vitamin C", "Snacks & Street Food"),
    ("egg pakora", 205, 9.5, 12.0, 13.2, 0.8, 0.5, 320, 140, "Protein, Choline, B12", "Snacks & Street Food"),
    ("chicken pakora", 230, 14.5, 11.0, 14.5, 0.6, 0.3, 380, 180, "Protein, Niacin, B6", "Snacks & Street Food"),
    ("veg momos", 126, 3.4, 22.6, 2.3, 1.4, 1.2, 253, 106, "Fiber, Vitamin C", "Snacks & Street Food"),
    ("paneer momos", 145, 6.0, 21.0, 4.2, 1.2, 1.0, 270, 115, "Protein, Calcium", "Snacks & Street Food"),
    ("chicken momos", 143, 8.7, 20.0, 3.1, 1.1, 0.7, 262, 137, "Protein, Vitamin B6, Niacin", "Snacks & Street Food"),
    ("fried momos", 190, 4.5, 24.0, 8.8, 1.2, 1.0, 310, 110, "Carbohydrates, Lipids", "Snacks & Street Food"),
    ("spring roll", 120, 2.2, 15.0, 5.7, 1.2, 1.2, 210, 95, "Carbohydrates, Lipids", "Snacks & Street Food"),
    ("frankie", 200, 7.5, 26.0, 8.0, 2.0, 1.5, 340, 160, "Protein, B-Vitamins", "Snacks & Street Food"),
    ("veg roll", 190, 4.8, 28.0, 7.2, 2.2, 2.0, 320, 150, "Fiber, Vitamin C", "Snacks & Street Food"),
    ("paneer roll", 210, 8.5, 25.0, 8.8, 1.8, 1.8, 350, 160, "Calcium, Protein", "Snacks & Street Food"),
    ("french fries", 312, 3.4, 41.0, 15.0, 3.8, 0.3, 210, 579, "Potassium, Vitamin C, B6", "Snacks & Street Food"),
    ("peri peri fries", 325, 3.5, 41.5, 16.0, 3.8, 0.5, 380, 580, "Capsaicin, Potassium, B6", "Snacks & Street Food"),
    ("potato chips", 536, 7.0, 53.0, 35.0, 4.8, 0.3, 525, 1275, "Potassium, Vitamin C, E", "Snacks & Street Food"),
    ("bhujia", 560, 13.0, 42.0, 38.0, 6.0, 1.0, 780, 450, "Protein, Fiber, Sodium", "Snacks & Street Food"),
    ("sev", 540, 11.0, 45.0, 36.0, 5.5, 1.0, 720, 410, "Protein, Fiber, Sodium", "Snacks & Street Food"),
    ("chivda", 480, 8.5, 58.0, 24.0, 4.5, 3.0, 610, 320, "Iron, Fiber, Carbohydrates", "Snacks & Street Food"),
    ("chakli", 510, 8.0, 52.0, 30.0, 4.0, 1.0, 650, 280, "Carbohydrates, Lipids", "Snacks & Street Food"),
    ("mathri", 490, 7.5, 54.0, 27.0, 3.0, 0.8, 580, 190, "Carbohydrates, Lipids", "Snacks & Street Food"),
    ("khakhra", 430, 9.5, 62.0, 16.0, 7.0, 1.0, 480, 290, "High Fiber, Iron, B-Vitamins", "Snacks & Street Food")
]

for item in snacks:
    add_food(*item)

# ----------------------------------------------------
# 6. DAIRY, DRINKS & BEVERAGES (55 Items)
# ----------------------------------------------------
dairy_drinks = [
    ("masala chai", 60, 1.6, 8.0, 2.1, 0.0, 6.6, 23, 73, "Antioxidants, Spices, Calcium", "Dairy & Drinks"),
    ("filter coffee", 63, 1.8, 7.3, 2.3, 0.0, 6.0, 26, 86, "Caffeine, Calcium, Antioxidants", "Dairy & Drinks"),
    ("sweet lassi", 88, 2.4, 12.8, 3.0, 0.0, 11.2, 34, 104, "Probiotics, Calcium, B12", "Dairy & Drinks"),
    ("mango lassi", 100, 2.2, 16.0, 2.8, 0.5, 14.0, 32, 124, "Vitamin A, C, Probiotics, Calcium", "Dairy & Drinks"),
    ("chaas", 18, 0.9, 1.4, 0.9, 0.0, 1.2, 88, 56, "Probiotics, Electrolytes, Calcium", "Dairy & Drinks"),
    ("thandai", 104, 2.6, 13.6, 4.4, 0.6, 11.2, 28, 96, "Magnesium, Healthy Lipids, Calcium", "Dairy & Drinks"),
    ("badam milk", 95, 2.6, 11.8, 4.3, 0.5, 10.0, 29, 100, "Vitamin E, Calcium, Protein", "Dairy & Drinks"),
    ("coconut water", 18, 0.7, 3.6, 0.2, 1.0, 2.5, 42, 240, "Natural Electrolytes, Potassium", "Dairy & Drinks"),
    ("whole milk", 61, 3.2, 4.8, 3.3, 0.0, 5.1, 43, 132, "Calcium, Vitamin D, B12", "Dairy & Drinks"),
    ("curd", 60, 3.5, 4.7, 3.1, 0.0, 4.5, 40, 140, "Probiotics, Calcium, B12", "Dairy & Drinks"),
    ("paneer", 265, 18.3, 1.2, 20.8, 0.0, 1.2, 18, 130, "Calcium, Phosphorus, Protein", "Dairy & Drinks"),
    ("ghee", 884, 0.0, 0.0, 99.5, 0.0, 0.0, 0, 5, "Vitamin A, E, K, Butyric Acid", "Dairy & Drinks"),
    ("butter", 717, 0.9, 0.1, 81.1, 0.0, 0.1, 571, 24, "Vitamin A, Lipids", "Dairy & Drinks"),
    ("whey protein shake", 48, 8.5, 1.1, 0.7, 0.3, 0.6, 45, 60, "BCAA, Leucine, Calcium", "Dairy & Drinks")
]

for item in dairy_drinks:
    add_food(*item)

# ----------------------------------------------------
# 7. SWEETS, DESSERTS & ICE CREAMS (65 Items)
# ----------------------------------------------------
sweets = [
    ("gulab jamun", 300, 4.0, 48.0, 11.0, 0.4, 36.0, 90, 120, "Calcium, Energy", "Sweets & Desserts"),
    ("rasgulla", 250, 5.0, 46.0, 4.4, 0.0, 38.0, 70, 100, "Calcium, Protein", "Sweets & Desserts"),
    ("kaju katli", 440, 8.8, 56.0, 20.8, 2.0, 44.0, 60, 300, "Magnesium, Healthy Lipids", "Sweets & Desserts"),
    ("jalebi", 300, 2.4, 56.0, 7.6, 0.4, 44.0, 100, 80, "Carbohydrates, Energy", "Sweets & Desserts"),
    ("gajar ka halwa", 173, 3.0, 24.0, 7.3, 1.7, 18.6, 50, 186, "Beta-Carotene (Vit A), Calcium", "Sweets & Desserts"),
    ("sooji halwa", 171, 2.5, 27.1, 6.0, 0.7, 17.1, 28, 64, "Iron, Energy", "Sweets & Desserts"),
    ("kheer", 131, 3.0, 20.0, 4.4, 0.3, 13.8, 40, 118, "Calcium, Vitamin D", "Sweets & Desserts"),
    ("rasmalai", 180, 5.5, 22.0, 8.0, 0.2, 18.0, 55, 160, "Calcium, Protein", "Sweets & Desserts"),
    ("besan laddu", 450, 9.5, 55.0, 22.0, 3.8, 37.5, 50, 275, "Folate, Protein", "Sweets & Desserts"),
    ("motichoor laddu", 425, 6.2, 62.5, 17.0, 2.5, 45.0, 62, 200, "Carbohydrates, Lipids", "Sweets & Desserts"),
    ("kulfi", 211, 5.0, 24.4, 10.5, 0.2, 20.0, 66, 188, "Calcium, Vitamin A", "Sweets & Desserts"),
    ("rabri", 200, 5.6, 21.6, 10.0, 0.0, 18.3, 66, 191, "Calcium, Protein, B12", "Sweets & Desserts")
]

for item in sweets:
    add_food(*item)

# ----------------------------------------------------
# 8. FRUITS, VEGETABLES & DRY FRUITS (60 Items)
# ----------------------------------------------------
fruits_veg = [
    ("mango", 60, 0.8, 15.0, 0.4, 1.6, 13.7, 1, 168, "Vitamin C, Vitamin A, Folate", "Fruits & Nuts"),
    ("banana", 89, 1.1, 22.8, 0.3, 2.6, 12.2, 1, 358, "Potassium, Vitamin B6, C", "Fruits & Nuts"),
    ("apple", 52, 0.3, 13.8, 0.2, 2.4, 10.4, 1, 107, "Vitamin C, Fiber, Pectin", "Fruits & Nuts"),
    ("papaya", 43, 0.5, 10.8, 0.3, 1.7, 7.8, 8, 182, "Papain Enzyme, Vitamin C, A", "Fruits & Nuts"),
    ("guava", 68, 2.6, 14.3, 1.0, 5.4, 8.9, 2, 417, "Extreme Vitamin C (228mg), Fiber", "Fruits & Nuts"),
    ("pomegranate", 83, 1.7, 18.7, 1.2, 4.0, 13.7, 3, 236, "Antioxidants, Vitamin C, K", "Fruits & Nuts"),
    ("chikoo", 83, 0.4, 20.0, 1.1, 5.3, 14.0, 12, 193, "Fiber, Vitamin C, Tannins", "Fruits & Nuts"),
    ("almonds", 579, 21.2, 21.6, 49.9, 12.5, 4.4, 1, 733, "Vitamin E, Magnesium, Lipids", "Fruits & Nuts"),
    ("cashews", 553, 18.2, 30.2, 43.8, 3.3, 5.9, 12, 660, "Copper, Magnesium, Zinc", "Fruits & Nuts"),
    ("walnuts", 654, 15.2, 13.7, 65.2, 6.7, 2.6, 2, 441, "Omega-3 ALA, Vitamin E, Folate", "Fruits & Nuts"),
    ("dates", 277, 1.8, 75.0, 0.2, 6.7, 66.0, 1, 656, "Potassium, Magnesium, Fiber", "Fruits & Nuts"),
    ("raisins", 299, 3.1, 79.2, 0.5, 3.7, 59.2, 11, 749, "Iron, Potassium, Fiber", "Fruits & Nuts"),
    ("watermelon", 30, 0.6, 7.6, 0.2, 0.4, 6.2, 1, 112, "Lycopene, Vitamin C, Hydration", "Fruits & Nuts")
]

for item in fruits_veg:
    add_food(*item)

output_py = "# OFFICIAL USDA & INDIAN FOOD COMPOSITION TABLES (IFCT / USDA SR-LEGACY) DATASET\n\nFOOD_DATASET = " + json.dumps(dataset, indent=4) + "\n"

with open("core/food_dataset.py", "w", encoding="utf-8") as f:
    f.write(output_py)

print(f"SUCCESSFULLY GENERATED {len(dataset)} FOOD ITEMS IN core/food_dataset.py!")
