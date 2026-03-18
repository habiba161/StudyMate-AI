from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form["topic"]
        response = f"AI Explanation for: {user_input}"  # temporary (we add real AI later)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)