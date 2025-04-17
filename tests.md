GET http://localhost:5000/products/price?min=50&max=200

GET http://localhost:5000/products/category/Accessories

GET http://localhost:5000/products/search?q=mouse

GET http://localhost:5000/setup-indexes


- **Method** (GET, POST, etc.)  
- **URL** (e.g., `http://localhost:5000/products`)  
- **What to do** in Postman  
- Sample data (if needed)  
- What to expect as a response ✅  

---

## 🧪 1. Add Single Product
**Method:** `POST`  
**URL:** `http://localhost:5000/products`  
**Body:** Raw → JSON  
```json
{
  "name": "Test Product",
  "category": "Testing",
  "price": 99.99,
  "stock": 15,
  "status": "in-stock"
}
```

✅ **Expected:**  
```json
{
  "message": "Product added",
  "id": "<generated_id>"
}
```

---

## 🧪 2. Add Multiple Products (Bulk Insert)
**Method:** `POST`  
**URL:** `http://localhost:5000/products`  
**Body:** Raw → JSON  
```json
[
  {
    "name": "Test A",
    "category": "Testing",
    "price": 10.0,
    "stock": 5,
    "status": "low-stock"
  },
  {
    "name": "Test B",
    "category": "Testing",
    "price": 20.0,
    "stock": 15,
    "status": "in-stock"
  }
]
```

✅ **Expected:**  
```json
{
  "message": "Products added",
  "ids": ["<id1>", "<id2>"]
}
```

---

## 🧪 3. Get All Products
**Method:** `GET`  
**URL:** `http://localhost:5000/products`

✅ **Expected:**  
An array of all product objects with `_id` converted to strings.

---

## 🧪 4. Get Products by Category
**Method:** `GET`  
**URL:** `http://localhost:5000/products/category/Testing`

✅ **Expected:**  
Array of products with `"category": "Testing"`.

---

## 🧪 5. Get Products in a Price Range
**Method:** `GET`  
**URL:**  
`http://localhost:5000/products/price?min=10&max=100`

✅ **Expected:**  
Products priced between 10 and 100.

---

## 🧪 6. Search Products by Name (Case-insensitive)
**Method:** `GET`  
**URL:**  
`http://localhost:5000/products/search?q=test`

✅ **Expected:**  
Products with "test" in their name, regardless of case.

---

## 🧪 7. Update a Product
**Method:** `PATCH`  
**URL:** `http://localhost:5000/products/<product_id>`  
(Replace `<product_id>` with a real one from previous GET)  
**Body:** Raw → JSON  
```json
{
  "price": 150.0,
  "stock": 20
}
```

✅ **Expected:**  
```json
{
  "message": "Product updated",
  "modified_count": 1
}
```

---

## 🧪 8. Delete a Product
**Method:** `DELETE`  
**URL:** `http://localhost:5000/products/<product_id>`  
(Use an actual ID)

✅ **Expected:**  
```json
{
  "message": "Product deleted",
  "deleted_count": 1
}
```

---

Absolutely! Here's your test case for the **paginated products endpoint**:

---

### 🔍 9. Paginated Products Endpoint Test

- **Method:** `GET`  
- **URL:** `http://localhost:5000/products/paginated?page=1&limit=5`  

- **What to expect as a response ✅:**
```json
[
  {
    "_id": "661e...c7f",
    "name": "Laptop",
    "category": "Electronics",
    "price": 1200.99,
    "quantity": 15
  },
  {
    "_id": "661e...d4a",
    "name": "Office Chair",
    "category": "Furniture",
    "price": 149.50,
    "quantity": 30
  },
  ...
]
```

> ✅ You should receive **up to 5 products** (based on your `limit=5`), starting from the **first page** (`page=1`).

---

### ✅ Bonus Tip:
You can test `page=2` and `limit=3` like this:
```
http://localhost:5000/products/paginated?page=2&limit=3
```
That will skip the first 3 results and return the next 3.

---

Got it! Here's the aggregation testing section in your preferred format:

---

## 🧪 10. Get Total Inventory Value  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/total-value`  

✅ **Expected:**  
```json
{
  "total_inventory_value": 13999.5
}
```
> 🔹 *This number will change based on your actual data — it's the sum of `price * quantity` for all products.*

---

## 🧪 11. Get Product Count Per Category  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/category-count`  

✅ **Expected:**  
```json
[
  { "_id": "Electronics", "count": 5 },
  { "_id": "Clothing", "count": 6 },
  { "_id": "Furniture", "count": 4 }
]
```
> 🔹 *Shows how many products are in each category.*

---

## 🧪 12. Get Average Price Per Category  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/average-price`  

✅ **Expected:**  
```json
[
  { "_id": "Electronics", "average_price": 149.99 },
  { "_id": "Clothing", "average_price": 37.5 },
  { "_id": "Furniture", "average_price": 220.0 }
]
```
> 🔹 *Calculates the average price for each category.*

## 🧪 13. Get Top Selling Products  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/top-selling`  

✅ **Expected:**  
```json
[
  { "_id": "Product A", "total_sales": 500 },
  { "_id": "Product B", "total_sales": 300 },
  { "_id": "Product C", "total_sales": 250 }
]
```

---

## 🧪 14. Get Lowest Stock Products  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/low-stock`  || `http://localhost:5000/products/low-stock?threshold=10`

✅ **Expected:**  
```json
[
  { "_id": "Product F", "stock": 2 },
  { "_id": "Product G", "stock": 1 },
  { "_id": "Product H", "stock": 3 }
]
```

---

## 🧪 15. Group Products by Brand/Vendor  
**Method:** `GET`  
**URL:** `http://localhost:5000/products/group-by-brand`  

✅ **Expected:**  
```json
[
  { "_id": "Brand A", "count": 10 },
  { "_id": "Brand B", "count": 5 },
  { "_id": "Brand C", "count": 8 }
]
```

---

Once these routes are added to your app, you can easily test them through Postman. Let me know if you need any further adjustments or explanations! 😊