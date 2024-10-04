from flask import Flask, render_template, request, jsonify
import damageUtils


app = Flask(__name__, template_folder='templates')

@app.route("/")
def details():
    return render_template("details.html")

@app.route("/submit_claim_details", methods=["POST", "GET"])
def submit_claim_details():

    user_description = request.form["description-of-accident"]
    image_path = "headlight3.jfif.jpg"

    response = jsonify({
        "message" : damageUtils.output(image_path, user_description)
    })

    return response

if __name__ == '__main__':
    app.run(debug=True)

