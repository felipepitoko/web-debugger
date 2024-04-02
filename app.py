import json
from flask import Flask, request, render_template
from datetime import datetime
from flask import jsonify

app = Flask(__name__) 
app.debug = True
@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'GET':
            print('Send html')
            #send "hello-world.html" from templates as response
            return render_template('hello-world.html')
        else:        
            if request.is_json:
                data = request.json
                nome_arquivo = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
                with open(f"received/{nome_arquivo}.json", 'w') as file:
                    json.dump(data, file)

                return 'JSON data saved to file successfully'
            else:
                return 'No JSON data found in the request body', 400
    except Exception as e:
        print(e)
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500
    
@app.route('/teste', methods=['GET'])
def teste_on():
    return ({"teste": "nah"}, 200)

#set the app to auto reload everytime the code changes
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=8080, debug=True)