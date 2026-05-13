import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from forms import LoginForm, RegisterForm
from models import Student, User, db

app = Flask(__name__, instance_relative_config=True)

app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def allowed_file(file):
    filename = file.filename
    valid_extension = "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    valid_mime = file.content_type in ["image/png", "image/jpeg"]
    return valid_extension and valid_mime


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("register"))

        user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role=form.role.data,
            display_name=form.email.data
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful!")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("students"))

        flash("Invalid email or password.")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("home"))


@app.route("/students")
@login_required
def students():
    student_list = Student.query.order_by(Student.full_name).all()
    return render_template("students.html", students=student_list)


@app.route("/add-student", methods=["POST"])
@login_required
def add_student():
    if current_user.role != "admin":
        flash("Only admin users can add students.")
        return redirect(url_for("students"))

    student = Student(
        full_name=request.form["name"],
        email=request.form["email"]
    )

    db.session.add(student)
    db.session.commit()

    flash("Student added successfully.")
    return redirect(url_for("students"))


@app.route("/delete-student/<int:id>")
@login_required
def delete_student(id):
    if current_user.role != "admin":
        flash("Only admin users can delete students.")
        return redirect(url_for("students"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully.")
    return redirect(url_for("students"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        file = request.files.get("profile_picture")

        if not display_name:
            flash("Display name cannot be empty.")
            return redirect(url_for("profile"))

        current_user.display_name = display_name

        if file and file.filename:
            if allowed_file(file):
                filename = secure_filename(file.filename)
                extension = os.path.splitext(filename)[1]
                new_filename = f"user_{current_user.id}{extension}"

                file.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
                current_user.image_filename = new_filename
            else:
                flash("Only JPG, JPEG, and PNG files are allowed.")
                return redirect(url_for("profile"))

        db.session.commit()
        flash("Profile successfully updated.")
        return redirect(url_for("profile"))

    return render_template("profile.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
