from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/checkout", methods=["GET"])
def checkout():
    product = request.args.get("product")
    price = request.args.get("price")
    return render_template("page.html", product=product, price=price)

@app.route("/api/<product>", methods=["POST"])
def purchase(product):
    price = request.form.get("price")
    return redirect(url_for("checkout", product=product, price=price))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

