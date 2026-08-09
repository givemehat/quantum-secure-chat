import tkinter as tk
from tkinter import ttk, messagebox
import threading

from qkd import generate_quantum_key
from crypto import encrypt, decrypt

BG = "#1e1e1e"  # window background
CARD = "#2b2b2b"  # section card background
ENTRY_BG = "#1a1a1a"  # input background
BORDER = "#444444"  # border / separator


FG = "#eeeeee"  # primary text  (near white)
FG_DIM = "#aaaaaa"  # secondary / labels
FG_KEY = "#6fcf6f"  # key display (green)
FG_ENC = "#e0a040"  # encrypted text (amber)
FG_DEC = "#6fcf6f"  # decrypted text (green)


BLUE = "#4a90d9"
GREEN = "#5aad78"
AMBER = "#d4a030"
RED = "#c05050"

# Fonts
F = ("Arial", 10)
FB = ("Arial", 10, "bold")
FM = ("Courier New", 11)  # monospace for key/cipher
FS = ("Arial", 9)


def make_btn(parent, text, cmd, bg=BLUE, width=14):

    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=bg,
        fg="#111111",
        activebackground=bg,
        activeforeground="#111111",
        font=FB,
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        width=width,
        cursor="hand2",
        highlightthickness=0,
    )


def section_lbl(parent, text):

    tk.Label(
        parent,
        text=text,
        fg=FG_DIM,
        bg=BG,
        font=("Arial", 9, "bold"),
        anchor="w",
    ).pack(fill="x", padx=16, pady=(12, 3))


def card(parent):
    """A simple card-style frame."""
    f = tk.Frame(parent, bg=CARD, padx=14, pady=12)
    f.pack(fill="x", padx=14, pady=(0, 2))
    return f


