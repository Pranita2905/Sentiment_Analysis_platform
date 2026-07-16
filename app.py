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
    <title>AI Sentiment Intelligence</title>
    <style>
        :root {
            --bg-color: #090d16;
            --card-bg: rgba(17, 24, 39, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            
            /* Neon Glow Gradients */
            --primary-grad: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --primary-glow: rgba(99, 102, 241, 0.4);
            
            /* Status Colors */
            --pos-bg: rgba(16, 185, 129, 0.1);
            --pos-border: rgba(16, 185, 129, 0.3);
            --pos-glow: rgba(16, 185, 129, 0.2);
            --pos-text: #34d399;
            
            --neg-bg: rgba(239, 68, 68, 0.1);
            --neg-border: rgba(239, 68, 68, 0.3);
            --neg-glow: rgba(239, 68, 68, 0.2);
            --neg-text: #f87171;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
            color: var(--text-primary);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }

        .container {
            width: 100%;
            max-width: 600px;
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 40px;
            border-radius: 24px;
            border: 1px solid var(--border-color);
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
            position: relative;
        }

        /* Subtle top ambient glow bar */
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 10%;
            right: 10%;
            height: 2px;
            background: var(--primary-grad);
            filter: blur(4px);
        }

        .header {
            text-align: center;
            margin-bottom: 35px;
        }

        h1 {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -1px;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .subtitle {
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        .form-group {
            margin-bottom: 24px;
            position: relative;
        }

        label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }

        textarea {
            width: 100%;
            height: 150px;
            padding: 20px;
            font-size: 16px;
            line-height: 1.6;
            color: var(--text-primary);
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            resize: none;
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        textarea:focus {
            border-color: #818cf8;
            background: rgba(15, 23, 42, 0.8);
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.15);
        }

        button {
            width: 100%;
            padding: 16px;
            background: var(--primary-grad);
            border: none;
            color: white;
            font-size: 16px;
            font-weight: 700;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px var(--primary-glow);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--primary-glow);
            filter: brightness(1.1);
        }

        button:active {
            transform: translateY(0);
        }

        .result {
            margin-top: 28px;
            padding: 20px;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            border: 1px solid transparent;
            animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .pos {
            background: var(--pos-bg);
            color: var(--pos-text);
            border-color: var(--pos-border);
            box-shadow: 0 10px 20px -5px var(--pos-glow);
        }

        .neg {
            background: var(--neg-bg);
            color: var(--neg-text);
            border-color: var(--neg-border);
            box-shadow: 0 10px 20px -5px var(--neg-glow);
        }

        .footer {
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            font-size: 12px;
            color: var(--text-secondary);
            letter-spacing: 0.5px;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    <!-- Importing modern font -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Sentiment AI</h1>
        <div class="subtitle">NLP Inference Engine</div>
    </div>

    <form method="POST">
        <div class="form-group">
            <label for="review">Analyze Text Sentiment</label>
            <textarea
                id="review"
                name="review"
                placeholder="Type or paste your review here to run the sentiment classification model..."
                required>{{review}}</textarea>
        </div>
        <button type="submit">Analyze Sentiment</button>
    </form>

    {% if prediction %}
    <div class="result {{color}}">
        {{prediction}}
    </div>
    {% endif %}

    <div class="footer">
        Crafted by Pranita
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
