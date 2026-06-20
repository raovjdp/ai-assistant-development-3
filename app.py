import os
import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Feedback log file path
FEEDBACK_FILE = 'feedback_log.csv'

# Initialize feedback CSV if it doesn't exist
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Function', 'Prompt_Style', 'User_Input', 'AI_Response', 'Is_Helpful'])

# Mock AI Engine for demonstration (Replace with actual 'google-genai' or 'openai' API calls)
def call_ai_model(final_prompt):
    # Simulated responses based on keywords for offline testing
    prompt_lower = final_prompt.lower()
    if "capital of france" in prompt_lower:
        return "The capital of France is Paris, a global center for art, fashion, gastronomy, and culture."
    elif "summarize" in prompt_lower or "summary" in prompt_lower:
        return "[Summary] The provided text discusses key themes, condensing the core message into a concise, easily digestible format."
    elif "dragon" in prompt_lower or "story" in prompt_lower:
        return "Once upon a time, in a valley shrouded in mist, a gentle dragon named Ignis guarded a princess who preferred books over balls..."
    return f"This is a simulated AI response tailored to your prompt: \n\n\"{final_prompt[:100]}...\""

# 2. Prompt Design Matrix (3 Functions x 3 Style Variations each)
PROMPT_TEMPLATES = {
    "qa": {
        "concise": "Provide a direct, single-sentence factual answer to this query: {input}",
        "detailed": "Provide an in-depth, detailed explanation covering the history and context of: {input}",
        "creative_fact": "Explain the following concept as if you are a passionate tour guide or storyteller: {input}"
    },
    "summary": {
        "bullet": "Summarize the following text using exactly three high-impact bullet points:\n\n{input}",
        "professional": "Provide a professional, executive summary paragraph of the following text:\n\n{input}",
        "casual": "Explain the main takeaway of this text in one simple, casual sentence for a non-expert:\n\n{input}"
    },
    "creative": {
        "fairytale": "Write a whimsical, classic fairytale opening based on this idea: {input}",
        "sci_fi": "Generate a gritty, futuristic cyberpunk scene or plot hook based on this idea: {input}",
        "poetic": "Compose an emotionally resonant, short poem reflecting this theme: {input}"
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        function_type = request.form.get('function_type')
        prompt_style = request.form.get('prompt_style')
        user_input = request.form.get('user_input')
        
        # Construct dynamic prompt using our template matrix
        template = PROMPT_TEMPLATES.get(function_type, {}).get(prompt_style, "{input}")
        formatted_prompt = template.format(input=user_input)
        
        # Get response from AI
        ai_response = call_ai_model(formatted_prompt)
        
        return jsonify({
            'status': 'success',
            'formatted_prompt': formatted_prompt,
            'ai_response': ai_response
        })
        
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def save_feedback():
    data = request.json
    import datetime
    
    with open(FEEDBACK_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('function'),
            data.get('style'),
            data.get('input'),
            data.get('response'),
            data.get('helpful')
        ])
    return jsonify({'status': 'feedback_saved'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
