# ============================================================
# GIFT GENIE - GIFT RECOMMENDATION LOGIC
# ============================================================


def generate_gift_ideas(interest, budget):
    """
    Generate gift suggestions based on:
    - recipient interest
    - recipient budget

    Recommendation rules:
    1. Match the recipient's interest.
    2. Only show gifts that fit the budget.
    3. Higher budgets unlock higher-value gifts.
    4. Rank gifts according to the user's budget.
    5. Return up to 5 recommendations.
    """

    interest = str(interest).lower().strip()

    budget = float(budget)


    # ========================================================
    # GIFT CATALOG
    # ========================================================

    gift_catalog = {


        # ====================================================
        # SPORTS
        # ====================================================

        "sports": [

            {
                "name": "Sports Wristband",
                "description":
                    "A small and practical accessory for someone who enjoys sports.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Sports Socks",
                "description":
                    "A simple gift for someone who enjoys staying active.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Sports Towel",
                "description":
                    "A useful towel for workouts and sports activities.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Sports Water Bottle",
                "description":
                    "A practical bottle for workouts and outdoor activities.",
                "min_price": 25,
                "max_price": 45
            },

            {
                "name": "Sports Cap",
                "description":
                    "A useful accessory for outdoor sports activities.",
                "min_price": 30,
                "max_price": 50
            },

            {
                "name": "Resistance Bands",
                "description":
                    "A practical fitness accessory for home workouts.",
                "min_price": 35,
                "max_price": 60
            },

            {
                "name": "Sports T-shirt",
                "description":
                    "A comfortable shirt for sports and casual activities.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Sports Jersey",
                "description":
                    "A great gift for someone who enjoys sports.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Sports Bag",
                "description":
                    "A useful bag for carrying sports clothes and equipment.",
                "min_price": 60,
                "max_price": 120
            },

            {
                "name": "Sports Shoes",
                "description":
                    "A useful gift for someone who regularly enjoys sports.",
                "min_price": 100,
                "max_price": 200
            },

            {
                "name": "Fitness Tracker",
                "description":
                    "A practical device for tracking daily activity and exercise.",
                "min_price": 120,
                "max_price": 250
            },

            {
                "name": "Premium Sports Backpack",
                "description":
                    "A larger sports bag for carrying clothes and equipment.",
                "min_price": 150,
                "max_price": 300
            },

            {
                "name": "Advanced Fitness Watch",
                "description":
                    "A higher-value wearable for tracking fitness activities.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Premium Sports Equipment Set",
                "description":
                    "A complete collection of useful equipment for sports enthusiasts.",
                "min_price": 400,
                "max_price": 800
            }

        ],


        # ====================================================
        # GAMING
        # ====================================================

        "gaming": [

            {
                "name": "Gaming Keychain",
                "description":
                    "A small gaming-themed accessory.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Gaming Stickers",
                "description":
                    "Fun gaming-themed stickers for a laptop or gaming setup.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Controller Thumb Grips",
                "description":
                    "A small accessory that can improve controller comfort.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Gaming Mouse Pad",
                "description":
                    "A useful addition to a gaming setup.",
                "min_price": 20,
                "max_price": 40
            },

            {
                "name": "Gaming Gift Card",
                "description":
                    "Useful for purchasing games or digital items.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "RGB Desk Light",
                "description":
                    "A decorative light for improving a gaming setup.",
                "min_price": 40,
                "max_price": 80
            },

            {
                "name": "Gaming Mouse",
                "description":
                    "A useful gift for someone who enjoys gaming.",
                "min_price": 60,
                "max_price": 120
            },

            {
                "name": "Gaming Headset",
                "description":
                    "A useful accessory for gaming and entertainment.",
                "min_price": 80,
                "max_price": 180
            },

            {
                "name": "Mechanical Keyboard",
                "description":
                    "A practical upgrade for a gaming or computer setup.",
                "min_price": 100,
                "max_price": 220
            },

            {
                "name": "Gaming Controller",
                "description":
                    "A useful accessory for someone who enjoys playing games.",
                "min_price": 100,
                "max_price": 220
            },

            {
                "name": "Gaming Chair",
                "description":
                    "A larger upgrade for a comfortable gaming setup.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Gaming Monitor",
                "description":
                    "A useful display upgrade for a gaming setup.",
                "min_price": 300,
                "max_price": 700
            },

            {
                "name": "Premium Gaming Setup Upgrade",
                "description":
                    "A higher-value collection for improving a gaming setup.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # READING
        # ====================================================

        "reading": [

            {
                "name": "Personalized Bookmark",
                "description":
                    "A small but meaningful gift for a book lover.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Reading Journal",
                "description":
                    "A simple journal for recording books and reading progress.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Book Sleeve",
                "description":
                    "A useful cover for protecting books while travelling.",
                "min_price": 20,
                "max_price": 30
            },

            {
                "name": "Novel / Book",
                "description":
                    "A great choice for someone who enjoys reading.",
                "min_price": 30,
                "max_price": 50
            },

            {
                "name": "Bookstore Gift Card",
                "description":
                    "Lets them choose their own favourite book.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Reading Journal Set",
                "description":
                    "A thoughtful set for tracking reading progress.",
                "min_price": 35,
                "max_price": 60
            },

            {
                "name": "Reading Lamp",
                "description":
                    "A useful accessory for comfortable reading.",
                "min_price": 50,
                "max_price": 100
            },

            {
                "name": "E-Reader Accessories",
                "description":
                    "Useful accessories for someone who reads digitally.",
                "min_price": 60,
                "max_price": 120
            },

            {
                "name": "Premium Book Set",
                "description":
                    "A thoughtful collection for someone who loves reading.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Premium Book Collection",
                "description":
                    "A larger collection for a dedicated book lover.",
                "min_price": 120,
                "max_price": 220
            },

            {
                "name": "E-Reader",
                "description":
                    "A useful device for someone who enjoys digital reading.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Premium Reading Corner Set",
                "description":
                    "A larger collection for creating a cosy reading space.",
                "min_price": 300,
                "max_price": 600
            },

            {
                "name": "Deluxe Reading Collection",
                "description":
                    "A premium collection for a dedicated book lover.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # GARDENING
        # ====================================================

        "gardening": [

            {
                "name": "Small Plant",
                "description":
                    "A simple gift for someone who enjoys plants.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Mini Plant Pot",
                "description":
                    "A small decorative pot for their favourite plant.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Gardening Gloves",
                "description":
                    "A practical accessory for simple gardening tasks.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Indoor Plant",
                "description":
                    "A simple and thoughtful gift for plant lovers.",
                "min_price": 25,
                "max_price": 50
            },

            {
                "name": "Personalized Plant Pot",
                "description":
                    "A decorative gift for a gardening enthusiast.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Gardening Tool Set",
                "description":
                    "Useful tools for everyday gardening tasks.",
                "min_price": 35,
                "max_price": 70
            },

            {
                "name": "Plant Care Set",
                "description":
                    "Useful items for caring for indoor plants.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Gardening Starter Kit",
                "description":
                    "Useful tools for someone who enjoys gardening.",
                "min_price": 60,
                "max_price": 110
            },

            {
                "name": "Indoor Plant Set",
                "description":
                    "A collection of plants for someone who enjoys gardening.",
                "min_price": 70,
                "max_price": 130
            },

            {
                "name": "Premium Gardening Tool Set",
                "description":
                    "A larger collection of useful gardening tools.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Plant Display Set",
                "description":
                    "A decorative set for displaying plants at home.",
                "min_price": 120,
                "max_price": 220
            },

            {
                "name": "Indoor Garden System",
                "description":
                    "A larger setup for growing plants indoors.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Premium Indoor Garden Setup",
                "description":
                    "A higher-value setup for dedicated gardening enthusiasts.",
                "min_price": 400,
                "max_price": 800
            }

        ],


        # ====================================================
        # COOKING
        # ====================================================

        "cooking": [

            {
                "name": "Measuring Spoon Set",
                "description":
                    "A practical tool for cooking and baking.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Spice Jar Set",
                "description":
                    "A useful set for keeping spices organised.",
                "min_price": 20,
                "max_price": 30
            },

            {
                "name": "Recipe Book",
                "description":
                    "A collection of recipes to inspire new dishes.",
                "min_price": 20,
                "max_price": 35
            },

            {
                "name": "Personalized Apron",
                "description":
                    "A fun and useful gift for a cooking enthusiast.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Baking Set",
                "description":
                    "A useful set for someone who enjoys baking.",
                "min_price": 35,
                "max_price": 65
            },

            {
                "name": "Kitchen Storage Set",
                "description":
                    "Practical storage containers for an organised kitchen.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Cooking Utensil Set",
                "description":
                    "A practical set of everyday kitchen tools.",
                "min_price": 40,
                "max_price": 80
            },

            {
                "name": "Premium Cookware Set",
                "description":
                    "A useful gift for someone who enjoys cooking.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Kitchen Appliance",
                "description":
                    "A useful appliance for everyday cooking.",
                "min_price": 100,
                "max_price": 200
            },

            {
                "name": "Premium Baking Set",
                "description":
                    "A larger collection for someone who enjoys baking.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Premium Kitchen Set",
                "description":
                    "A larger collection of useful kitchen equipment.",
                "min_price": 180,
                "max_price": 300
            },

            {
                "name": "Premium Kitchen Appliance",
                "description":
                    "A higher-value appliance for a cooking enthusiast.",
                "min_price": 300,
                "max_price": 600
            },

            {
                "name": "Premium Kitchen Equipment Set",
                "description":
                    "A comprehensive collection of kitchen equipment.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # DANCING
        # ====================================================

        "dancing": [

            {
                "name": "Dance Hair Accessories",
                "description":
                    "Simple accessories suitable for dance practice.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Dance Socks",
                "description":
                    "A simple and useful gift for dance practice.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Dance Water Bottle",
                "description":
                    "A practical bottle for dance practices.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Dance Accessories Set",
                "description":
                    "A practical collection of accessories for dance practice.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Dance Bag",
                "description":
                    "A useful bag for carrying dance clothes and accessories.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Dance Practice Outfit",
                "description":
                    "Comfortable clothing suitable for dance practice.",
                "min_price": 50,
                "max_price": 80
            },

            {
                "name": "Dance Training Gear",
                "description":
                    "Useful equipment for dance exercises and practice.",
                "min_price": 50,
                "max_price": 90
            },

            {
                "name": "Dance Shoes",
                "description":
                    "A useful gift for someone who regularly enjoys dancing.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Dance Class Voucher",
                "description":
                    "A fun experience for someone who enjoys dancing.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Premium Dance Bag",
                "description":
                    "A larger bag for carrying dance clothes and accessories.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Dance Wear Set",
                "description":
                    "A comfortable outfit set suitable for regular practice.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Premium Dance Shoes",
                "description":
                    "A higher-value pair suitable for regular dance practice.",
                "min_price": 180,
                "max_price": 300
            },

            {
                "name": "Premium Dance Equipment Set",
                "description":
                    "A larger collection of useful items for dance practice.",
                "min_price": 400,
                "max_price": 800
            }

        ],


        # ====================================================
        # MUSIC
        # ====================================================

        "music": [

            {
                "name": "Music Notebook",
                "description":
                    "A simple notebook for music lovers.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Music Keychain",
                "description":
                    "A small accessory for someone who loves music.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Music Picks Set",
                "description":
                    "A simple accessory set for someone who plays guitar.",
                "min_price": 10,
                "max_price": 25
            },

            {
                "name": "Music Gift Card",
                "description":
                    "A flexible gift for someone who enjoys music.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Phone Speaker",
                "description":
                    "A compact speaker for enjoying music.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Music Accessories Set",
                "description":
                    "Useful small accessories for music lovers.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Mini Bluetooth Speaker",
                "description":
                    "A compact speaker for everyday listening.",
                "min_price": 50,
                "max_price": 80
            },

            {
                "name": "Wireless Headphones",
                "description":
                    "A useful gift for enjoying music anywhere.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Bluetooth Speaker",
                "description":
                    "A great option for someone who enjoys listening to music.",
                "min_price": 80,
                "max_price": 160
            },

            {
                "name": "Premium Headphones",
                "description":
                    "A higher-quality option for music listening.",
                "min_price": 120,
                "max_price": 250
            },

            {
                "name": "Portable Speaker",
                "description":
                    "A practical speaker for music at home or outdoors.",
                "min_price": 100,
                "max_price": 220
            },

            {
                "name": "Studio Headphones",
                "description":
                    "A higher-value option for focused music listening.",
                "min_price": 250,
                "max_price": 450
            },

            {
                "name": "Premium Audio Speaker",
                "description":
                    "A higher-value speaker for someone who enjoys music.",
                "min_price": 300,
                "max_price": 600
            },

            {
                "name": "Premium Audio Setup",
                "description":
                    "A larger audio setup for dedicated music lovers.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # ART & DRAWING
        # ====================================================

        "art & drawing": [

            {
                "name": "Sketchbook",
                "description":
                    "A simple gift for someone who enjoys drawing.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Drawing Pencils",
                "description":
                    "A useful set for everyday sketching.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Eraser & Pencil Set",
                "description":
                    "A small and practical drawing accessory set.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Drawing Set",
                "description":
                    "A useful set of drawing supplies.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Watercolour Set",
                "description":
                    "A creative gift for someone who enjoys painting.",
                "min_price": 30,
                "max_price": 70
            },

            {
                "name": "Sketching Set",
                "description":
                    "A practical set for sketching and drawing.",
                "min_price": 35,
                "max_price": 65
            },

            {
                "name": "Art Brush Set",
                "description":
                    "A useful collection of brushes for creative projects.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Premium Art Set",
                "description":
                    "A larger collection of art supplies.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Digital Drawing Tablet",
                "description":
                    "A useful tool for digital artists.",
                "min_price": 100,
                "max_price": 220
            },

            {
                "name": "Professional Drawing Set",
                "description":
                    "A more complete collection for serious artists.",
                "min_price": 120,
                "max_price": 220
            },

            {
                "name": "Painting Starter Kit",
                "description":
                    "A larger set for painting and creative projects.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Premium Digital Art Tablet",
                "description":
                    "A higher-value tool for digital artists.",
                "min_price": 300,
                "max_price": 600
            },

            {
                "name": "Professional Art Studio Set",
                "description":
                    "A comprehensive collection for dedicated artists.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # FASHION
        # ====================================================

        "fashion": [

            {
                "name": "Fashion Accessories",
                "description":
                    "A small accessory to complement their style.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Fashion Hair Accessories",
                "description":
                    "A simple accessory for completing an outfit.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Fashion Keychain",
                "description":
                    "A small stylish accessory for everyday use.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Fashion Gift Card",
                "description":
                    "Lets them choose something that matches their style.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Fashion Bag",
                "description":
                    "A stylish and practical everyday accessory.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Fashion Accessories Set",
                "description":
                    "A collection of accessories to complement their style.",
                "min_price": 35,
                "max_price": 70
            },

            {
                "name": "Minimalist Wallet",
                "description":
                    "A practical and stylish everyday accessory.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Premium Fashion Bag",
                "description":
                    "A stylish gift for someone interested in fashion.",
                "min_price": 80,
                "max_price": 160
            },

            {
                "name": "Fashion Store Voucher",
                "description":
                    "A flexible option for someone who enjoys fashion.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Premium Wallet",
                "description":
                    "A practical and stylish gift for everyday use.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Premium Accessories Set",
                "description":
                    "A stylish set of accessories for fashion lovers.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Premium Fashion Collection",
                "description":
                    "A higher-value selection for someone who enjoys fashion.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Luxury Fashion Gift Set",
                "description":
                    "A premium gift collection for a special occasion.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # TECHNOLOGY
        # ====================================================

        "technology": [

            {
                "name": "Phone Stand",
                "description":
                    "A useful accessory for everyday technology use.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Cable Organiser",
                "description":
                    "A practical accessory for keeping charging cables tidy.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Phone Grip",
                "description":
                    "A small accessory for more comfortable phone use.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Wireless Charger",
                "description":
                    "A practical accessory for compatible devices.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "USB Hub",
                "description":
                    "A useful accessory for connecting multiple devices.",
                "min_price": 35,
                "max_price": 70
            },

            {
                "name": "Power Bank",
                "description":
                    "A practical device for keeping phones charged on the go.",
                "min_price": 40,
                "max_price": 80
            },

            {
                "name": "Wireless Earbuds",
                "description":
                    "A useful technology gift for everyday use.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Smart Device",
                "description":
                    "A practical technology gift for everyday life.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Smartwatch",
                "description":
                    "A useful wearable device for everyday activities.",
                "min_price": 120,
                "max_price": 250
            },

            {
                "name": "Portable SSD",
                "description":
                    "A practical storage device for files and digital content.",
                "min_price": 120,
                "max_price": 250
            },

            {
                "name": "Tablet",
                "description":
                    "A versatile device for entertainment, study and everyday tasks.",
                "min_price": 300,
                "max_price": 600
            },

            {
                "name": "Laptop Accessories Set",
                "description":
                    "A useful collection for improving a computer setup.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Premium Smart Device",
                "description":
                    "A higher-value technology gift for everyday use.",
                "min_price": 400,
                "max_price": 800
            },

            {
                "name": "Premium Technology Bundle",
                "description":
                    "A larger collection of useful technology accessories and devices.",
                "min_price": 600,
                "max_price": 1000
            }

        ],


        # ====================================================
        # PHOTOGRAPHY
        # ====================================================

        "photography": [

            {
                "name": "Camera Strap",
                "description":
                    "A useful accessory for photography.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Lens Cleaning Kit",
                "description":
                    "A practical kit for keeping photography equipment clean.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Memory Card Case",
                "description":
                    "A small organiser for storing memory cards safely.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Mini Tripod",
                "description":
                    "A useful tool for taking stable photos.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Camera Accessories",
                "description":
                    "Useful accessories for photography enthusiasts.",
                "min_price": 30,
                "max_price": 70
            },

            {
                "name": "Camera Cleaning Set",
                "description":
                    "A practical set for maintaining camera equipment.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Phone Photography Kit",
                "description":
                    "Useful accessories for improving smartphone photography.",
                "min_price": 40,
                "max_price": 70
            },

            {
                "name": "Photography Bag",
                "description":
                    "A practical bag for carrying photography equipment.",
                "min_price": 70,
                "max_price": 130
            },

            {
                "name": "Tripod",
                "description":
                    "A useful tool for stable photography.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Camera Accessories Set",
                "description":
                    "A useful collection of accessories for photography.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Photography Lighting Kit",
                "description":
                    "Useful lighting equipment for better photos.",
                "min_price": 120,
                "max_price": 220
            },

            {
                "name": "Camera Backpack",
                "description":
                    "A protective and practical backpack for camera equipment.",
                "min_price": 100,
                "max_price": 200
            },

            {
                "name": "Mirrorless Camera",
                "description":
                    "A versatile camera for photography enthusiasts.",
                "min_price": 400,
                "max_price": 800
            },

            {
                "name": "Premium Photography Equipment Set",
                "description":
                    "A higher-value collection for serious photography enthusiasts.",
                "min_price": 600,
                "max_price": 1000
            }

        ],


        # ====================================================
        # TRAVELLING
        # ====================================================

        "travelling": [

            {
                "name": "Travel Tag",
                "description":
                    "A useful accessory for identifying luggage.",
                "min_price": 10,
                "max_price": 20
            },

            {
                "name": "Travel Organizer",
                "description":
                    "A small organizer for keeping travel items tidy.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Passport Cover",
                "description":
                    "A practical cover for keeping a passport protected.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Travel Bottle",
                "description":
                    "A practical item for travelling.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Travel Organizer Set",
                "description":
                    "Useful organizers for keeping travel belongings tidy.",
                "min_price": 30,
                "max_price": 70
            },

            {
                "name": "Travel Pillow",
                "description":
                    "A useful accessory for making trips more comfortable.",
                "min_price": 35,
                "max_price": 60
            },

            {
                "name": "Travel Toiletry Bag",
                "description":
                    "A practical bag for organising personal travel items.",
                "min_price": 35,
                "max_price": 70
            },

            {
                "name": "Travel Backpack",
                "description":
                    "A useful bag for trips and travelling.",
                "min_price": 70,
                "max_price": 150
            },

            {
                "name": "Travel Luggage",
                "description":
                    "A practical gift for someone who travels often.",
                "min_price": 100,
                "max_price": 200
            },

            {
                "name": "Premium Travel Bag",
                "description":
                    "A stylish and practical bag for frequent travellers.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Travel Set",
                "description":
                    "A useful collection of accessories for travelling.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Premium Travel Backpack",
                "description":
                    "A larger and more durable backpack for frequent travelling.",
                "min_price": 180,
                "max_price": 350
            },

            {
                "name": "Premium Travel Luggage Set",
                "description":
                    "A larger luggage set for frequent travellers.",
                "min_price": 250,
                "max_price": 500
            },

            {
                "name": "Premium Travel Collection",
                "description":
                    "A comprehensive travel set for frequent travellers.",
                "min_price": 500,
                "max_price": 900
            }

        ],


        # ====================================================
        # BEAUTY & SELF-CARE
        # ====================================================

        "beauty & self-care": [

            {
                "name": "Self-care Mask Set",
                "description":
                    "A simple gift for relaxing and self-care.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Self-care Journal",
                "description":
                    "A simple journal for relaxation and personal reflection.",
                "min_price": 15,
                "max_price": 25
            },

            {
                "name": "Personal Care Pouch",
                "description":
                    "A practical pouch for carrying personal care items.",
                "min_price": 15,
                "max_price": 30
            },

            {
                "name": "Self-care Gift Set",
                "description":
                    "A thoughtful collection for relaxation and self-care.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Personalized Pouch",
                "description":
                    "A practical pouch for carrying personal items.",
                "min_price": 30,
                "max_price": 70
            },

            {
                "name": "Bath & Body Set",
                "description":
                    "A relaxing collection for everyday self-care.",
                "min_price": 35,
                "max_price": 70
            },

            {
                "name": "Self-care Accessories",
                "description":
                    "A collection of simple accessories for relaxation.",
                "min_price": 30,
                "max_price": 60
            },

            {
                "name": "Premium Self-care Set",
                "description":
                    "A larger self-care collection for relaxation.",
                "min_price": 70,
                "max_price": 130
            },

            {
                "name": "Self-care Spa Voucher",
                "description":
                    "A relaxing experience for someone who enjoys self-care.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Premium Bath & Body Set",
                "description":
                    "A larger collection for a relaxing self-care routine.",
                "min_price": 80,
                "max_price": 150
            },

            {
                "name": "Wellness Gift Set",
                "description":
                    "A thoughtful collection for relaxation and everyday wellness.",
                "min_price": 100,
                "max_price": 180
            },

            {
                "name": "Premium Wellness Set",
                "description":
                    "A larger collection for relaxation and wellness.",
                "min_price": 200,
                "max_price": 400
            },

            {
                "name": "Premium Wellness Experience",
                "description":
                    "A higher-value experience for relaxation and wellness.",
                "min_price": 400,
                "max_price": 800
            }

        ]

    }


    # ========================================================
    # CHECK INTEREST
    # ========================================================

    if interest not in gift_catalog:

        return []


    # ========================================================
    # FIND GIFTS THAT FIT THE BUDGET
    # ========================================================

    available_gifts = []


    for gift in gift_catalog[interest]:

        if gift["min_price"] <= budget:

            available_gifts.append(
                gift
            )


    # ========================================================
    # NO MATCHING GIFTS
    # ========================================================

    if not available_gifts:

        return []


    # ========================================================
    # RECOMMENDATION TARGET
    #
    # We do not simply choose the most expensive gift.
    #
    # The target is around 65% of the user's budget so
    # the recommendation still leaves some room for the user.
    # ========================================================

    target_price = budget * 0.65


    # ========================================================
    # SORT BY CLOSENESS TO TARGET
    # ========================================================

    available_gifts.sort(
        key=lambda gift:
            abs(
                (
                    gift["min_price"]
                    + gift["max_price"]
                ) / 2
                - target_price
            )
    )


    # ========================================================
    # ADD MORE VARIETY
    #
    # Avoid returning too many gifts with almost identical
    # price ranges when possible.
    # ========================================================

    suggestions = []


    used_price_ranges = []


    for gift in available_gifts:

        price_midpoint = (
            gift["min_price"]
            + gift["max_price"]
        ) / 2


        too_similar = False


        for previous_midpoint in used_price_ranges:

            if abs(
                price_midpoint
                - previous_midpoint
            ) < 20:

                too_similar = True

                break


        if not too_similar:

            suggestions.append(
                gift
            )

            used_price_ranges.append(
                price_midpoint
            )


        if len(suggestions) == 5:

            break


    # ========================================================
    # FILL REMAINING SLOTS
    #
    # If price variety prevented us from reaching 5,
    # fill the remaining slots with the next best gifts.
    # ========================================================

    if len(suggestions) < 5:

        for gift in available_gifts:

            if gift in suggestions:

                continue


            suggestions.append(
                gift
            )


            if len(suggestions) == 5:

                break


    # ========================================================
    # FINAL PRICE SAFETY
    #
    # Never display a maximum price above the user's budget.
    # ========================================================

    final_suggestions = []


    for gift in suggestions:

        adjusted_gift = gift.copy()


        adjusted_gift["max_price"] = min(
            gift["max_price"],
            budget
        )


        if (
            adjusted_gift["min_price"]
            <= adjusted_gift["max_price"]
        ):

            final_suggestions.append(
                adjusted_gift
            )


    return final_suggestions