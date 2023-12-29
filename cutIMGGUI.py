import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def carica_immagine():
    # Permette all'utente di selezionare un'immagine e la visualizza
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Ridimensiona l'immagine per la visualizzazione
        img = ImageTk.PhotoImage(img)
        panel.configure(image=img)
        panel.image = img
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

def taglia_immagine():
    # Recupera il percorso del file e i parametri dall'interfaccia utente
    file_path = entry_path.get()
    righe = int(entry_righe.get())
    colonne = int(entry_colonne.get())
    overlap = float(entry_overlap.get())
    argument={"file":file_path, "r":righe,"c":colonne, "oh":overlap,"ow":overlap}

    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Errore", "Seleziona un file immagine valido.")
        return
    
    try:
        taglia_immagine_con_overlap(argument)
        messagebox.showinfo("Completato", "L'immagine è stata tagliata con successo.")
    except Exception as e:
        messagebox.showerror("Errore", str(e))

def taglia_immagine_con_overlap(argument):
    # Carica l'immagine
    try:
        img = Image.open(argument["file"])

        # Calcola la larghezza e l'altezza di ogni cella della griglia
        width, height = img.size
        cell_width = width // int(argument["c"])
        cell_height = height // int(argument["r"])

        # Calcola l'overlap in pixel
        overlap_width = int(cell_width * float(argument["ow"]))
        overlap_height = int(cell_height * float(argument["oh"]))

        # Lista per salvare i percorsi dei pezzi tagliati
        grid_images_paths = []

        # Taglia l'immagine in una griglia con sovrapposizione
        for i in range(int(argument["r"])):
            for j in range(int(argument["c"])):
                # Calcola le coordinate del pezzo da tagliare considerando l'overlap
                left = max(j * cell_width, 0)
                right = min((j + 1) * cell_width + overlap_width, width)
                top = max(i * cell_height, 0)
                bottom = min((i + 1) * cell_height + overlap_height, height)
                
                # Taglia l'immagine
                grid_img = img.crop((left, top, right, bottom))
                
                # Salva il pezzo tagliato
                grid = grid_img.resize((1123,794))
                # Salvo il pezzo tagliato
                grid_path = f'./grid_{i+1}{j+1}.jpg'
                grid.save(grid_path, dpi=(300,300))
                grid_images_paths.append(grid_path)
        return grid_images_paths
    except FileNotFoundError:
        print("File non trovato")
    except Exception as e:
        # Questo blocco cattura altre possibili eccezioni
        print(f"Si è verificato un errore: {e}")

# Crea la finestra principale
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Taglia Immagine")

    # Crea e posiziona i widget
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    button_carica = tk.Button(frame, text="Carica Immagine", command=carica_immagine)
    button_carica.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    entry_path = tk.Entry(frame, width=50)
    entry_path.grid(row=0, column=1, padx=5, pady=5)

    label_righe = tk.Label(frame, text="Righe:")
    label_righe.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    entry_righe = tk.Entry(frame, width=10)
    entry_righe.grid(row=1, column=1, sticky="w", padx=5)

    label_colonne = tk.Label(frame, text="Colonne:")
    label_colonne.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    entry_colonne = tk.Entry(frame, width=10)
    entry_colonne.grid(row=2, column=1, sticky="w", padx=5)

    label_overlap = tk.Label(frame, text="Sovrapposizione (%):")
    label_overlap.grid(row=3, column=0, sticky="w", padx=5, pady=5)

    entry_overlap = tk.Entry(frame, width=10)
    entry_overlap.grid(row=3, column=1, sticky="w", padx=5)

    button_taglia = tk.Button(frame, text="Taglia Immagine", command=taglia_immagine)
    button_taglia.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    panel = tk.Label(frame)
    panel.grid(row=5, column=0, columnspan=2, sticky="ew")

    root.mainloop()
