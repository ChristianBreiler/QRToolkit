import customtkinter as ctk
from tkinter import filedialog
import qrcode
import qrcode.constants
import validators
import os
from pyzbar.pyzbar import decode
from PIL import Image
import webbrowser

# Code to produce QR Codes for given links or decode QR Codes from png images and then open them automatically.
# The Code will only accept valid links

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("450x500")
root.resizable(width=False, height=False)
root.title("QRToolkit")

# convert to QR code when pressing enter
root.bind("<Return>", lambda event: startGenerate())

# Set a gradient background color (light to dark)
root.configure(bg="#1f1f1f")

# Frame for the widgets
frame = ctk.CTkFrame(master=root, corner_radius=15, fg_color="#282828")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
title = ctk.CTkLabel(
    master=frame,
    text="QRToolkit",
    font=("Arial", 24, "bold"),
    text_color="#FFCC70",
)
title.grid(row=0, column=0, columnspan=2, pady=20, padx=10)

# Link Input
inputwindowLink = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter your Link",
    width=350,
    height=40,
    justify="center",
    corner_radius=12,
)
inputwindowLink.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Filename Input
inputwindowName = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter your Filename",
    width=350,
    height=40,
    justify="center",
    corner_radius=12,
)
inputwindowName.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Notification Label for error or success messages
notificationLabel = ctk.CTkLabel(
    master=frame, text="", width=400, height=30, font=("Arial", 12), text_color="white"
)
notificationLabel.grid(row=3, column=0, columnspan=2, pady=10)

# Image for buttons
generateImage = Image.open("img/qr.png")
scanImg = Image.open("img/scan.png")

# Button to generate QR code
generateButton = ctk.CTkButton(
    master=frame,
    text="Generate QR-Code",
    corner_radius=12,
    fg_color="#4158D0",
    hover_color="#1E2A57",
    border_color="#FFCC70",
    border_width=2,
    image=ctk.CTkImage(dark_image=generateImage, light_image=generateImage),
    command=lambda: startGenerate(),
    width=250,
    height=50,
    font=("Arial", 14, "bold"),
)
generateButton.grid(row=4, column=0, padx=10, pady=20, sticky="ew")

# Button to import and decode a QR code from file by opening file explorer
importFileButton = ctk.CTkButton(
    master=frame,
    text="Import a QR Code (as PNG)",
    corner_radius=12,
    fg_color="#FF7F50",
    hover_color="#F75C00",
    border_color="#FFCC70",
    border_width=2,
    image=ctk.CTkImage(dark_image=scanImg, light_image=scanImg),
    command=lambda: importQRCodePic(),
    width=250,
    height=50,
    font=("Arial", 14, "bold"),
)
importFileButton.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

# configure the grid of the frame
frame.grid_columnconfigure(0, weight=1)

frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=0)
frame.grid_rowconfigure(4, weight=0)
frame.grid_rowconfigure(5, weight=0)


# Generate QR Code from given link and name the file after the given filename
def generate_qr_code(link: str, filename: str) -> None:
    try:
        if not link:
            notificationLabel.configure(
                text="Error: Link is required!", text_color="red"
            )
            return

        if not filename:
            notificationLabel.configure(
                text="Error: Filename is required!", text_color="red"
            )
            return

        if not isValidUrl(link):
            notificationLabel.configure(text="Error: Invalid URL!", text_color="red")
            return

        if not filename.endswith(".png"):
            filename += ".png"

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)

        notificationLabel.configure(
            text="QR Code saved as " + filename, text_color="green"
        )

    except Exception as e:
        notificationLabel.configure(text=f"Error: {e}", text_color="red")


# Start QR Code Generation
def startGenerate() -> None:
    link = inputwindowLink.get().strip()
    filename = inputwindowName.get().strip()
    generate_qr_code(link, filename)


# Check if URL is valid using validators
def isValidUrl(link: str) -> bool:
    return validators.url(link)


# Import and decode a QR Code
def importQRCodePic() -> None:

    filepath = filedialog.askopenfilename()

    if filepath == "":
        return
    
    if not isPNG(filepath):
        notificationLabel.configure(text="The file must be a PNG", text_color="red")
        return

    decoded_data = decode(Image.open(filepath))

    if not decoded_data:
        notificationLabel.configure(text="No QR Code found!", text_color="red")
        return

    url = decoded_data[0].data.decode("utf-8")

    if not isValidUrl(url):
        notificationLabel.configure(text="The link is invalid", text_color="red")
        return

    webbrowser.open(url, new=0, autoraise=True)
    notificationLabel.configure(text="QR Code opened successfully!", text_color="green")


# Check if file is PNG from its ending
def isPNG(filepath) -> bool:
    filename = os.path.basename(filepath)
    return filename.endswith(".png")


root.mainloop()
