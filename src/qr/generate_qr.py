import qrcode
from qrcode.image.svg import SvgPathImage

def generate_qr_code(data, output_svg="zkp_qr.svg"):
    """
    Generate a QR code from the given data and save it as an SVG file.
    """
    # Create a QR code instance
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)

    # Save the QR code as an SVG file
    img = qr.make_image(image_factory=SvgPathImage)
    img.save(output_svg)
    print(f"QR Code saved as {output_svg}")
