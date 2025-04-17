No worries Tedlee — this is a pretty detailed project, but I’ll help you break it down step-by-step so it’s way easier to manage. We’ll divide it into **two parts** (just like your assignment says):

---

## 🧩 **PART ONE: Inventory Management System in MongoDB**

### ✅ Step-by-Step Plan

---

### **1. Set Up Your Project**
- **Choose a language**: Use **Node.js + Express** (recommended for MongoDB), or Python + Flask.
- **Install MongoDB locally** or create a **MongoDB Atlas** cluster (cloud).
- **Tooling**: Install **MongoDB Compass** for easy document inspection + **Postman** for API testing.

---

### **2. Create Your Product Schema (Document Structure)**

Example document:
```json
{
  "productName": "Teddy Bear (Large)",
  "category": "Plush Toys",
  "price": 24.99,
  "stock": 45,
  "status": "in-stock"
}
```

You can import the JSON we worked on earlier into your collection.

---

### **3. Implement Core Features**

#### 🔁 CRUD Operations (Create, Read, Update, Delete)
- Create (POST): `/api/products`
- Read (GET): `/api/products`, `/api/products/:id`
- Update (PATCH): `/api/products/:id`
- Delete (DELETE): `/api/products/:id`

Test these with **Postman**.

---

### **4. Advanced Features**

#### 🔍 Queries Using Operators
Use:
- `$eq`, `$gt`, `$lt` → filter by price or stock.
- `$in` → filter by category.
- `$regex` → search product names.

#### 🧮 Aggregations
Use aggregation pipelines to:
- Calculate **average price**
- Find **top 3 most expensive items**
- Count **in-stock vs low-stock**

#### 🔃 Sorting & Limiting
Use `.sort()` and `.limit()` for things like:
- Price (lowest to highest)
- Only 5 newest products

#### ⚡ Bulk Operations
Use `insertMany()` to add lots of products at once.

#### 🧾 Pagination
Use `.skip()` and `.limit()` to paginate results:
```js
db.products.find().skip(10).limit(10)
```

---

### **5. Performance**

#### 🔍 Indexing
Create indexes on:
- `productName`
- `category`
- `status`

#### 🎣 Cursors
Use cursors when handling large queries in code (e.g. Node.js or Python).

---

### **6. Security & Deployment**

#### 🌍 MongoDB Atlas
- Create a cluster
- Whitelist your IP
- Connect with connection string

#### 🔐 Add Basic Security
- Enable **authentication** and **passwords**.
- Use **environment variables** to store MongoDB URI.
- Use **roles** to allow read/write access only to specific users.

---

## 🧠 PART TWO: Security in NoSQL (MongoDB)

Here’s how to structure your report:

---

### 🔹 **1. Introduction to NoSQL**
- NoSQL = Non-relational DBs (e.g. MongoDB, Cassandra)
- Flexible schema, horizontal scaling, handles big data well

---

### 🔹 **2. Security in NoSQL**
- Not all NoSQL DBs have built-in security by default
- MongoDB initially had **open ports**, making it vulnerable
- Now supports: **authentication, authorization, encryption**

---

### 🔹 **3. Forms of Attacks**
- **Injection attacks** (via unfiltered user inputs)
- **Unauthorized access** (due to misconfigured permissions)
- **Denial of Service (DoS)** (overload database)
- **Data leakage** (via unencrypted communication)

---

### 🔹 **4. Solutions from Authors**
Some solutions proposed:
- **Santosh et al. (2020)**: Recommend role-based access and encrypted tokens.
- **Chen & Zhao (2021)**: Proposed secure API gateways + automatic vulnerability scanners.
- **MongoDB official docs**: Emphasize using TLS/SSL, IP whitelisting, and enabling audit logs.

---

### 🔹 **5. Open Challenges**
- Balancing speed and encryption overhead
- Lack of uniform security standards across NoSQL DBs
- Securing cloud deployments and third-party integrations

**Your proposal**: Develop plug-ins or middleware that auto-sanitize inputs and monitor unusual activity for small-scale devs.

---

## 📄 Suggested Files & Folders

```
inventory-app/
│
├── models/
│   └── Product.js
├── routes/
│   └── productRoutes.js
├── controllers/
│   └── productController.js
├── app.js
├── .env
├── postman_collection.json
└── README.md (documentation)
```

---

## 🧰 Tools Checklist

- [ ] MongoDB Compass
- [ ] MongoDB Atlas
- [ ] Postman
- [ ] Express (or Flask)
- [ ] Git + GitHub for group work

---

Let me know:
- What language you want to build the API in (Node.js or Python)?
- Do you want me to generate the codebase or a starter template?
- Want help drafting the documentation too?

We got this 💪