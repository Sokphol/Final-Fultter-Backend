"""
Database seeder — populates the DB with demo data for development.
Run: python seed.py
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.brand import Brand
from app.models.product import Product, ProductImage, ProductVariant
from app.models.cart import Cart
from app.utils.security import hash_password
from app.utils.slugify import slugify


app = create_app("development")

with app.app_context():
    db.create_all()
    print("[OK] Tables ready.")

    # ── Admin user ────────────────────────────────────────────────
    admin = User.query.filter_by(email="admin@headphoneshop.com").first()
    if not admin:
        admin = User(
            name="Admin",
            email="admin@headphoneshop.com",
            password_hash=hash_password("admin123"),
            role="admin",
            phone="+855 12 345 678",
        )
        db.session.add(admin)

    customer = User.query.filter_by(email="john@example.com").first()
    if not customer:
        customer = User(
            name="John Doe",
            email="john@example.com",
            password_hash=hash_password("password123"),
            role="customer",
            phone="+855 98 765 432",
        )
        db.session.add(customer)
    db.session.flush()

    for user in (admin, customer):
        if not Cart.query.filter_by(user_id=user.id).first():
            db.session.add(Cart(user_id=user.id))
    print("[OK] Users seeded.")

    # ── Categories ────────────────────────────────────────────────
    cats = [
        ("Over-Ear", "Full-size headphones for immersive sound."),
        ("Studio Open-Back", "Open-back reference headphones."),
        ("True Wireless", "Completely wireless earbuds."),
        ("Gaming", "Headphones optimized for gaming."),
        ("IEMs", "In-ear monitors for detailed listening."),
        ("DAC/Amps", "Digital-to-analog converters and headphone amplifiers."),
        ("Accessory", "Cables and replacement parts."),
    ]
    cats = [
        Category.query.filter_by(name=name).first()
        or Category(
            name=name,
            slug=slugify(name),
            description=description,
            is_active=True,
        )
        for name, description in cats
    ]
    db.session.add_all([category for category in cats if category.id is None])
    db.session.flush()
    print("[OK] Categories seeded.")

    # ── Brands ───────────────────────────────────────────────────
    brands = [
        ("SonicFlow", "Considered sound for wherever life takes you."),
        ("Auralis", "Reference audio for focused listening."),
        ("Northstar", "Clear, confident sound for every day."),
        ("SonicFlow Accessories", "Cables and accessories for your listening setup."),
    ]
    brands = [
        Brand.query.filter_by(name=name).first()
        or Brand(
            name=name,
            slug=slugify(name),
            description=description,
            is_active=True,
        )
        for name, description in brands
    ]
    db.session.add_all([brand for brand in brands if brand.id is None])
    db.session.flush()
    print("[OK] Brands seeded.")

    # ── Products ──────────────────────────────────────────────────
    products_data = [
        {
            "slug": "apex-anc-pro",
            "name": "SonicFlow Apex ANC Pro",
            "description": "A reference-grade planar flagship with adaptive hybrid cancellation and lossless wireless audio, tuned for long listening sessions.",
            "short_description": "Silence the world. Hear everything.",
            "sku": "SONICFLOW-APEX-ANC-PRO",
            "price": 499,
            "sale_price": 449,
            "stock_quantity": 50,
            "brand": "SonicFlow",
            "category": "Over-Ear",
            "is_featured": True,
            "average_rating": 4.9,
            "review_count": 284,
            "sold_count": 284,
            "connectivity": "Bluetooth 5.4 / LDAC / USB-C",
            "driver_size": "50mm planar magnetic",
            "frequency_response": "5Hz - 48kHz",
            "impedance": "32 Ohm",
            "battery_life": "60 hours",
            "noise_cancellation": True,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Obsidian", "#252831"), ("Champagne", "#D4AF37"), ("Cloud", "#E4E5E8")],
        },
        {
            "slug": "muse-700",
            "name": "Muse Studio 700",
            "description": "Open-back reference headphones with a natural soundstage and hand-matched dynamic drivers for critical listening.",
            "short_description": "Every detail, in its place.",
            "sku": "AURALIS-MUSE-700",
            "price": 379,
            "sale_price": 329,
            "stock_quantity": 25,
            "brand": "Auralis",
            "category": "Studio Open-Back",
            "is_featured": True,
            "average_rating": 4.8,
            "review_count": 192,
            "sold_count": 192,
            "connectivity": "Wired",
            "driver_size": "Dynamic open-back",
            "frequency_response": "8Hz - 42kHz",
            "impedance": "300 Ohm",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Graphite", "#4B4D52"), ("Silver", "#B9BDC4")],
        },
        {
            "slug": "pulse-buds",
            "name": "Pulse Buds Studio",
            "description": "Compact true wireless monitors with adaptive ANC, a low-latency studio mode, and an all-day charging case.",
            "short_description": "Pocket-sized precision.",
            "sku": "SONICFLOW-PULSE-BUDS",
            "price": 219,
            "sale_price": 189,
            "stock_quantity": 60,
            "brand": "SonicFlow",
            "category": "True Wireless",
            "is_featured": True,
            "average_rating": 4.7,
            "review_count": 326,
            "sold_count": 326,
            "connectivity": "Bluetooth 5.4 / LDAC",
            "driver_size": "10mm dynamic",
            "frequency_response": "20Hz - 20kHz",
            "impedance": "16 Ohm",
            "battery_life": "32 hours",
            "noise_cancellation": True,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Ink", "#202127"), ("Sage", "#84917D"), ("Ivory", "#E3DED3")],
        },
        {
            "slug": "arena-x",
            "name": "Arena X Wireless",
            "description": "A low-latency gaming headset with a broadcast-ready detachable mic and spatial audio profiles.",
            "short_description": "Hear the move before it happens.",
            "sku": "NORTHSTAR-ARENA-X",
            "price": 249,
            "sale_price": None,
            "stock_quantity": 35,
            "brand": "Northstar",
            "category": "Gaming",
            "is_featured": False,
            "average_rating": 4.6,
            "review_count": 148,
            "sold_count": 148,
            "connectivity": "Bluetooth / 2.4GHz wireless",
            "driver_size": "50mm dynamic",
            "frequency_response": "10Hz - 28kHz",
            "impedance": "32 Ohm",
            "battery_life": "40 hours",
            "noise_cancellation": False,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1599669454699-248893623440?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Black / Orange", "#292A2E"), ("White", "#E1E2E4")],
        },
        {
            "slug": "atelier-planar",
            "name": "Atelier Planar One",
            "description": "Lightweight planar open-backs built for an expansive, even-handed presentation at the desk.",
            "short_description": "A wider window into the mix.",
            "sku": "AURALIS-ATELIER-PLANAR",
            "price": 599,
            "sale_price": None,
            "stock_quantity": 16,
            "brand": "Auralis",
            "category": "Studio Open-Back",
            "is_featured": False,
            "average_rating": 4.9,
            "review_count": 86,
            "sold_count": 86,
            "connectivity": "Wired",
            "driver_size": "Planar magnetic",
            "frequency_response": "6Hz - 50kHz",
            "impedance": "32 Ohm",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Midnight", "#292B33"), ("Brushed Silver", "#B7BAC0")],
        },
        {
            "slug": "roam-anc",
            "name": "Roam ANC 45",
            "description": "Fold-flat wireless headphones with adaptive cancellation, multipoint Bluetooth, and a warm, energetic tuning.",
            "short_description": "Quiet confidence, anywhere.",
            "sku": "SONICFLOW-ROAM-ANC-45",
            "price": 319,
            "sale_price": 279,
            "stock_quantity": 40,
            "brand": "SonicFlow",
            "category": "Over-Ear",
            "is_featured": False,
            "average_rating": 4.5,
            "review_count": 211,
            "sold_count": 211,
            "connectivity": "Bluetooth 5.3 / AAC",
            "driver_size": "40mm dynamic",
            "frequency_response": "10Hz - 25kHz",
            "impedance": "28 Ohm",
            "battery_life": "45 hours",
            "noise_cancellation": True,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Carbon", "#262830"), ("Stone", "#B6ADA0")],
        },
        {
            "slug": "echo-mini",
            "name": "Echo Mini Buds",
            "description": "Everyday wireless earbuds with clear calls, pocket-friendly charging, and a lively balanced sound.",
            "short_description": "Small case. Big character.",
            "sku": "NORTHSTAR-ECHO-MINI",
            "price": 119,
            "sale_price": None,
            "stock_quantity": 75,
            "brand": "Northstar",
            "category": "True Wireless",
            "is_featured": True,
            "average_rating": 4.4,
            "review_count": 409,
            "sold_count": 409,
            "connectivity": "Bluetooth 5.3 / AAC",
            "driver_size": "8mm dynamic",
            "frequency_response": "20Hz - 20kHz",
            "impedance": "16 Ohm",
            "battery_life": "24 hours",
            "noise_cancellation": False,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Black", "#24252A"), ("Coral", "#B86B58")],
        },
        {
            "slug": "studio-classic",
            "name": "Studio Classic 80",
            "description": "Closed-back monitoring headphones with dependable isolation, replaceable parts, and an honest studio response.",
            "short_description": "Made for the work behind the music.",
            "sku": "AURALIS-STUDIO-CLASSIC-80",
            "price": 179,
            "sale_price": 159,
            "stock_quantity": 45,
            "brand": "Auralis",
            "category": "Over-Ear",
            "is_featured": False,
            "average_rating": 4.6,
            "review_count": 173,
            "sold_count": 173,
            "connectivity": "Wired",
            "driver_size": "45mm dynamic",
            "frequency_response": "8Hz - 30kHz",
            "impedance": "80 Ohm",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1599669454699-248893623440?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Studio Black", "#24252A"), ("Grey", "#777A80")],
        },
        {
            "slug": "sonic-arc-48",
            "name": "SonicFlow Arc 48",
            "description": "Premium wireless headphones with adaptive noise cancellation, natural transparency, and a balanced high-resolution sound.",
            "short_description": "A quieter way to travel.",
            "sku": "SONICFLOW-ARC-48",
            "price": 429,
            "sale_price": 389,
            "stock_quantity": 32,
            "brand": "SonicFlow",
            "category": "Over-Ear",
            "is_featured": False,
            "average_rating": 4.8,
            "review_count": 134,
            "sold_count": 134,
            "connectivity": "Bluetooth 5.4 / LDAC / USB-C",
            "driver_size": "45mm dynamic",
            "frequency_response": "5Hz - 40kHz",
            "impedance": "32 Ohm",
            "battery_life": "48 hours",
            "noise_cancellation": True,
            "microphone": True,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Midnight Black", "#17191E"), ("Titanium Silver", "#B8BBC2"), ("Warm Sand", "#B5A58D")],
        },
        {
            "slug": "reference-iem-one",
            "name": "Reference IEM One",
            "description": "Compact in-ear monitors with a balanced armature and dynamic driver tuned for precise, effortless detail.",
            "short_description": "Your own front-row seat.",
            "sku": "AURALIS-REFERENCE-IEM-ONE",
            "price": 279,
            "sale_price": None,
            "stock_quantity": 28,
            "brand": "Auralis",
            "category": "IEMs",
            "is_featured": False,
            "average_rating": 4.8,
            "review_count": 96,
            "sold_count": 96,
            "connectivity": "Wired",
            "driver_size": "Hybrid 1DD + 2BA",
            "frequency_response": "10Hz - 40kHz",
            "impedance": "18 Ohm",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Obsidian", "#252831"), ("Silver", "#B9BDC4")],
        },
        {
            "slug": "meridian-dac-one",
            "name": "Meridian DAC One",
            "description": "A pocket-sized USB DAC and headphone amplifier with a clean output stage for high-resolution listening.",
            "short_description": "Every source, brought into focus.",
            "sku": "SONICFLOW-MERIDIAN-DAC-ONE",
            "price": 229,
            "sale_price": 199,
            "stock_quantity": 30,
            "brand": "SonicFlow",
            "category": "DAC/Amps",
            "is_featured": False,
            "average_rating": 4.7,
            "review_count": 72,
            "sold_count": 72,
            "connectivity": "USB-C / USB Audio",
            "driver_size": "Dual ESS ES9219",
            "frequency_response": "5Hz - 90kHz",
            "impedance": "16-300 Ohm",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Graphite", "#363941"), ("Titanium", "#B9BDC4")],
        },
        {
            "slug": "accessory-balanced-cable",
            "name": "4.4mm Balanced Silver Cable",
            "description": "A premium 4.4mm balanced headphone cable.",
            "short_description": "A balanced connection.",
            "sku": "ACCESSORY-BALANCED-CABLE",
            "price": 49,
            "sale_price": None,
            "stock_quantity": 100,
            "brand": "SonicFlow Accessories",
            "category": "Accessory",
            "is_featured": False,
            "average_rating": 5,
            "review_count": 0,
            "sold_count": 0,
            "connectivity": "Wired",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Silver", "#C0C0C0")],
        },
        {
            "slug": "accessory-velour-pads",
            "name": "Velour Ear Pads",
            "description": "A pair of breathable replacement velour ear pads.",
            "short_description": "Comfort for longer sessions.",
            "sku": "ACCESSORY-VELOUR-PADS",
            "price": 29,
            "sale_price": None,
            "stock_quantity": 100,
            "brand": "SonicFlow Accessories",
            "category": "Accessory",
            "is_featured": False,
            "average_rating": 5,
            "review_count": 0,
            "sold_count": 0,
            "connectivity": "Wired",
            "noise_cancellation": False,
            "microphone": False,
            "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85",
            "colors": [("Black", "#24252A")],
        },
    ]

    brand_map = {b.name: b for b in brands}
    cat_map = {c.name: c for c in cats}

    for pd in products_data:
        colors = pd.pop("colors")
        image_url = pd.pop("image")
        brand_name = pd.pop("brand")
        category_name = pd.pop("category")
        product_slug = pd.pop("slug")

        if Product.query.filter_by(sku=pd["sku"]).first():
            continue

        product = Product(
            slug=product_slug,
            brand_id=brand_map[brand_name].id,
            category_id=cat_map[category_name].id,
            **pd,
        )
        db.session.add(product)
        db.session.flush()

        # Add a placeholder image
        img = ProductImage(
            product_id=product.id,
            image_url=image_url,
            is_primary=True,
            sort_order=0,
        )
        db.session.add(img)

        # Add variants
        for i, color_info in enumerate(colors):
            if isinstance(color_info, tuple):
                color_name, color_hex = color_info
            else:
                color_name, color_hex = color_info, None
            variant = ProductVariant(
                product_id=product.id,
                color_name=color_name,
                color_hex=color_hex,
                stock_quantity=10,
                price_adjustment=0.00,
            )
            db.session.add(variant)

    db.session.commit()
    print(f"[OK] {len(products_data)} demo products available.")
    print("\n[SUCCESS] Database seeded successfully!")
    print("\nAdmin credentials:")
    print("  Email   : admin@headphoneshop.com")
    print("  Password: admin123")
    print("\nCustomer credentials:")
    print("  Email   : john@example.com")
    print("  Password: password123")
