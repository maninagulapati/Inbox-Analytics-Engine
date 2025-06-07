# 📩 Inbox Analytics Engine

Transform emails with CSV or Excel attachments into **automated dashboards** using Postmark webhooks, FastAPI, and Streamlit.

**🔸 Submission for the Postmark Challenge: Inbox Innovators**

---

## 🚀 What It Does

The **Inbox Analytics Engine** is a smart email-report parser that:

- 📨 Captures CSV/XLSX files from **inbound emails** using Postmark
- 🧠 Extracts data, identifies patterns, and generates AI-powered **insights**
- 📊 Displays **interactive dashboards** using Streamlit and Plotly
- ⚡ Saves time by removing the need for manual downloads or Excel wrangling

---

## 🔑 Key Features

- ✅ **Postmark Webhook** integration for real-time email processing  
- 📂 Supports **CSV and XLSX** formats  
- 📈 Beautiful **visualizations** with Plotly  
- 🧠 Built-in **GPT** for summaries, anomaly detection, and chart suggestions  
- 🗂️ Files organized by sender and subject  

---

## 🧪 Demo: Run Locally

> This app is currently not hosted online. You can run it locally:

### 1. Clone the Repository

```bash
git clone https://github.com/maninagulapati/Inbox-Analytics-Engine.git
cd Inbox-Analytics-Engine

2. Set Up Environment
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt

3.Start the FastAPI Backend
uvicorn backend.main:app --reload

4. Run the Streamlit Dashboard
streamlit run dashboard/app.py

5. Set Up Postmark Inbound Webhook
http://localhost:8000/inbound
Send an email with .csv or .xlsx attachments to your Postmark inbound email address.
