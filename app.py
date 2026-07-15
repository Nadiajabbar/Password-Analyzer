from flask import Flask, render_template, request, session, jsonify
import pickle
import re

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("model.pkl", "rb"))

# SAME FEATURE SET
def extract_features(password):
    return [
        len(password),
        len(re.findall(r"\d", password)),
        len(re.findall(r"[A-Z]", password)),
        len(re.findall(r"[a-z]", password)),
        len(re.findall(r"[^a-zA-Z0-9]", password)),
    ]

def strength_score(password):
    score = 0
    if len(password) >= 8: score += 25
    if re.search(r"\d", password): score += 25
    if re.search(r"[A-Z]", password): score += 25
    if re.search(r"[^a-zA-Z0-9]", password): score += 25
    return score

@app.route("/", methods=["GET", "POST"])
def index():

    if "history" not in session:
        session["history"] = []

    prediction = None
    score = None
    last_password = None

    if request.method == "POST":
        password = request.form["password"]

        features = [extract_features(password)]
        prediction = model.predict(features)[0]
        score = strength_score(password)

        # Save to history permanently
        session["history"].append({
            "password": password,
            "result": prediction,
            "score": score
        })

        session.modified = True
        last_password = password

    return render_template(
        "index.html",
        prediction=prediction,
        score=score,
        history=session["history"]
    )

# RESET ONLY CURRENT RESULT (NOT HISTORY)
@app.route("/reset_current", methods=["POST"])
def reset_current():
    return jsonify({"status": "cleared"})

# CLEAR FULL HISTORY (OPTIONAL BUTTON)
@app.route("/reset_all", methods=["POST"])
def reset_all():
    session["history"] = []
    session.modified = True
    return jsonify({"status": "all_cleared"})

if __name__ == "__main__":
    app.run(debug=True)