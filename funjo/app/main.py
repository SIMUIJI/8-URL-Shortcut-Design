from flask import Flask, request, redirect, jsonify, render_template
import hashlib
import os
import psycopg2  # PostgreSQL 데이터베이스 연결을 위한 라이브러리
import redis  # Redis 캐시를 위한 라이브러리

app = Flask(__name__)

# 데이터베이스 연결
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

@app.route('/api/v1/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('longUrl')
    if not long_url:  # 긴 URL이 비어있을 경우 오류 처리
        return jsonify({'error': 'longUrl is required'}), 400

    # 해시 함수로 단축 URL 생성
    short_url = hashlib.md5(long_url.encode()).hexdigest()[:7]  # 해시값을 7자로 자름

    # DB에 URL 저장 (is_enable 기본값 1)
    cursor.execute("INSERT INTO urls (short_url, long_url, is_enable) VALUES (%s, %s, %s)", (short_url, long_url, 1))
    conn.commit()

    return jsonify({'shortUrl': short_url}), 201

@app.route('/api/v1/getLongUrl', methods=['POST'])
def get_long_url():
    short_url = request.json.get('shortUrl')
    if not short_url:  # 단축 URL이 비어있을 경우 오류 처리
        return jsonify({'error': 'shortUrl is required'}), 400

    cursor.execute("SELECT long_url, is_enable FROM urls WHERE short_url = %s", (short_url,))
    result = cursor.fetchone()
    
    if result:
        if result[1] == 1:  # is_enable이 1인 경우에만 긴 URL 반환
            return jsonify({'longUrl': result[0]}), 200
        else:
            return jsonify({'error': 'This URL is disabled'}), 403  # URL이 비활성화된 경우 오류 반환

    return jsonify({'error': 'URL not found'}), 404

@app.route('/api/v1/toggleUrl/<short_url>', methods=['PUT'])
def toggle_url(short_url):
    cursor.execute("SELECT is_enable FROM urls WHERE short_url = %s", (short_url,))
    result = cursor.fetchone()

    if result:
        new_status = 0 if result[0] == 1 else 1  # 현재 상태 반전
        cursor.execute("UPDATE urls SET is_enable = %s WHERE short_url = %s", (new_status, short_url))
        conn.commit()
        return jsonify({'shortUrl': short_url, 'newStatus': new_status}), 200

    return jsonify({'error': 'URL not found'}), 404

@app.route('/api/v1/shortUrl/<short_url>', methods=['GET'])
def redirect_url(short_url):
    cursor.execute("SELECT long_url, is_enable FROM urls WHERE short_url = %s", (short_url,))
    result = cursor.fetchone()

    if result and result[1] == 1:  # is_enable이 1일 때만 리디렉션
        return redirect(result[0], code=302)  # 리디렉션
    return {"error": "URL not found or disabled"}, 404

@app.route('/api/v1/urls', methods=['GET'])
def get_urls():
    cursor.execute("SELECT short_url, long_url, is_enable FROM urls")  # short_url, long_url, is_enable 선택
    urls = cursor.fetchall()
    return jsonify(urls)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
