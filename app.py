from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    session
)

import os

from dotenv import load_dotenv

from datetime import datetime, date

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import get_db, init_db
from gift_logic import generate_gift_ideas


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret-key"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_days_until(date_string):

    try:

        occasion_date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()

        today = date.today()

        occasion_this_year = occasion_date.replace(
            year=today.year
        )

        if occasion_this_year < today:

            occasion_this_year = occasion_date.replace(
                year=today.year + 1
            )

        return (
            occasion_this_year - today
        ).days

    except (ValueError, TypeError):

        return 0


def format_price(min_price, max_price):

    if min_price == max_price:

        return f"RM{min_price:.0f}"

    return (
        f"RM{min_price:.0f} - "
        f"RM{max_price:.0f}"
    )


def login_required():

    if "user_id" not in session:

        flash(
            "Please login to continue.",
            "error"
        )

        return False

    return True


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        if not all([
            username,
            email,
            password,
            confirm_password
        ]):

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        if len(password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        connection = get_db()


        # ====================================================
        # CHECK USERNAME
        # ====================================================

        existing_username = connection.execute("""
            SELECT id
            FROM users

            WHERE username = ?
        """, (
            username,
        )).fetchone()


        if existing_username:

            connection.close()

            flash(
                "Username already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # ====================================================
        # CHECK EMAIL
        # ====================================================

        existing_email = connection.execute("""
            SELECT id
            FROM users

            WHERE email = ?
        """, (
            email,
        )).fetchone()


        if existing_email:

            connection.close()

            flash(
                "Email already exists.",
                "error"
            )

            return redirect(
                url_for("register")
            )


        # ====================================================
        # HASH PASSWORD
        # ====================================================

        hashed_password = generate_password_hash(
            password
        )


        # ====================================================
        # CREATE USER
        # ====================================================

        connection.execute("""
            INSERT INTO users
            (
                username,
                email,
                password_hash
            )

            VALUES (?, ?, ?)
        """, (
            username,
            email,
            hashed_password
        ))


        connection.commit()

        connection.close()


        flash(
            "Registration successful! Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if "user_id" in session:

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not email or not password:

            flash(
                "Please enter your email and password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        connection = get_db()


        # ====================================================
        # FIND USER
        # ====================================================

        user = connection.execute("""
            SELECT *
            FROM users

            WHERE email = ?
        """, (
            email,
        )).fetchone()


        connection.close()


        if user is None:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # ====================================================
        # CHECK PASSWORD
        # ====================================================

        if not check_password_hash(
            user["password_hash"],
            password
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )


        # ====================================================
        # CREATE SESSION
        # ====================================================

        session.clear()

        session["user_id"] = user["id"]

        session["username"] = user["username"]

        session["user_name"] = user["username"]

        session["email"] = user["email"]


        flash(
            f"Welcome back, {user['username']}!",
            "success"
        )


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("login")
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    connection = get_db()


    # ========================================================
    # STATISTICS
    # ========================================================

    recipient_count = connection.execute("""
        SELECT COUNT(*)
        FROM recipients

        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]


    gift_count = connection.execute("""
        SELECT COUNT(*)
        FROM gift_ideas

        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]


    occasion_count = connection.execute("""
        SELECT COUNT(*)
        FROM occasions

        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]


    saved_count = connection.execute("""
        SELECT COUNT(*)
        FROM saved_gifts

        WHERE user_id = ?
    """, (
        user_id,
    )).fetchone()[0]


    # ========================================================
    # ALL UPCOMING OCCASIONS
    # ========================================================

    occasion_rows = connection.execute("""
        SELECT
            occasions.*,
            recipients.name AS recipient_name

        FROM occasions

        LEFT JOIN recipients
            ON occasions.recipient_id = recipients.id

        WHERE occasions.user_id = ?

        ORDER BY occasions.date ASC
    """, (
        user_id,
    )).fetchall()


    upcoming_occasions = []


    for occasion in occasion_rows:

        days = calculate_days_until(
            occasion["date"]
        )


        upcoming_occasions.append({

            "name":
                occasion["recipient_name"]
                or "Unknown",

            "occasion":
                occasion["occasion"],

            "date":
                occasion["date"],

            "days":
                days

        })


    upcoming_occasions.sort(
        key=lambda item: item["days"]
    )


    # ========================================================
    # ALL CURRENT GIFT IDEAS
    # ========================================================

    gift_rows = connection.execute("""
        SELECT *
        FROM gift_ideas

        WHERE user_id = ?

        ORDER BY id DESC
    """, (
        user_id,
    )).fetchall()


    recent_gifts = []


    for gift in gift_rows:

        recent_gifts.append({

            "id":
                gift["id"],

            "name":
                gift["name"],

            "description":
                gift["description"],

            "price":
                format_price(
                    gift["min_price"],
                    gift["max_price"]
                )

        })


    connection.close()


    return render_template(
        "dashboard.html",

        recipient_count=recipient_count,

        gift_count=gift_count,

        occasion_count=occasion_count,

        saved_count=saved_count,

        upcoming_occasions=upcoming_occasions,

        recent_gifts=recent_gifts
    )


# ============================================================
# RECIPIENTS
# ============================================================

@app.route("/recipients")
def recipients():

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    recipients_list = connection.execute("""
        SELECT *
        FROM recipients

        WHERE user_id = ?

        ORDER BY id DESC
    """, (
        session["user_id"],
    )).fetchall()


    connection.close()


    return render_template(
        "recipients.html",

        recipients=recipients_list
    )


# ============================================================
# ADD RECIPIENT
# ============================================================

@app.route(
    "/recipients/add",
    methods=["GET", "POST"]
)
def recipient_form():

    if not login_required():

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        relationship = request.form.get(
            "relationship",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        interest = request.form.get(
            "interest",
            ""
        ).strip()

        budget = request.form.get(
            "budget",
            ""
        ).strip()


        # ====================================================
        # VALIDATION
        # ====================================================

        if not all([
            name,
            relationship,
            age,
            interest,
            budget
        ]):

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for("recipient_form")
            )


        try:

            age = int(age)

            budget = float(budget)

        except ValueError:

            flash(
                "Age and budget must be valid numbers.",
                "error"
            )

            return redirect(
                url_for("recipient_form")
            )


        if age < 1 or age > 120:

            flash(
                "Please enter a valid age.",
                "error"
            )

            return redirect(
                url_for("recipient_form")
            )


        # ====================================================
        # BUDGET LIMIT
        # ====================================================

        if budget < 10:

            flash(
                "Budget must be at least RM10.",
                "error"
            )

            return redirect(
                url_for("recipient_form")
            )


        if budget > 1000:

            flash(
                "Budget cannot be more than RM1,000.",
                "error"
            )

            return redirect(
                url_for("recipient_form")
            )


        connection = get_db()


        connection.execute("""
            INSERT INTO recipients
            (
                user_id,
                name,
                relationship,
                age,
                interest,
                budget
            )

            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            name,
            relationship,
            age,
            interest,
            budget
        ))


        connection.commit()

        connection.close()


        flash(
            "Recipient added successfully!",
            "success"
        )


        return redirect(
            url_for("recipients")
        )


    # ========================================================
    # GET DEFAULT BUDGET
    # ========================================================

    connection = get_db()


    user = connection.execute("""
        SELECT default_budget
        FROM users

        WHERE id = ?
    """, (
        user_id,
    )).fetchone()


    connection.close()


    default_budget = 100


    if user and user["default_budget"]:

        default_budget = user["default_budget"]


    return render_template(
        "recipient_form.html",

        recipient=None,

        edit_mode=False,

        default_budget=default_budget
    )


# ============================================================
# EDIT RECIPIENT
# ============================================================

@app.route(
    "/recipients/edit/<int:recipient_id>",
    methods=["GET", "POST"]
)
def edit_recipient(recipient_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    recipient = connection.execute("""
        SELECT *
        FROM recipients

        WHERE id = ?

        AND user_id = ?
    """, (
        recipient_id,
        session["user_id"]
    )).fetchone()


    if recipient is None:

        connection.close()

        flash(
            "Recipient not found.",
            "error"
        )

        return redirect(
            url_for("recipients")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        relationship = request.form.get(
            "relationship",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        interest = request.form.get(
            "interest",
            ""
        ).strip()

        budget = request.form.get(
            "budget",
            ""
        ).strip()


        if not all([
            name,
            relationship,
            age,
            interest,
            budget
        ]):

            connection.close()

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_recipient",
                    recipient_id=recipient_id
                )
            )


        try:

            age = int(age)

            budget = float(budget)

        except ValueError:

            connection.close()

            flash(
                "Age and budget must be valid numbers.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_recipient",
                    recipient_id=recipient_id
                )
            )


        if age < 1 or age > 120:

            connection.close()

            flash(
                "Please enter a valid age.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_recipient",
                    recipient_id=recipient_id
                )
            )


        # ====================================================
        # BUDGET LIMIT
        # ====================================================

        if budget < 10:

            connection.close()

            flash(
                "Budget must be at least RM10.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_recipient",
                    recipient_id=recipient_id
                )
            )


        if budget > 1000:

            connection.close()

            flash(
                "Budget cannot be more than RM1,000.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_recipient",
                    recipient_id=recipient_id
                )
            )


        connection.execute("""
            UPDATE recipients

            SET
                name = ?,
                relationship = ?,
                age = ?,
                interest = ?,
                budget = ?

            WHERE id = ?

            AND user_id = ?
        """, (
            name,
            relationship,
            age,
            interest,
            budget,
            recipient_id,
            session["user_id"]
        ))


        connection.commit()

        connection.close()


        flash(
            "Recipient updated successfully!",
            "success"
        )


        return redirect(
            url_for("recipients")
        )


    connection.close()


    return render_template(
        "recipient_form.html",

        recipient=recipient,

        edit_mode=True
    )


