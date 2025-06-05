from flask import Flask, request, jsonify, make_response
import os

app = Flask(__name__)

# Pertanyaan DASS-21 dengan kode baru
questions = [
    "D1 Saya sama sekali tidak dapat merasakan perasaan positif (contoh: merasa gembira, bangga, dsb).",
    "D2 Saya merasa sulit berinisiatif melakukan sesuatu.",
    "D3 Saya merasa tidak ada lagi yang bisa saya harapkan.",
    "D4 Saya merasa sedih dan tertekan.",
    "D5 Saya tidak bisa merasa antusias terhadap hal apapun.",
    "D6 Saya merasa diri saya tidak berharga.",
    "D7 Saya merasa hidup ini tidak berarti.",
    "A1 Saya merasa rongga mulut saya kering.",
    "A2 Saya merasa kesulitan bernafas (misalnya seringkali terengah-engah atau tidak dapat bernapas padahal tidak melakukan aktivitas fisik sebelumnya).",
    "A3 Saya merasa gemetar (misalnya pada tangan).",
    "A4 Saya merasa khawatir dengan situasi dimana saya mungkin menjadi panik dan mempermalukan diri sendiri.",
    "A5 Saya merasa hampir panik.",
    "A6 Saya menyadari kondisi jantung saya (seperti meningkatnya atau melemahnya detak jantung) meskipun sedang tidak melakukan aktivitas fisik.",
    "A7 Saya merasa ketakutan tanpa alasan yang jelas.",
    "S1 Saya merasa sulit untuk beristirahat.",
    "S2 Saya cenderung menunjukkan reaksi berlebihan terhadap suatu situasi.",
    "S3 Saya merasa energi saya terkuras karena terlalu cemas.",
    "S4 Saya merasa gelisah.",
    "S5 Saya merasa sulit untuk merasa tenang.",
    "S6 Saya sulit untuk bersabar dalam menghadapi gangguan yang terjadi ketika sedang melakukan sesuatu.",
    "S7 Perasaan saya mudah tergugah atau tersentuh."
]

# Indeks pertanyaan untuk masing-masing skala (tidak perlu digunakan pada penilaian dengan input D/A/S array)
dass21_keys = ['D', 'A', 'S']

# Interpretasi skor tetap
dass21_scale = {
    "Depresi": [(0, 9, "Normal"), (10, 13, "Ringan"), (14, 20, "Sedang"), (21, 27, "Berat"), (28, 100, "Sangat berat")],
    "Kecemasan": [(0, 7, "Normal"), (8, 9, "Ringan"), (10, 14, "Sedang"), (15, 19, "Berat"), (20, 100, "Sangat berat")],
    "Stres": [(0, 14, "Normal"), (15, 18, "Ringan"), (19, 25, "Sedang"), (26, 33, "Berat"), (34, 100, "Sangat berat")]
}

@app.route("/dass21/questions", methods=["GET"])
def get_questions():
    return jsonify({
        "status": "success",
        "questions": questions
    })

@app.route("/dass21/score", methods=["POST"])
def calculate_score():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON data"}), 400

        # Validasi: Pastikan D, A, dan S ada dan masing-masing panjang 7, isinya int 0-3
        for scale in ["D", "A", "S"]:
            if scale not in data:
                return jsonify({"error": f"Missing key '{scale}' in request body"}), 400
            if not isinstance(data[scale], list) or len(data[scale]) != 7:
                return jsonify({"error": f"Data '{scale}' harus berupa array 7 angka, tiap item 0-3"}), 400
            for idx, val in enumerate(data[scale]):
                if not isinstance(val, int) or val < 0 or val > 3:
                    return jsonify({"error": f"Nilai {scale}[{idx}] harus 0, 1, 2, atau 3"}), 400

        # Hitung skor
        scores = {
            "Depresi": sum(data["D"]) * 2,
            "Kecemasan": sum(data["A"]) * 2,
            "Stres": sum(data["S"]) * 2
        }

        categories = {}
        for scale, scale_name in zip(["D", "A", "S"], ["Depresi", "Kecemasan", "Stres"]):
            total = scores[scale_name]
            cat = next(cat for (low, high, cat) in dass21_scale[scale_name] if low <= total <= high)
            categories[scale_name] = cat

        response = {
            "status": "success",
            "scores": scores,
            "categories": categories,
            "interpretation": {
                scale: f"Skor = {scores[scale]} → {categories[scale]}"
                for scale in ["Depresi", "Kecemasan", "Stres"]
            }
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=int(os.environ.get("PORT", 8080)))