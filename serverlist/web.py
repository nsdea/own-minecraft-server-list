import flask
import mcstatus

app = flask.Flask(__name__, static_url_path='/')

def color_codes(text: str):
    text = text.strip(' <>')
    num = 0

    codes = {
        '0': 'color: #000000',
        '1': 'color: #0000AA',
        '2': 'color: #00AA00',
        '3': 'color: #00AAAA',
        '4': 'color: #AA0000',
        '5': 'color: #AA00AA',
        '6': 'color: #FFAA00',
        '7': 'color: #AAAAAA',
        '8': 'color: #555555',
        '9': 'color: #5555FF',

        'a': 'color: #55FF55',
        'b': 'color: #55FFFF',
        'c': 'color: #FF5555',
        'd': 'color: #FF55FF',
        'e': 'color: #FFFF55',
        'f': 'color: #FFFFFF',
        
        'l': 'font-weight: bold',
        'm': 'text-decoration:line-through',
        'n': 'text-decoration:underline',
        'o': 'font-style:italic'
    }

    for code in codes.keys():
        text = text.replace(f'§{code}', f'<span style="{codes[code]};">') 
        num += 1

    return text + num*'</span>'

def get_infos(*ips):
    server_data = []

    for ip in ips:
        data = mcstatus.JavaServer.lookup(ip).status()
        text = color_codes(data.description)
        ping = data.latency

        if ping > 0:    color = 'cyan'
        if ping > 20:   color = 'lightgreen'
        if ping > 100:  color = 'yellow'
        if ping > 200:  color = 'orange'
        if ping > 500:  color = 'red'

        server_data.append({'ip': ip, 'data': data, 'text': text, 'color': color})
    
    return server_data

@app.route('/')
def index():
    return flask.render_template('index.html', servers=get_infos('hypixel.net', 'gommehd.net', '2b2t.org', 'neruxvace.net'))

@app.route('/only/<ip>')
def server(ip):
    return flask.render_template('index.html', servers=get_infos(ip))

app.run(port=1111, debug=True)