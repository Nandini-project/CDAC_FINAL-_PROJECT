from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "super-secret-key-123"

# In-memory storage
users = {}   # {username: password}
posts = []   # list of dicts

@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            flash("User already exists")
            return redirect(url_for("register"))

        users[username] = password
        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.get(username) == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route("/dashboard")
def dashboard():
    print("SESSION:", session)
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/create", methods=["GET", "POST"])
def create_post():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        posts.append({
            "author": session["user"],
            "title": title,
            "content": content
        })
        return redirect(url_for("index"))

    return render_template("create_post.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


