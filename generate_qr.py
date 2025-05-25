import qrcode

valid_ids = ['24567', '12345', '77777', '00001']

invalid_ids = ['99999', '11111', '54321', '66666']

for id_ in valid_ids:
    img = qrcode.make(id_)
    img.save(f'valid_qr_{id_}.png')
    print(f"[OK] Действительный QR: valid_qr_{id_}.png")

for id_ in invalid_ids:
    img = qrcode.make(id_)
    img.save(f'invalid_qr_{id_}.png')
    print(f"[!] Недействительный QR: invalid_qr_{id_}.png")