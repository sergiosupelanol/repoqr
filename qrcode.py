import io
import pyqrcode
from base64 import b64encode, b64decode
import json
import os
from datetime import datetime
import eel

# Initialize eel with web directory
eel.init('web')

# Crear directorio para guardar QR codes si no existe
SAVE_DIR = 'saved_qrcodes'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


@eel.expose()
def generate_qr(data):
    img = pyqrcode.create(data)
    buffers = io.BytesIO()
    img.png(buffers, scale=8)
    encoded = b64encode(buffers.getvalue()).decode("ascii")
    print("QR code generation successful")
    return "data:image/png;base64, " + encoded


@eel.expose()
def save_qr(data, image_data):
    try:
        # Crear nombre de archivo único usando timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_code_{timestamp}.png"
        filepath = os.path.join(SAVE_DIR, filename)

        # Eliminar el prefijo de datos base64 y decodificar
        image_data = image_data.replace("data:image/png;base64, ", "")
        image_bytes = b64decode(image_data)

        # Guardar la imagen
        with open(filepath, 'wb') as f:
            f.write(image_bytes)

        # Guardar registro en JSON
        save_to_history(data, filepath)

        print(f"QR saved successfully at: {filepath}")
        return {"success": True, "path": filepath}
    except Exception as e:
        print(f"Error saving QR: {str(e)}")
        return {"success": False, "error": str(e)}


def save_to_history(data, filepath):
    history_file = 'qr_history.json'
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Crear entrada de historial
    entry = {
        'timestamp': timestamp,
        'data': data,
        'filepath': filepath
    }

    # Cargar historial existente o crear nuevo
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    # Añadir nueva entrada y guardar
    history.append(entry)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)


@eel.expose()
def get_save_location():
    """Retorna la ubicación donde se guardan los QR codes"""
    return os.path.abspath(SAVE_DIR)


eel.start('index.html', size=(960, 600))