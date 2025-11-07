from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TARGET_BASE_URL = "https://services.zentrades.pro"

@app.route("/proxy", methods=["POST"])
def proxy_request():
    try:
        data = request.get_json()

        # Required fields
        target_url = data.get("url")
        method = data.get("method", "GET").upper()
        headers = data.get("headers", {})
        body = data.get("body", {})

        if not target_url:
            return jsonify({"error": "Missing 'url' in request"}), 400

        # ✅ Override the origin
        headers["origin"] = "https://app.zentrades.pro"

        # Forward the request
        if method == "GET":
            resp = requests.get(target_url, headers=headers, params=body)
        elif method == "POST":
            resp = requests.post(target_url, headers=headers, json=body)
        elif method == "PUT":
            resp = requests.put(target_url, headers=headers, json=body)
        else:
            return jsonify({"error": "Unsupported method"}), 400

        # Return response directly
        return (resp.text, resp.status_code, {"Content-Type": resp.headers.get("Content-Type", "application/json")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "✅ Zentrades Proxy is running on Render"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
