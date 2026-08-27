# 🎁 Gift Genie

Gift Genie is a web application that helps users find thoughtful gift ideas based on a recipient's information such as their relationship, age, interests, and budget.

## ✨ Features

- 👤 User registration and login
- 👥 Recipient management
- 🎁 Rule-based gift recommendations
- 💰 Budget-based gift suggestions
- ❤️ Save favourite gift ideas
- 📅 Manage important occasions
- 🔔 Occasion notifications
- ⚙️ User settings
- 👤 Profile activity
- 📱 Responsive mobile design

## 🧠 Recommendation System

Gift Genie currently uses a **rule-based recommendation system**.

Gift suggestions are generated according to:

- Recipient's interest
- Recipient's budget

The system contains a gift catalogue for different interest categories and selects suitable suggestions based on the user's budget.

Recommendations are limited to a maximum of 5 gift ideas.

## 🛠️ Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Jinja2

## 📁 Project Structure

```text
gift-genie/
│
├── app.py
├── database.py
├── gift_logic.py
├── requirements.txt
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── login.html
    ├── register.html
    ├── profile.html
    ├── settings.html
    ├── recipients.html
    ├── recipient_form.html
    ├── gift_ideas.html
    ├── edit_gift.html
    ├── saved_gifts.html
    ├── occasions.html
    └── occasion_form.html