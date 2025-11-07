from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/proxy", methods=["POST"])
def proxy_request():
    data = request.get_json()
    endpoint = data.get("endpoint")
    headers = data.get("headers", {})
    ticket_id = data.get("ticketId")
    body = data.get("body", {})

    if not endpoint or not headers or not ticket_id:
        return jsonify({"error": "Missing required data"}), 400

    # Ensure correct Origin
    headers["origin"] = "https://app.zentrades.pro"

    try:
        url = f"https://services.zentrades.pro{endpoint}"
        response = requests.post(url, headers=headers, json=body, timeout=30)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
