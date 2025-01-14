from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# إضافة المسار الرئيسي للمشروع إلى مسار بايثون
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew import crew  # استيراد كائن Crew الخاص بك
from custom_agent import get_gemini_response

app = Flask(__name__)

# **هام:** قم بتحديث `origins` بعنوان URL لخادم الواجهة الأمامية الخاص بك
CORS(app, resources={r"/upload": {"origins": "https://your-frontend-server.com"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'لم يتم تضمين أي جزء للصورة'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار أي صورة'}), 400
    if file:
        image_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(image_path)

        # الحصول على الوصف من Gemini
        response_from_gemini = get_gemini_response(image_path)

        # تشغيل عملية CrewAI
        result = crew.kickoff(inputs={'description': response_from_gemini.text})

        # قراءة ملف HTML الذي تم إنشاؤه
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                generated_html = f.read()
        except FileNotFoundError:
            return jsonify({'error': 'لم يتم العثور على ملف HTML الذي تم إنشاؤه'}), 500

        return jsonify({'html': generated_html})

if __name__ == '__main__':
    app.run(debug=True)
