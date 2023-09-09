from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/sms',methods=['GET'])
def receive():
    sms_content = request.form.get('content')
    print(f'received {sms_content}')
    return jsonify(status='success')


if __name__ == '__main__':
    app.run(debug=True)
