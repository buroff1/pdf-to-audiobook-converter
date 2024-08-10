import customtkinter as ctk  # Importing customtkinter for the custom GUI elements
from tkinter import filedialog, messagebox  # Importing filedialog and messagebox from tkinter
from gtts import gTTS  # Importing gTTS for text-to-speech conversion
import pdfplumber  # Importing pdfplumber for extracting text from PDF files
import os  # Importing os for file operations
import tempfile  # Importing tempfile for creating temporary files
import pygame  # Importing pygame for playing audio files


class PDFReaderApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("PDF to MP3 Audiobook Converter")  # Setting the window title

        # Center the application window on the screen
        self.center_window(800, 600)

        # Set appearance mode and default color theme for customtkinter
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

        # Create a text area for displaying PDF text
        self.text_area = ctk.CTkTextbox(root, wrap="word", font=("Helvetica", 18))
        self.text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        # Create an upload button for selecting PDF files
        self.upload_button = ctk.CTkButton(root, text="Upload PDF", command=self.upload_pdf, width=150, height=40)
        self.upload_button.pack(side="left", padx=10, pady=10)

        # Create a listen button for playing the converted text
        self.listen_button = ctk.CTkButton(root, text="Listen", command=self.listen_text, state="disabled", width=150,
                                           height=40)
        self.listen_button.pack(side="left", padx=10, pady=10)

        # Create a download button for saving the MP3 file
        self.download_button = ctk.CTkButton(root, text="Download MP3", command=self.download_mp3, state="disabled",
                                             width=150, height=40)
        self.download_button.pack(side="left", padx=10, pady=10)

        # Create an exit button for closing the application
        self.exit_button = ctk.CTkButton(root, text="Exit", command=root.quit, width=150, height=40)
        self.exit_button.pack(side="right", padx=10, pady=10)

        # Initialize variables for storing extracted PDF text and temporary audio file path
        self.pdf_text = ""
        self.temp_audio_file = None

    def center_window(self, width, height):
        # Calculate and set the position to center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def upload_pdf(self):
        # Open a file dialog to select a PDF file and extract its text
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.extract_text(file_path)  # Extract text from the selected PDF file
            self.text_area.delete("1.0", "end")  # Clear the text area
            self.text_area.insert("end", self.pdf_text)  # Insert the extracted text into the text area
            self.listen_button.configure(state="normal")  # Enable the listen button
            self.download_button.configure(state="normal")  # Enable the download button

    def extract_text(self, file_path):
        # Extract text from the PDF file using pdfplumber
        self.pdf_text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                self.pdf_text += page.extract_text()

    def listen_text(self):
        # Convert the extracted text to speech and play it
        if self.pdf_text:
            tts = gTTS(text=self.pdf_text, lang='en')  # Convert text to speech using gTTS
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                tts.save(temp_file.name)  # Save the speech to a temporary file
                self.temp_audio_file = temp_file.name  # Store the path to the temporary audio file
            pygame.mixer.init()  # Initialize the pygame mixer
            pygame.mixer.music.load(self.temp_audio_file)  # Load the audio file into the mixer
            pygame.mixer.music.play()  # Play the audio

    def download_mp3(self):
        # Convert the extracted text to speech and save it as an MP3 file
        if self.pdf_text:
            tts = gTTS(text=self.pdf_text, lang='en')  # Convert text to speech using gTTS
            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if save_path:
                tts.save(save_path)  # Save the speech to the selected file path
                messagebox.showinfo("Success", "MP3 file has been saved successfully!")  # Show success message

    def on_closing(self):
        # Remove the temporary audio file (if exists) and close the application
        if self.temp_audio_file and os.path.exists(self.temp_audio_file):
            os.remove(self.temp_audio_file)  # Delete the temporary audio file
        self.root.destroy()  # Close the application window


if __name__ == "__main__":
    # Create and run the main application window
    root = ctk.CTk()  # Initialize the customtkinter root window
    root.iconbitmap("audiobook.ico")  # Set the window icon
    app = PDFReaderApp(root)  # Create an instance of the PDFReaderApp class
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Set the protocol for handling window close event
    root.mainloop()  # Start the main event loop
