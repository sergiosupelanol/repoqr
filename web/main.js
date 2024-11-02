async function generateQr() {
    var data = document.getElementById('data').value;
    if (!data) {
        alert('Por favor ingrese texto para generar el código QR');
        return;
    }
    try {
        let result = await eel.generate_qr(data)();
        setImage(result);
        // Habilitar el botón de guardar
        document.getElementById('saveButton').disabled = false;
    } catch (error) {
        alert('Error al generar el código QR');
        console.error(error);
    }
}

function setImage(base64) {
    document.getElementById("qr").src = base64;
}

function clearImage() {
    document.getElementById("qr").src = "";
    document.getElementById("data").value = "";
    document.getElementById('saveButton').disabled = true;
}

async function saveQR() {
    const data = document.getElementById('data').value;
    const qrImage = document.getElementById('qr').src;

    if (!qrImage || !data) {
        alert('Por favor genere un código QR primero');
        return;
    }

    try {
        const result = await eel.save_qr(data, qrImage)();
        if (result.success) {
            const saveLocation = await eel.get_save_location()();
            alert(`QR guardado exitosamente!\nUbicación: ${saveLocation}`);
        } else {
            alert('Error al guardar el QR: ' + result.error);
        }
    } catch (error) {
        alert('Error al guardar el QR');
        console.error(error);
    }
}