# ============================================================
# DELETE RECIPIENT
# ============================================================

@app.route(
    "/recipients/delete/<int:recipient_id>"
)
def delete_recipient(recipient_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    connection.execute("""
        DELETE FROM recipients

        WHERE id = ?

        AND user_id = ?
    """, (
        recipient_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    flash(
        "Recipient deleted successfully!",
        "success"
    )


    return redirect(
        url_for("recipients")
    )


# ============================================================
# GIFT IDEAS
# ============================================================

@app.route(
    "/gift-ideas",
    methods=["GET", "POST"]
)
def gift_ideas():

    if not login_required():

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]

    connection = get_db()


    # ========================================================
    # GET RECIPIENTS
    # ========================================================

    recipients_list = connection.execute("""
        SELECT *
        FROM recipients

        WHERE user_id = ?

        ORDER BY name ASC
    """, (
        user_id,
    )).fetchall()


    # ========================================================
    # GET RECENT INTERESTS
    # ========================================================

    recent_interests = connection.execute("""
        SELECT

            interest,

            COUNT(*) AS recipient_count,

            MAX(id) AS latest_recipient_id

        FROM recipients

        WHERE user_id = ?

        GROUP BY interest

        ORDER BY latest_recipient_id DESC

        LIMIT 6
    """, (
        user_id,
    )).fetchall()


    # ========================================================
    # GENERATE GIFT IDEAS
    # ========================================================

    if request.method == "POST":

        recipient_id = request.form.get(
            "recipient_id",
            type=int
        )


        if not recipient_id:

            connection.close()

            flash(
                "Please select a recipient.",
                "error"
            )

            return redirect(
                url_for("gift_ideas")
            )


        recipient = connection.execute("""
            SELECT *
            FROM recipients

            WHERE id = ?

            AND user_id = ?
        """, (
            recipient_id,
            user_id
        )).fetchone()


        if recipient is None:

            connection.close()

            flash(
                "Recipient not found.",
                "error"
            )

            return redirect(
                url_for("gift_ideas")
            )


        suggestions = generate_gift_ideas(
            recipient["interest"],
            recipient["budget"]
        )


        # ====================================================
        # REMOVE OLD GIFT IDEAS
        # ====================================================

        connection.execute("""
            DELETE FROM gift_ideas

            WHERE recipient_id = ?

            AND user_id = ?
        """, (
            recipient_id,
            user_id
        ))


        # ====================================================
        # SAVE NEW GIFT IDEAS
        # ====================================================

        for gift in suggestions:

            connection.execute("""
                INSERT INTO gift_ideas
                (
                    user_id,
                    recipient_id,
                    name,
                    description,
                    min_price,
                    max_price
                )

                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                recipient_id,
                gift["name"],
                gift["description"],
                gift["min_price"],
                gift["max_price"]
            ))


        connection.commit()

        connection.close()


        flash(
            "Gift ideas generated successfully!",
            "success"
        )


        return redirect(
            url_for(
                "gift_ideas",
                recipient_id=recipient_id
            )
        )


    # ========================================================
    # SHOW SELECTED RECIPIENT'S GIFTS
    # ========================================================

    selected_recipient_id = request.args.get(
        "recipient_id",
        type=int
    )


    selected_recipient = None

    gifts = []


    if selected_recipient_id:

        selected_recipient = connection.execute("""
            SELECT *
            FROM recipients

            WHERE id = ?

            AND user_id = ?
        """, (
            selected_recipient_id,
            user_id
        )).fetchone()


        if selected_recipient:

            gifts = connection.execute("""
                SELECT *
                FROM gift_ideas

                WHERE recipient_id = ?

                AND user_id = ?

                ORDER BY id DESC
            """, (
                selected_recipient_id,
                user_id
            )).fetchall()


    connection.close()


    return render_template(
        "gift_ideas.html",

        recipients=recipients_list,

        recent_interests=recent_interests,

        selected_recipient=selected_recipient,

        gifts=gifts
    )


# ============================================================
# EDIT GIFT
# ============================================================

@app.route(
    "/gift-ideas/edit/<int:gift_id>",
    methods=["GET", "POST"]
)
def edit_gift(gift_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    gift = connection.execute("""
        SELECT *
        FROM gift_ideas

        WHERE id = ?

        AND user_id = ?
    """, (
        gift_id,
        session["user_id"]
    )).fetchone()


    if gift is None:

        connection.close()

        flash(
            "Gift idea not found.",
            "error"
        )

        return redirect(
            url_for("gift_ideas")
        )


    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        min_price = request.form.get(
            "min_price",
            ""
        ).strip()

        max_price = request.form.get(
            "max_price",
            ""
        ).strip()


        if not all([
            name,
            description,
            min_price,
            max_price
        ]):

            connection.close()

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_gift",
                    gift_id=gift_id
                )
            )


        try:

            min_price = float(min_price)

            max_price = float(max_price)

        except ValueError:

            connection.close()

            flash(
                "Prices must be valid numbers.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_gift",
                    gift_id=gift_id
                )
            )


        if min_price < 0 or max_price < 0:

            connection.close()

            flash(
                "Prices cannot be negative.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_gift",
                    gift_id=gift_id
                )
            )


        if min_price > max_price:

            connection.close()

            flash(
                "Minimum price cannot be greater than maximum price.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_gift",
                    gift_id=gift_id
                )
            )


        connection.execute("""
            UPDATE gift_ideas

            SET
                name = ?,
                description = ?,
                min_price = ?,
                max_price = ?

            WHERE id = ?

            AND user_id = ?
        """, (
            name,
            description,
            min_price,
            max_price,
            gift_id,
            session["user_id"]
        ))


        connection.commit()

        connection.close()


        flash(
            "Gift idea updated successfully!",
            "success"
        )


        return redirect(
            url_for(
                "gift_ideas",
                recipient_id=gift["recipient_id"]
            )
        )


    connection.close()


    return render_template(
        "edit_gift.html",

        gift=gift
    )


# ============================================================
# DELETE GIFT
# ============================================================

@app.route(
    "/gift-ideas/delete/<int:gift_id>"
)
def delete_gift(gift_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    gift = connection.execute("""
        SELECT *
        FROM gift_ideas

        WHERE id = ?

        AND user_id = ?
    """, (
        gift_id,
        session["user_id"]
    )).fetchone()


    if gift is None:

        connection.close()

        flash(
            "Gift idea not found.",
            "error"
        )

        return redirect(
            url_for("gift_ideas")
        )


    recipient_id = gift["recipient_id"]


    connection.execute("""
        DELETE FROM gift_ideas

        WHERE id = ?

        AND user_id = ?
    """, (
        gift_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    flash(
        "Gift idea deleted successfully!",
        "success"
    )


    return redirect(
        url_for(
            "gift_ideas",
            recipient_id=recipient_id
        )
    )


# ============================================================
# SAVE GIFT
# ============================================================

@app.route(
    "/gift-ideas/save/<int:gift_id>"
)
def save_gift(gift_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    gift = connection.execute("""
        SELECT *
        FROM gift_ideas

        WHERE id = ?

        AND user_id = ?
    """, (
        gift_id,
        session["user_id"]
    )).fetchone()


    if gift is None:

        connection.close()

        flash(
            "Gift idea not found.",
            "error"
        )

        return redirect(
            url_for("gift_ideas")
        )


    existing = connection.execute("""
        SELECT id
        FROM saved_gifts

        WHERE gift_idea_id = ?

        AND user_id = ?
    """, (
        gift_id,
        session["user_id"]
    )).fetchone()


    if existing is None:

        connection.execute("""
            INSERT INTO saved_gifts
            (
                user_id,
                gift_idea_id,
                recipient_id
            )

            VALUES (?, ?, ?)
        """, (
            session["user_id"],
            gift_id,
            gift["recipient_id"]
        ))


        connection.commit()


        flash(
            "Gift saved successfully!",
            "success"
        )


    else:

        flash(
            "This gift is already saved.",
            "error"
        )


    connection.close()


    return redirect(
        url_for(
            "gift_ideas",
            recipient_id=gift["recipient_id"]
        )
    )


# ============================================================
# SAVED GIFTS
# ============================================================

@app.route("/saved-gifts")
def saved_gifts():

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    saved_list = connection.execute("""
        SELECT

            saved_gifts.id AS saved_id,

            gift_ideas.id AS gift_id,

            gift_ideas.name,

            gift_ideas.description,

            gift_ideas.min_price,

            gift_ideas.max_price,

            recipients.name AS recipient_name

        FROM saved_gifts

        JOIN gift_ideas
            ON saved_gifts.gift_idea_id = gift_ideas.id

        JOIN recipients
            ON saved_gifts.recipient_id = recipients.id

        WHERE saved_gifts.user_id = ?

        ORDER BY saved_gifts.id DESC
    """, (
        session["user_id"],
    )).fetchall()


    connection.close()


    return render_template(
        "saved_gifts.html",

        saved_gifts=saved_list
    )


# ============================================================
# DELETE SAVED GIFT
# ============================================================

@app.route(
    "/saved-gifts/delete/<int:saved_id>"
)
def delete_saved_gift(saved_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    connection.execute("""
        DELETE FROM saved_gifts

        WHERE id = ?

        AND user_id = ?
    """, (
        saved_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    flash(
        "Saved gift removed.",
        "success"
    )


    return redirect(
        url_for("saved_gifts")
    )


# ============================================================
# OCCASIONS
# ============================================================

@app.route("/occasions")
def occasions():

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    occasions_list = connection.execute("""
        SELECT

            occasions.*,

            recipients.name AS recipient_name

        FROM occasions

        LEFT JOIN recipients
            ON occasions.recipient_id = recipients.id

        WHERE occasions.user_id = ?

        ORDER BY occasions.date ASC
    """, (
        session["user_id"],
    )).fetchall()


    connection.close()


    return render_template(
        "occasions.html",

        occasions=occasions_list
    )


# ============================================================
# ADD OCCASION
# ============================================================

@app.route(
    "/occasions/add",
    methods=["GET", "POST"]
)
def occasion_form():

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    recipients_list = connection.execute("""
        SELECT *
        FROM recipients

        WHERE user_id = ?

        ORDER BY name ASC
    """, (
        session["user_id"],
    )).fetchall()


    if request.method == "POST":

        recipient_id = request.form.get(
            "recipient_id",
            type=int
        )

        occasion = request.form.get(
            "occasion",
            ""
        ).strip()

        occasion_date = request.form.get(
            "date",
            ""
        ).strip()


        if (
            not recipient_id
            or not occasion
            or not occasion_date
        ):

            connection.close()

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for("occasion_form")
            )


        recipient = connection.execute("""
            SELECT id
            FROM recipients

            WHERE id = ?

            AND user_id = ?
        """, (
            recipient_id,
            session["user_id"]
        )).fetchone()


        if recipient is None:

            connection.close()

            flash(
                "Recipient not found.",
                "error"
            )

            return redirect(
                url_for("occasion_form")
            )


        connection.execute("""
            INSERT INTO occasions
            (
                user_id,
                recipient_id,
                occasion,
                date
            )

            VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            recipient_id,
            occasion,
            occasion_date
        ))


        connection.commit()

        connection.close()


        flash(
            "Occasion added successfully!",
            "success"
        )


        return redirect(
            url_for("occasions")
        )


    connection.close()


    return render_template(
        "occasion_form.html",

        recipients=recipients_list,

        occasion=None,

        title="Add Occasion"
    )


# ============================================================
# EDIT OCCASION
# ============================================================

@app.route(
    "/occasions/edit/<int:occasion_id>",
    methods=["GET", "POST"]
)
def edit_occasion(occasion_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    occasion = connection.execute("""
        SELECT *
        FROM occasions

        WHERE id = ?

        AND user_id = ?
    """, (
        occasion_id,
        session["user_id"]
    )).fetchone()


    if occasion is None:

        connection.close()

        flash(
            "Occasion not found.",
            "error"
        )

        return redirect(
            url_for("occasions")
        )


    recipients_list = connection.execute("""
        SELECT *
        FROM recipients

        WHERE user_id = ?

        ORDER BY name ASC
    """, (
        session["user_id"],
    )).fetchall()


    if request.method == "POST":

        recipient_id = request.form.get(
            "recipient_id",
            type=int
        )

        occasion_name = request.form.get(
            "occasion",
            ""
        ).strip()

        occasion_date = request.form.get(
            "date",
            ""
        ).strip()


        if (
            not recipient_id
            or not occasion_name
            or not occasion_date
        ):

            connection.close()

            flash(
                "Please fill in all fields.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_occasion",
                    occasion_id=occasion_id
                )
            )


        recipient = connection.execute("""
            SELECT id
            FROM recipients

            WHERE id = ?

            AND user_id = ?
        """, (
            recipient_id,
            session["user_id"]
        )).fetchone()


        if recipient is None:

            connection.close()

            flash(
                "Recipient not found.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_occasion",
                    occasion_id=occasion_id
                )
            )


        connection.execute("""
            UPDATE occasions

            SET
                recipient_id = ?,
                occasion = ?,
                date = ?

            WHERE id = ?

            AND user_id = ?
        """, (
            recipient_id,
            occasion_name,
            occasion_date,
            occasion_id,
            session["user_id"]
        ))


        connection.commit()

        connection.close()


        flash(
            "Occasion updated successfully!",
            "success"
        )


        return redirect(
            url_for("occasions")
        )


    connection.close()


    return render_template(
        "occasion_form.html",

        recipients=recipients_list,

        occasion=occasion,

        title="Edit Occasion"
    )


