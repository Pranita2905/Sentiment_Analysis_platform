from flask import Flask, request, render_template_string
import pickle

app = Flask(__name__)

# Load Model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Load Vectorizer
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

HTML = """
<!DOCTYPE html>
<html>
<head>

<title>Sentiment Analysis</title>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Segoe UI,sans-serif;
}

body{

background:linear-gradient(135deg,#0f172a,#2563eb);
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
padding:20px;

}

.container{

width:100%;
max-width:900px;
background:white;
padding:40px;
border-radius:20px;
box-shadow:0 10px 30px rgba(0,0,0,.25);

}

h1{

text-align:center;
color:#1e40af;
margin-bottom:10px;

}

p{

text-align:center;
color:#64748b;
margin-bottom:30px;

}

textarea{

width:100%;
height:220px;
padding:18px;
font-size:17px;
border-radius:12px;
border:1px solid #ccc;
resize:none;

}

button{

margin-top:20px;
width:100%;
padding:16px;
background:#2563eb;
border:none;
color:white;
font-size:20px;
border-radius:12px;
cursor:pointer;

}

button:hover{

background:#1d4ed8;

}

.result{

margin-top:30px;
padding:20px;
border-radius:15px;
text-align:center;
font-size:28px;
font-weight:bold;

}

.pos{

background:#dcfce7;
color:#15803d;

}

.neg{

background:#fee2e2;
color:#dc2626;

}

.footer{

margin-top:30px;
text-align:center;
color:#64748b;

}

</style>

</head>

<body>

<div class="container">

<h1>😊 Sentiment Analysis System</h1>

<p>Logistic Regression + TF-IDF + Flask</p>

<form method="POST">

<textarea
name="review"
placeholder="Enter your review here..."
required>{{review}}</textarea>

<button type="submit">

Analyze Sentiment

</button>

</form>

{% if prediction %}

<div class="result {{color}}">

{{prediction}}

</div>

{% endif %}

<div class="footer">

Developed by Pranita

</div>

</div>

</body>

</html>
"""

@app.route("/", methods=["GET","POST"])
def home():

    prediction = ""
    color = ""
    review = ""

    if request.method == "POST":

        review = request.form["review"]

        vector = vectorizer.transform([review])

        pred = model.predict(vector)[0]

        if pred == 1:

            prediction = "😊 Positive Review"

            color = "pos"

        else:

            prediction = "😞 Negative Review"

            color = "neg"

    return render_template_string(

        HTML,

        prediction=prediction,

        color=color,

        review=review

    )

if __name__ == "__main__":
    app.run()
