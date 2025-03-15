import customtkinter as ctk
import qrcode
import qrcode.constants
import validators


# Code to produce QR Codes for given links. The Code will only accept valid links

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("700x300")
root.resizable(width=False, height=False)

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="QR Code Generator")
title.pack(pady=12, padx=10)

inputwindowLink = ctk.CTkEntry(
    master=frame, placeholder_text="Enter your Link", width=350, justify="center"
)
inputwindowLink.pack(pady=12, padx=10)

inputwindowName = ctk.CTkEntry(
    master=frame,
    placeholder_text="Enter your filename",
    width=350,
    justify="center",
)
inputwindowName.pack(pady=12, padx=10)


# Generate the qr code as a file with the qecode library, also checks if the given link is valid and formats the filename
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


# Fetches the link and the filename once the button is clicked
def startGenerate() -> None:
    link = inputwindowLink.get().strip()
    filename = inputwindowName.get().strip()
    generate_qr_code(link, filename)


# Checks if the URL is valid using the validators library
def isValidUrl(link: str) -> bool:
    return validators.url(link)


generateButton = ctk.CTkButton(
    master=frame,
    text="Generate QR-Code",
    command=startGenerate,
    width=50,
)
generateButton.pack(pady=12, padx=10)

notificationLabel = ctk.CTkLabel(master=frame, text="", width=100)
notificationLabel.pack(pady=12, padx=10)

root.mainloop()
