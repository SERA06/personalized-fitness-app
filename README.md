## **Personalized Fitness App 🚀**  

A **Flask-based** web application that provides **personalized fitness and health activity recommendations** based on user input.  

### **Features**  
✅ User authentication (Login & Register)  
✅ Personalized fitness recommendations using **CatBoost ML model**  
✅ Flask-Mail integration for contact form  
✅ Secure environment variable management  
✅ Deployed using **AWS**  

---

### **Installation & Setup**  
#### **1. Clone the Repository**  
```sh
git clone https://github.com/SERA06/personalized-fitness-app.git
cd personalized-fitness-app
```

#### **2. Create & Activate a Virtual Environment**  
- **Windows (PowerShell)**  
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```
- **Mac/Linux**  
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

#### **3. Install Dependencies**  
```sh
pip install -r requirements.txt
```

#### **4. Set Up Environment Variables**  
Create a `.env` file in the project root and add:  
```ini
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///users.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

#### **5. Run the Flask App**  
```sh
python app.py
```
Now, open your browser and visit:  
**http://127.0.0.1:5000/** 🚀  

---

### **How to Use the App?**  
1. Click **"Get Started"** → Redirects to **Login Page**  
2. Register/Login to access the **Fitness Check** page  
3. Enter **BMI, weight, height, fitness level** → Click **Next**  
4. Set **Goals, duration, calories burned, intensity** → Click **Get Recommendation**  
5. Get **personalized activity recommendations**! 🎯  

---

### **Deployment (AWS Guide Coming Soon...)**  
- Work in progress: The app is being deployed to **AWS**.  


---

### **License**  
📝 This project is **open-source** under the **MIT License**.  

---

#### **📩 Contact**  
For any queries, reach out via:  
📧 **fitnessrecommend@gmail.com**  

---

