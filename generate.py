import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
import textwrap
import qrcode
import pyperclip
import webbrowser

# --------------------- UI Functions ---------------------

def draw_buttons(frame):
    cv2.rectangle(frame, (50, 100), (250, 200), (100, 200, 100), -1)
    cv2.putText(frame, "Image Scan", (70, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.rectangle(frame, (350, 100), (550, 200), (100, 100, 255), -1)
    cv2.putText(frame, "Live Scan", (370, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, "Press 'g' to Generate QR", (160, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

def draw_wrapped_text(img, text, origin, max_width=35, font=cv2.FONT_HERSHEY_SIMPLEX,
                      font_scale=0.9, color=(0, 0, 0), thickness=3, line_height=28):
    wrapped = textwrap.wrap(text, width=max_width)
    x, y = origin
    for i, line in enumerate(wrapped):
        y_offset = y + i * line_height
        # White shadow (background)
        cv2.putText(img, line, (x + 1, y_offset + 1), font, font_scale, (255, 255, 255), thickness + 2)
        # Black text on top
        cv2.putText(img, line, (x, y_offset), font, font_scale, color, thickness)

def detect_qr_type(data):
    if data.startswith("http://") or data.startswith("https://"):
        return "URL"
    elif data.startswith("WIFI:"):
        return "WiFi Config"
    elif data.startswith("BEGIN:VCARD"):
        return "vCard (Contact)"
    elif data.startswith("SMSTO:"):
        return "SMS"
    elif data.startswith("MATMSG:"):
        return "Email"
    elif data.startswith("tel:"):
        return "Phone Number"
    else:
        return "Text"

# --------------------- QR Scan Functions ---------------------

def scan_qr_from_image(image_path):
    image = cv2.imread(image_path)
    data_found = []
    decoded_objects = decode(image)
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        data_found.append(data)
        pts = [tuple(point) for point in obj.polygon]
        cv2.polylines(image, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 2)
        qr_type = detect_qr_type(data)
        label = f"[{qr_type}] {data}"
        draw_wrapped_text(image, label, (pts[0][0], pts[0][1] - 10), max_width=35)

        if qr_type == "URL":
            pyperclip.copy(data)
            webbrowser.open(data) 
            print(f"[Copied to Clipboard] {data}")

    return image, data_found


def image_scan_mode():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        scanned_img, results = scan_qr_from_image(file_path)
        if not results:
            cv2.putText(scanned_img, "No QR Code Found", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("Image QR Scanner", scanned_img)
        cv2.waitKey(0)
        cv2.destroyWindow("Image QR Scanner")

def live_scan_mode():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access camera.")
        return

    copied_urls = set()  # prevent duplicate copies

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode("utf-8")
            pts = [tuple(point) for point in obj.polygon]
            cv2.polylines(frame, [np.array(pts, dtype=np.int32)], True, (255, 0, 0), 2)
            qr_type = detect_qr_type(data)
            label = f"[{qr_type}] {data}"
            draw_wrapped_text(frame, label, (pts[0][0], pts[0][1] - 10), max_width=35)

            if qr_type == "URL" and data not in copied_urls:
                pyperclip.copy(data)
                copied_urls.add(data)
                webbrowser.open(data)
                print(f"[Copied to Clipboard] {data}")

        cv2.putText(frame, "Press 'q' to return", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow("Live QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow("Live QR Scanner")


# --------------------- QR Generator ---------------------

def generate_qr_code_ui():
    root = tk.Tk()
    root.withdraw()
    text = simpledialog.askstring("QR Generator", "Enter text or URL to generate QR:")
    if text:
        img = qrcode.make(text)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if save_path:
            img.save(save_path)
            print("QR Code saved to:", save_path)
            img = img.convert("RGB")  # Convert to RGB mode
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            cv2.imshow("Generated QR", img_cv)
            cv2.waitKey(0)
            cv2.destroyWindow("Generated QR")


def main_ui():
    while True:
        frame = np.zeros((300, 600, 3), dtype=np.uint8)
        draw_buttons(frame)
        cv2.putText(frame, "Press 'i' for Image or 'l' for Live Scan", (60, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.imshow("QR Code Scanner UI", frame)

        key = cv2.waitKey(0)
        if key == ord('i'):
            cv2.destroyWindow("QR Code Scanner UI")
            image_scan_mode()
        elif key == ord('l'):
            cv2.destroyWindow("QR Code Scanner UI")
            live_scan_mode()
        elif key == ord('g'):
            cv2.destroyWindow("QR Code Scanner UI")
            generate_qr_code_ui()
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main_ui()
