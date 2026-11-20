from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    error = None

    if request.method == 'POST':
        router_device = {
            'device_type': 'cisco_ios_telnet',
            'ip': '192.168.10.33',
            'port': 32770,
            'username': 'admin',
            'password': 'eve123',
            'secret': 'eve123'
        }

        net_connect = None
        try:
            print("Connecting to the router...")
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()
            
            commands_to_run = [
                "show version",
                "show ip interface brief",
                "show running-config"
            ]

            for cmd in commands_to_run:
                print(f"\n--- Output for: {cmd} ---")
                output = net_connect.send_command(cmd)
                results[cmd] = output  
                print(output)

        except Exception as e:
            error = f"Connection failed: {e}"
        finally:
            if net_connect is not None:
                net_connect.disconnect()
                print("\nDisconnected successfully.")

    return render_template('index.html', results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)