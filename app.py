from flask import Flask, render_template, request, jsonify
from chatbot import handle_response
from langchain.memory import ConversationBufferMemory
import markdown  # To convert markdown to HTML

app = Flask(__name__)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    memory.save_context({"input": user_input}, {"output": ""})

    chat_history = memory.load_memory_variables({})["chat_history"]
    history_text = ""
    for msg in chat_history:
        if msg.type == "human":
            history_text += f"User: {msg.content}\n"
        elif msg.type == "ai":
            history_text += f"Assistant: {msg.content}\n"

    prompt = history_text + f"User: {user_input}\nAssistant:"
    bot_response = handle_response(prompt)

    # Convert markdown to HTML for better formatting
    formatted_response = markdown.markdown(bot_response)

    memory.chat_memory.add_ai_message(bot_response)
    return jsonify({'response': formatted_response})

if __name__ == "__main__":
    app.run(debug=True)
