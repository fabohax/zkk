import qrcode
from qrcode.image.svg import SvgPathImage

def generate_qr_code(data, public_key, output_dir="."):
    """
    Generate a QR code from the given data and save it as an SVG file.
    The filename includes the public key for identification.
    """
    # Create a QR code instance
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)

    # Construct output filename with public key
    output_svg = f"{output_dir}/zkp_qr_{public_key[:8]}.svg"

    # Save the QR code as an SVG file
    img = qr.make_image(image_factory=SvgPathImage)
    img.save(output_svg)
    print(f"QR Code saved as {output_svg}")