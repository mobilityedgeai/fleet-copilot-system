import os
import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Debug - mostrar caminhos
print("=== DEBUG PATHS ===")
print(f"__file__: {__file__}")
print(f"dirname(__file__): {os.path.dirname(__file__)}")
print(f"dirname(dirname(__file__)): {os.path.dirname(os.path.dirname(__file__))}")

# Tentar diferentes caminhos para templates
template_paths = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    os.path.join(os.path.dirname(__file__), 'templates'),
    'templates',
    '../templates'
]

for path in template_paths:
    abs_path = os.path.abspath(path)
    exists = os.path.exists(abs_path)
    print(f"Template path: {path} -> {abs_path} (exists: {exists})")
    if exists:
        files = os.listdir(abs_path)
        print(f"  Files: {files}")

# Usar o primeiro caminho que existe
template_dir = None
for path in template_paths:
    if os.path.exists(path):
        template_dir = path
        break

print(f"Using template_dir: {template_dir}")
print("=== END DEBUG ===")

# Criar app Flask
if template_dir:
    app = Flask(__name__, template_folder=template_dir)
else:
    app = Flask(__name__)  # Usar padrão

@app.route('/')
def index():
    return "Flask is running! Check logs for template debug info."

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Fleet Copilot BI Server is running'}

@app.route('/debug')
def debug():
    return f"Template folder: {app.template_folder}"

# Suas outras rotas aqui...
@app.route('/api/copilot/dashboard')
def dashboard_menu():
    enterprise_id = request.args.get('enterpriseId', 'qzDVZ1jB6IC60baxtsDU')
    return render_template('dashboard_menu.html', enterprise_id=enterprise_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
