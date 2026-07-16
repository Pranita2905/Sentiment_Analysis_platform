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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sentiment Analysis Dashboard</title>
    <style>
        :root {
            --bg-main: #f8fafc;
            --panel-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --border: #e2e8f0;
            
            --pos-bg: #f0fdf4;
            --pos-text: #166534;
            --pos-border: #bbf7d0;
            
            --neg-bg: #fef2f2;
            --neg-text: #991b1b;
            --neg-border: #fecaca;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 24px;
        }

        .dashboard {
            width: 100%;
            max-width: 680px;
            background: var(--panel-bg);
            padding: 40px;
            border-radius: 16px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }

        .header {
            margin-bottom: 32px;
        }

        h1 {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: var(--text-main);
            margin-bottom: 6px;
        }

        .subtitle {
            font-size: 14px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .form-group {
            margin-bottom: 24px;
        }

        label {
            display: block;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        textarea {
            width: 100%;
            height: 160px;
            padding: 16px;
            font-size: 15px;
            line-height: 1.5;
            border-radius: 10px;
            border: 1px solid var(--border);
            background-color: #fafafa;
            resize: none;
            color: var(--text-main);
            transition: all 0.2s ease;
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary);
            background-color: var(--panel-bg);
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        button {
            width: 100%;
            padding: 14px;
            background: var(--primary);
            border: none;
            color: white;
            font-size: 15px;
            font-weight: 600;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        button:hover {
            background: var(--primary-hover);
        }

        .result {
            margin-top: 24px;
            padding: 18px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            border: 1px solid transparent;
            animation: fadeIn 0.3s ease-in-out;
        }

        .pos {
            background: var(--pos-bg);
            color: var(--pos-text);
            border-color: var(--pos-border);
        }

        .neg {
            background: var(--neg-bg);
            color: var(--neg-text);
            border-color: var(--neg-border);
        }

        .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            text-align: center;
            font-size: 13px;
            color: var(--text-muted);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(4px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<div class="dashboard">
    <div class="header">
        <h1>Sentiment Analysis</h1>
        <div class="subtitle">Logistic Regression + TF-IDF Production Environment</div>
    </div>

    <form method="POST">
        <div class="form-group">
            <label for="review">Input Text</label>
            <textarea
                id="review"
                name="review"
                placeholder="Type or paste sample text here to evaluate sentiment classification..."
                required>{{review}}</textarea>
        </div>
        <button type="submit">Run Inference Pipeline</button>
    </form>

    {% if prediction %}
    <div class="result {{color}}">
        {{prediction}}
    </div>
    {% endif %}

    <div class="footer">
        System engineered by Pranita
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
            prediction = "✨ Positive Sentiment Detected"
            color = "pos"
        else:
            prediction = "⚠️ Negative Sentiment Detected"
            color = "neg"

    return render_template_string(
        HTML,
        prediction=prediction,
        color=color,
        review=review
    )

if __name__ == "__main__":
    app.run()