class App:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.key = ""
        self._setup()
        self._ui()

    def _setup(self):
        self.root.title("Quantum Secure Chat")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        w, h = 580, 660
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        s = ttk.Style(self.root)
        s.theme_use("clam")
        s.configure(
            "Bar.Horizontal.TProgressbar",
            troughcolor=ENTRY_BG,
            background=BLUE,
            bordercolor=BORDER,
            thickness=10,
        )

    def _ui(self):

        hdr = tk.Frame(self.root, bg=CARD, pady=10)
        hdr.pack(fill="x")

        tk.Label(
            hdr,
            text="Quantum Secure Chat",
            fg=FG,
            bg=CARD,
            font=("Arial", 13, "bold"),
        ).pack(side="left", padx=16)

        tk.Label(
            hdr,
            text="BB84 + XOR",
            fg=FG_DIM,
            bg=CARD,
            font=FS,
        ).pack(side="right", padx=16)

        tk.Frame(self.root, height=1, bg=BORDER).pack(fill="x")

        # Quantum Key
        section_lbl(self.root, "QUANTUM KEY")
        kc = card(self.root)

        self.key_var = tk.StringVar(value="No key generated yet")
        tk.Label(
            kc,
            textvariable=self.key_var,
            fg=FG_KEY,
            bg=ENTRY_BG,
            font=FM,
            anchor="w",
            padx=10,
            pady=7,
            wraplength=510,
            justify="left",
        ).pack(fill="x")

        bar_row = tk.Frame(kc, bg=CARD)
        bar_row.pack(fill="x", pady=(8, 2))

        tk.Label(bar_row, text="Strength:", fg=FG_DIM, bg=CARD, font=FS).pack(
            side="left"
        )

        self.bar = ttk.Progressbar(
            bar_row,
            style="Bar.Horizontal.TProgressbar",
            orient="horizontal",
            length=330,
            maximum=100,
            value=0,
        )
        self.bar.pack(side="left", padx=(8, 0))

        self.bar_lbl = tk.Label(bar_row, text="—", fg=FG_DIM, bg=CARD, font=FS)
        self.bar_lbl.pack(side="left", padx=(10, 0))

        self.gen_btn = make_btn(kc, "Generate Key", self._gen_key, bg=BLUE, width=16)
        self.gen_btn.pack(anchor="w", pady=(10, 0))

        section_lbl(self.root, "MESSAGE")
        mc = card(self.root)

        self.msg = tk.Entry(
            mc,
            font=("Arial", 11),
            bg=ENTRY_BG,
            fg=FG,
            insertbackground=FG,
            selectbackground=BLUE,
            selectforeground=FG,
            relief="flat",
            bd=0,
        )
        self.msg.pack(fill="x", ipady=8, ipadx=4)

        tk.Frame(mc, height=1, bg=BORDER).pack(fill="x", pady=(2, 8))

        br = tk.Frame(mc, bg=CARD)
        br.pack(fill="x")

        make_btn(br, "Encrypt", self._encrypt, bg="#3a8a3a", width=12).pack(side="left")
        make_btn(br, "Decrypt", self._decrypt, bg="#3a6ab0", width=12).pack(
            side="left", padx=(8, 0)
        )
        make_btn(br, "Clear", self._clear, bg="#7a3a3a", width=8).pack(
            side="left", padx=(8, 0)
        )

        # Encrypted
        section_lbl(self.root, "ENCRYPTED")
        ec = card(self.root)

        self.enc = tk.Text(
            ec,
            height=3,
            font=FM,
            bg=ENTRY_BG,
            fg=FG_ENC,
            selectbackground=BLUE,
            relief="flat",
            bd=0,
            wrap="word",
        )
        self.enc.pack(fill="x", padx=2, pady=2)

        # Decrypted
        section_lbl(self.root, "DECRYPTED")
        dc = card(self.root)

        self.dec = tk.Text(
            dc,
            height=3,
            font=("Arial", 11),
            bg=ENTRY_BG,
            fg=FG_DEC,
            insertbackground=FG,
            selectbackground=BLUE,
            relief="flat",
            bd=0,
            wrap="word",
            state="disabled",
        )
        self.dec.pack(fill="x", padx=2, pady=2)

        tk.Frame(self.root, height=1, bg=BORDER).pack(fill="x", pady=(10, 0))
        sb = tk.Frame(self.root, bg=BG)
        sb.pack(fill="x")

        self.status_var = tk.StringVar(value="Ready? Generate a key to begin")
        self.status_lbl = tk.Label(
            sb,
            textvariable=self.status_var,
            fg=FG_DIM,
            bg=BG,
            font=FS,
            anchor="w",
        )
        self.status_lbl.pack(fill="x", padx=16, pady=5)

    def _status(self, text, color=FG_DIM):
        self.status_var.set(text)
        self.status_lbl.config(fg=color)

    def _set_bar(self, bits):
        pct = min(100, int(bits / 32 * 100))
        self.bar["value"] = pct
        s = ttk.Style()
        if pct < 35:
            col, label = RED, f"Weak ({bits} bits)"
        elif pct < 65:
            col, label = AMBER, f"Fair ({bits} bits)"
        else:
            col, label = GREEN, f"Strong ({bits} bits)"
        s.configure("Bar.Horizontal.TProgressbar", background=col)
        self.bar_lbl.config(text=label, fg=col)

    def _clear(self):
        self.msg.delete(0, tk.END)
        self.enc.delete("1.0", tk.END)
        self.dec.config(state="normal")
        self.dec.delete("1.0", tk.END)
        self.dec.config(state="disabled")
        self._status("Cleared")

    def _gen_key(self):
        self.gen_btn.config(state="disabled", text="Working…")
        self.key_var.set("Simulating quantum circuit…")
        self._status("Running BB84 simulation on AerSimulator…", BLUE)

        def _task():
            try:
                k = generate_quantum_key(32)
                self.key = k
                disp = " ".join(k[i : i + 4] for i in range(0, len(k), 4))
                self.root.after(0, lambda: self._on_key(disp, len(k)))
            except Exception as e:
                err = str(e)
                self.root.after(0, lambda: self._on_err(err))
            finally:
                self.root.after(
                    0, lambda: self.gen_btn.config(state="normal", text="Generate Key")
                )

        threading.Thread(target=_task, daemon=True).start()

    def _on_key(self, display, bits):
        self.key_var.set(display)
        self._set_bar(bits)
        self._status(f"Key ready  ·  {bits} sifted bits", GREEN)

    def _on_err(self, err):
        self.key_var.set("Error: key generation failed")
        self._status(f"Error: {err}", RED)
        messagebox.showerror("QKD Error", err)

    def _encrypt(self):
        if not self.key:
            messagebox.showerror("No Key", "Generate a key first.")
            return
        msg = self.msg.get()
        if not msg:
            messagebox.showwarning("Empty", "Enter a message to encrypt.")
            return
        ct = encrypt(msg, self.key)
        self.enc.delete("1.0", tk.END)
        self.enc.insert(tk.END, ct)
        self._status(f"Encrypted  ·  {len(msg)} → {len(ct)} chars", AMBER)

    def _decrypt(self):
        if not self.key:
            messagebox.showerror("No Key", "Generate a key first.")
            return
        ct = self.enc.get("1.0", tk.END).rstrip("\n")
        if not ct:
            messagebox.showwarning("Empty", "Nothing to decrypt.")
            return
        pt = decrypt(ct, self.key)
        self.dec.config(state="normal")
        self.dec.delete("1.0", tk.END)
        self.dec.insert(tk.END, pt)
        self.dec.config(state="disabled")
        original = self.msg.get()
        if original and pt == original:
            self._status("Decrypted  ·  ✓ Matches original message", GREEN)
        else:
            self._status(f"Decrypted  ·  {len(pt)} chars", FG_DIM)


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
