"""Flask Application for Paws Rescue Center."""
from flask import Flask, render_template, abort
from forms import SignUpForm, LoginForm
from flask import session, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

"""Information regarding the Pets in the System."""
pets = [
            {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
            {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
            {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
            {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."}, 
        ]

"""Information regarding the Users in the System."""
users = [
            {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"},
        ]   

@app.route("/")
def home():
    """View Function for the Home page."""
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    """View Function for the About page."""
    return render_template("about.html")

@app.route("/details/<int:pet_id>")
def details(pet_id):
    """View Function for the Details page of each pet."""
    pet = next((pet for pet in pets if pet["id"] == pet_id), None) 
    if pet is None: 
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet=pet)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """View Function to create new users"""
    form = SignUpForm(meta={'csrf': False})
    if form.validate_on_submit():
        new_user = {"id": len(users)+1, "full_name": form.fullName.data, "email": form.email.data, "password": form.password.data}
        users.append(new_user)
        return render_template("signup.html", message = "Successfully signed up")
    print(form.errors)
    return render_template("signup.html", form = form)

@app.route("/login", methods=["POST", "GET"])
def login():
    """View Function for login feature"""
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    """View Function to logout feature"""
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))
    

if __name__ == "__main__":
    """ """
    app.run(debug=True, host="0.0.0.0", port=3000)