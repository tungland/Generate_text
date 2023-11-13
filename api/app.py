from flask import Flask, request, jsonify
from gensim.models import KeyedVectors

app = Flask(__name__)

# Load your word2vec model here
model = KeyedVectors.load("fifth_capital_ddc.model")

@app.route('/wordvector/')
def home():
    return '''
    <html>
        <head><title>Instructions</title></head>
        <body>
            <h2>How to Use the Word Vector Service</h2>
            <p>Follow these steps to retrieve word vectors:</p>
            <ol>
                <li><strong>Prepare a JSON Request</strong>: Create a JSON object</li>
                <li><strong>Send the Request</strong>: Send a POST request to https://dh.nb.no/run/wordvector/get_vector with the JSON payload.</li>
                <li>You can use tools like Postman, or a simple curl command in the terminal</li>
                <li><strong>Example</strong>: curl -X POST https://dh.nb.no/run/wordvector/get_vector -H "Content-Type: application/json" -d '{"word": "example"}'</li>
                <li><strong>Receive the Response</strong>: The response will be a JSON object containing the word vector</li>
            </ol>
        </body>
    </html>
    '''


@app.route('/wordvector/get_vector', methods=['POST'])
def get_vector():
    data = request.json
    words = data.get('words')  # Expecting a list of words

    if not isinstance(words, list):
        return jsonify({"error": "Input should be a list of words"}), 400

    response = {}
    for word in words:
        if word in model.wv:
            response[word] = model.wv[word].tolist()  # Convert numpy array to list for JSON serialization
        else:
            response[word] = "Word not found in model"

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)