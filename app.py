from flask import Flask, jsonify, request
import face_recognition


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/compare", methods=["POST"])
def compare():
    if "profile_photo" not in request.files or "selfie" not in request.files:
        return jsonify({"error": "missing_files"}), 400

    profile_file = request.files["profile_photo"]
    selfie_file = request.files["selfie"]

    try:
        profile_image = face_recognition.load_image_file(profile_file)
        selfie_image = face_recognition.load_image_file(selfie_file)
    except Exception:
        return jsonify({"error": "invalid_image"}), 400

    profile_encodings = face_recognition.face_encodings(profile_image)
    if not profile_encodings:
        return jsonify({"error": "no_face_detected_in_profile_photo"})

    selfie_encodings = face_recognition.face_encodings(selfie_image)
    if not selfie_encodings:
        return jsonify({"error": "no_face_detected_in_selfie"})

    distance = face_recognition.face_distance(
        [profile_encodings[0]], selfie_encodings[0]
    )[0]

    return jsonify({"distance": float(distance)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