# ============================================================
# DELETE OCCASION
# ============================================================

@app.route(
    "/occasions/delete/<int:occasion_id>"
)
def delete_occasion(occasion_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()


    occasion = connection.execute("""
        SELECT id
        FROM occasions

        WHERE id = ?

        AND user_id = ?
    """, (
        occasion_id,
        session["user_id"]
    )).fetchone()


    if occasion is None:

        connection.close()

        flash(
            "Occasion not found.",
            "error"
        )

        return redirect(
            url_for("occasions")
        )


    connection.execute("""
        DELETE FROM occasions

        WHERE id = ?

        AND user_id = ?
    """, (
        occasion_id,
        session["user_id"]
    ))


    connection.commit()

    connection.close()


    flash(
        "Occasion deleted successfully!",
        "success"
    )


    return redirect(
        url_for("occasions")
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

@app.route("/notifications")
def notifications():

    if not login_required():

        return jsonify([])


    connection = get_db()


    # ========================================================
    # CHECK USER NOTIFICATION SETTING
    # ========================================================

    user = connection.execute("""
        SELECT notifications_enabled
        FROM users

        WHERE id = ?
    """, (
        session["user_id"],
    )).fetchone()


    # ========================================================
    # NOTIFICATIONS DISABLED
    # ========================================================

    if (
        user
        and user["notifications_enabled"] == 0
    ):

        connection.close()

        return jsonify([])


    # ========================================================
    # GET OCCASIONS
    # ========================================================

    occasions_list = connection.execute("""
        SELECT

            occasions.*,

            recipients.name AS recipient_name

        FROM occasions

        LEFT JOIN recipients
            ON occasions.recipient_id = recipients.id

        WHERE occasions.user_id = ?

        ORDER BY occasions.date ASC
    """, (
        session["user_id"],
    )).fetchall()


    notifications_list = []


    for occasion in occasions_list:

        days = calculate_days_until(
            occasion["date"]
        )


        if days <= 30:

            notifications_list.append({

                "name":
                    occasion["recipient_name"]
                    or "Unknown",

                "occasion":
                    occasion["occasion"],

                "date":
                    occasion["date"],

                "days":
                    days

            })


    connection.close()


    notifications_list.sort(
        key=lambda item: item["days"]
    )


    # ========================================================
    # SHOW MAXIMUM 5 NOTIFICATIONS
    # ========================================================

    notifications_list = notifications_list[:5]


    return jsonify(
        notifications_list
    )


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
def profile():

    if not login_required():

        return redirect(
            url_for("login")
        )


    connection = get_db()

    user_id = session["user_id"]


    # ========================================================
    # USER INFORMATION
    # ========================================================

    user = connection.execute("""
        SELECT *
        FROM users

        WHERE id = ?
    """, (
        user_id,
    )).fetchone()


    # ========================================================
    # PROFILE RECIPIENTS
    # ========================================================

    profile_recipients = connection.execute("""
        SELECT

            id,
            name,
            relationship,
            age,
            interest,
            budget

        FROM recipients

        WHERE user_id = ?

        ORDER BY id DESC
    """, (
        user_id,
    )).fetchall()


    # ========================================================
    # PROFILE SAVED GIFTS
    # ========================================================

    profile_saved_gifts = connection.execute("""
        SELECT

            saved_gifts.id AS saved_id,

            gift_ideas.name AS gift_name,

            gift_ideas.description,

            gift_ideas.min_price,

            gift_ideas.max_price,

            recipients.name AS recipient_name

        FROM saved_gifts

        JOIN gift_ideas
            ON saved_gifts.gift_idea_id = gift_ideas.id

        JOIN recipients
            ON saved_gifts.recipient_id = recipients.id

        WHERE saved_gifts.user_id = ?

        ORDER BY saved_gifts.id DESC
    """, (
        user_id,
    )).fetchall()


    # ========================================================
    # PROFILE UPCOMING OCCASIONS
    # ========================================================

    occasion_rows = connection.execute("""
        SELECT

            occasions.id,

            occasions.occasion,

            occasions.date,

            recipients.name AS recipient_name

        FROM occasions

        LEFT JOIN recipients
            ON occasions.recipient_id = recipients.id

        WHERE occasions.user_id = ?

        ORDER BY occasions.date ASC
    """, (
        user_id,
    )).fetchall()


    profile_occasions = []


    for occasion in occasion_rows:

        profile_occasions.append({

            "id":
                occasion["id"],

            "name":
                occasion["recipient_name"]
                or "Unknown",

            "occasion":
                occasion["occasion"],

            "date":
                occasion["date"],

            "days":
                calculate_days_until(
                    occasion["date"]
                )

        })


    profile_occasions.sort(
        key=lambda item: item["days"]
    )


    connection.close()


    return render_template(
        "profile.html",

        user=user,

        profile_recipients=profile_recipients,

        profile_saved_gifts=profile_saved_gifts,

        profile_occasions=profile_occasions
    )


# ============================================================
# SETTINGS
# ============================================================

@app.route(
    "/settings",
    methods=["GET", "POST"]
)
def settings():

    if not login_required():

        if request.method == "POST":

            return jsonify({
                "success": False,
                "message": "Please login to continue."
            }), 401

        return redirect(
            url_for("login")
        )


    user_id = session["user_id"]


    # ========================================================
    # SAVE SETTINGS
    # ========================================================

    if request.method == "POST":

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({
                "success": False,
                "message": "Invalid settings data."
            }), 400


        default_budget = data.get(
            "default_budget"
        )


        notifications = data.get(
            "notifications",
            "enabled"
        )


        # ====================================================
        # VALIDATE NOTIFICATION SETTING
        # ====================================================

        if notifications not in [
            "enabled",
            "disabled"
        ]:

            return jsonify({
                "success": False,
                "message":
                    "Invalid notification setting."
            }), 400


        # ====================================================
        # VALIDATE DEFAULT BUDGET
        # ====================================================

        try:

            default_budget = float(
                default_budget
            )

        except (TypeError, ValueError):

            return jsonify({
                "success": False,
                "message":
                    "Default Gift Budget must be a valid number."
            }), 400


        if (
            default_budget < 10
            or default_budget > 1000
            or not default_budget.is_integer()
        ):

            return jsonify({
                "success": False,
                "message":
                    "Default Gift Budget must be between RM10 and RM1,000."
            }), 400


        default_budget = int(
            default_budget
        )


        # ====================================================
        # CONVERT NOTIFICATION SETTING
        # ====================================================

        notifications_enabled = 1


        if notifications == "disabled":

            notifications_enabled = 0


        # ====================================================
        # SAVE TO DATABASE
        # ====================================================

        connection = get_db()


        connection.execute("""
            UPDATE users

            SET
                default_budget = ?,
                notifications_enabled = ?

            WHERE id = ?
        """, (
            default_budget,
            notifications_enabled,
            user_id
        ))


        connection.commit()

        connection.close()


        return jsonify({

            "success": True,

            "message":
                "Settings saved successfully!",

            "default_budget":
                default_budget,

            "notifications":
                notifications

        })


    # ========================================================
    # LOAD SETTINGS
    # ========================================================

    connection = get_db()


    user = connection.execute("""
        SELECT

            id,
            username,
            email,
            default_budget,
            notifications_enabled

        FROM users

        WHERE id = ?
    """, (
        user_id,
    )).fetchone()


    connection.close()


    return render_template(
        "settings.html",

        user=user
    )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_db()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )