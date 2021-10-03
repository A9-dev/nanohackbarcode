import cv2
from pyzbar import pyzbar
import requests
import json

last_barcode = ""


def send_data(obj):
    x = requests.post(
        "https://roomify.electrokid.co.uk/api/barcode",
        headers={"key": "roomify123", "roomid": "1"},
        data=obj,
    )
    print(x.text)


def decode(image):
    global last_barcode
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        if obj.data != last_barcode:
            last_barcode = obj.data
            print(last_barcode)
            send_data(json.dumps({"barcode": last_barcode.decode("utf-8")}))
    return image


if __name__ == "__main__":

    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)
        img = decode(frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("preview")

    # show the image
    cv2.imshow("img", img)
    cv2.waitKey(0)
