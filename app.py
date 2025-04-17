from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables from .env file
load_dotenv()  # This will load your MongoDB URI or other settings from a .env file

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection string (replace with your own if necessary)
client = MongoClient("mongodb+srv://HelloBeta:IV7wqssYdgwijpQx@cluster0.nnecnay.mongodb.net/inventory_db?retryWrites=true&w=majority")
db = client["inventory_db"]
collection = db["products"]

# :::::::::::::::::::::::::::::::::: CRUD Routes ::::::::::::::::::::::::::::::::::

# Create or Insert Products (Single or Bulk)
@app.route('/products', methods=['POST'])
def insert_product():
    data = request.get_json()

    # Check if it's a list (bulk insert) or a single product
    if isinstance(data, list):
        result = collection.insert_many(data)
        return jsonify({
            "message": "Products added",
            "ids": [str(id) for id in result.inserted_ids]
        }), 201
    else:
        result = collection.insert_one(data)
        return jsonify({
            "message": "Product added",
            "id": str(result.inserted_id)
        }), 201

# Get All Products
@app.route('/products', methods=['GET'])
def get_all_products():
    products = list(collection.find())
    # Convert ObjectId to string for JSON serialization
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Get Products by Category
@app.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    products = list(collection.find({"category": category}))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Get Products within a Price Range
@app.route('/products/price', methods=['GET'])
def get_products_by_price_range():
    min_price = float(request.args.get('min', 0))
    max_price = float(request.args.get('max', 10000))
    products = list(collection.find({"price": {"$gte": min_price, "$lte": max_price}}))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Search Products by Name (Fuzzy Search)
@app.route('/products/search', methods=['GET'])
def search_products_by_name():
    keyword = request.args.get('q', '')
    products = list(collection.find({"name": {"$regex": keyword, "$options": "i"}}))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Get Paginated Products
@app.route('/products/paginated', methods=['GET'])
def get_paginated_products():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    skip = (page - 1) * limit

    products = list(collection.find().skip(skip).limit(limit))
    for product in products:
        product['_id'] = str(product['_id'])
    return jsonify(products)

# Update a Product (PATCH)
@app.route('/products/<product_id>', methods=['PATCH'])
def update_product(product_id):
    data = request.get_json()
    result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})
    return jsonify({"message": "Product updated", "modified_count": result.modified_count})

# Delete a Product (DELETE)
@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = collection.delete_one({"_id": ObjectId(product_id)})
    return jsonify({"message": "Product deleted", "deleted_count": result.deleted_count})

# :::::::::::::::::::::::::::::::::: Aggregation Routes ::::::::::::::::::::::::::::::::::

# Get Total Inventory Value (Price * Quantity)
@app.route('/products/total-value', methods=['GET'])
def get_total_inventory_value():
    pipeline = [
        {"$project": {"total": {"$multiply": ["$price", "$quantity"]}}},  # Calculate total value for each product
        {"$group": {"_id": None, "total_inventory_value": {"$sum": "$total"}}}  # Sum all total values
    ]
    result = list(collection.aggregate(pipeline))
    total_value = result[0]["total_inventory_value"] if result else 0
    return jsonify({"total_inventory_value": total_value})

# Get Product Count per Category
@app.route('/products/category-count', methods=['GET'])
def get_product_count_per_category():
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}  # Count the number of products for each category
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# Get Average Price per Category
@app.route('/products/average-price', methods=['GET'])
def get_average_price_per_category():
    pipeline = [
        {"$group": {"_id": "$category", "average_price": {"$avg": "$price"}}}  # Calculate average price per category
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result)

# Get Top Selling Products (Summing sales)
@app.route('/products/top-selling', methods=['GET'])
def get_top_selling_products():
    pipeline = [
        {"$group": {
            "_id": "$name",  # Group by product name
            "total_sales": {"$sum": "$sales"}  # Sum the sales for each product
        }},
        {"$sort": {"total_sales": -1}}  # Sort by total_sales in descending order
    ]
    products = list(collection.aggregate(pipeline))
    return jsonify(products)

# :::::::::::::::::::::::::::::::::: Helper Functions ::::::::::::::::::::::::::::::::::

# Helper function to serialize ObjectId to string
def serialize_objectid(product):
    if '_id' in product:
        product['_id'] = str(product['_id'])
    return product

# Get Low Stock Products
@app.route('/products/low-stock', methods=['GET'])
def get_low_stock_products():
    threshold = int(request.args.get('threshold', 10))  # Default threshold is 10
    products = list(collection.find({"stock": {"$lt": threshold}}))
    
    # Serialize ObjectId to string for each product
    products = [serialize_objectid(product) for product in products]

    return jsonify(products)

# Get Products Grouped by Category
@app.route('/products/group-by-category', methods=['GET'])
def get_products_group_by_category():
    pipeline = [
        {"$group": {
            "_id": "$category",  # Group by category
            "products": {"$push": "$$ROOT"}  # Push all products of this category into a list
        }}
    ]
    products = list(collection.aggregate(pipeline))
    
    # Serialize ObjectId to string for each product
    for category in products:
        category['products'] = [serialize_objectid(product) for product in category['products']]
    
    return jsonify(products)


# This endpoint is for setting up indexes for better performance
@app.route('/setup-indexes', methods=['GET'])
def create_indexes():
    collection.create_index("name")       # For search
    collection.create_index("category")   # For category filter
    collection.create_index("status")     # For stock/status operations
    return jsonify({"message": "Indexes created!"})

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
