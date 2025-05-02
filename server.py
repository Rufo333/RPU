from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/score-understanding", methods=["POST"])
def score_understanding():
    data = request.json
    answers = data.get("answers", [])

    prompt = f"""
You are an evaluator of deep, human intelligence and symbolic thought. Score each of the following answers from 0 to 1 based on:
- Emotional depth
- Ability to hold paradox
- Metaphor/symbolism
- Empathy
- Philosophical insight

Return a JSON object:
{{
  "u1_score": float,
  "u2_score": float,
  "u3_score": float,
  "average": float,
  "reflections": [str, str, str]
}}

Answers:
1. {answers[0]}
2. {answers[1]}
3. {answers[2]}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a poetic evaluator of human understanding."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        text = response.choices[0].message["content"]
        return jsonify(eval(text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
