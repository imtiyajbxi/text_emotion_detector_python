import tkinter as tk
from tkinter import END, LEFT, E, W, N, S, Scrollbar, Text
from textblob import TextBlob

# --- UI Color Palette (Dark Blue Gradient Vibe) ---
BG_COLOR = "#0A1931"      # Deep Dark Navy Blue (Main Background)
FRAME_COLOR = "#182F51"   # Slightly Lighter Blue-Gray (Card Background)
ACCENT_COLOR = "#50C2FF"  # Bright Sky Blue/Cyan Accent
TEXT_COLOR = "#EAEAEA"    # Light Gray for main text
BUTTON_COLOR = "#007ACC"  # Classic Blue for button base
BUTTON_HOVER = "#50C2FF"  # Bright Blue for hover
NEGATIVE_COLOR = "#FF6B6B" # Red for ANGRY/SAD emotion
POSITIVE_COLOR = "#14D09C" # Green for HAPPY/JOYFUL emotion
NEUTRAL_COLOR = "#FFD700"  # Gold for neutral emotion

# --- Emotion Labels ---
HAPPY_LABEL = "😀 HAPPY"
ANGRY_LABEL = "😠 ANGRY"
NEUTRAL_LABEL = "😐 NEUTRAL"
VERY_POSITIVE_MOOD = "😄 Very Joyful"
NEGATIVE_MOOD = "😔 Mostly Negative"
NEUTRAL_MOOD = "🧐 Neutral/Mixed"

# --- Font Configuration ---
TITLE_FONT = ("Helvetica", 24, "bold")
BODY_FONT = ("Arial", 12)
RESULT_FONT = ("Courier New", 12)

# ---------------- Function to analyze emotion ----------------
def analyze_emotion():
    """Analyzes the sentiment of the text input using TextBlob and updates the UI."""
    text = text_entry.get("1.0", END).strip()
    
    # Reset result display
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", END)
    
    if not text:
        result_text.insert(END, f"⚠️ Please enter some text to analyze!", ("warning", NEUTRAL_COLOR))
        result_text.config(state=tk.DISABLED)
        return

    sentences = [s.strip() for s in text.split('.') if s.strip()]
    total_sentiment = 0
    
    # Sentence-by-Sentence Analysis and Display
    for s in sentences:
        blob = TextBlob(s)
        sentiment = blob.sentiment.polarity
        total_sentiment += sentiment
        
        # Determine classification and color (based on TextBlob polarity)
        if sentiment > 0.15:
            tag = "positive"
            color = POSITIVE_COLOR
            prefix = f"{HAPPY_LABEL}: "
        elif sentiment < -0.15:
            tag = "negative"
            color = NEGATIVE_COLOR
            prefix = f"{ANGRY_LABEL}: "
        else:
            tag = "neutral"
            color = NEUTRAL_COLOR
            prefix = f"{NEUTRAL_LABEL}: "

        # Insert text with specific color tags
        result_text.insert(END, prefix, "tag_prefix")
        result_text.insert(END, f"{s}.\n", (tag, color))
    
    # Calculate Overall Emotion Summary
    avg_sentiment = total_sentiment / len(sentences) if sentences else 0
    
    if avg_sentiment > 0.15:
        overall_text = f"Overall Emotion: {VERY_POSITIVE_MOOD}"
        overall_color = POSITIVE_COLOR
    elif avg_sentiment < -0.15:
        overall_text = f"Overall Emotion: {NEGATIVE_MOOD}"
        overall_color = NEGATIVE_COLOR
    else:
        overall_text = f"Overall Emotion: {NEUTRAL_MOOD}"
        overall_color = NEUTRAL_COLOR

    # Display Overall Emotion Summary at the top
    result_text.insert("1.0", f"--- EMOTION ANALYSIS SUMMARY ---\n{overall_text}\n\n", ("summary", overall_color))
    
    result_text.config(state=tk.DISABLED)

# ---------------- Canvas Button Implementation ----------------
# NOTE: Modified to support both pack() and grid() to avoid the TclError.
class RoundButton:
    def __init__(self, master, text, command, width, height, radius, fill, active_fill, text_color):
        self.master = master
        self.command = command
        self.text_color = text_color
        self.fill = fill
        self.active_fill = active_fill
        self.width = width
        self.height = height
        self.radius = radius
        
        # Create Canvas widget
        self.canvas = tk.Canvas(master, width=width, height=height, bg=master['bg'], highlightthickness=0)
        
        # Draw the rounded rectangle and get the rect item ID
        self.rect = self._draw_rounded_rectangle(0, 0, width, height, radius, fill)
        
        # Add Text
        self.button_text = self.canvas.create_text(width/2, height/2, text=text, font=("Arial", 14, "bold"), fill=text_color)
        
        # Bind events
        self.canvas.tag_bind(self.rect, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.button_text, "<Button-1>", self.on_click)
        self.canvas.tag_bind(self.rect, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.rect, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.button_text, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.button_text, "<Leave>", self.on_leave)
    
    def _draw_rounded_rectangle(self, x1, y1, x2, y2, radius, fill):
        """Helper to draw a simple rounded rectangle on the canvas."""
        # Clear previous drawings to avoid artifacts during redraw (for hover)
        self.canvas.delete("all_shapes") 
        
        # Draw main rectangle and corner ovals approximation
        self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=fill, outline=fill, tags="all_shapes")
        self.canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=fill, outline=fill, tags="all_shapes")
        self.canvas.create_oval(x1, y1, x1 + 2*radius, y1 + 2*radius, fill=fill, outline=fill, tags="all_shapes")
        self.canvas.create_oval(x2 - 2*radius, y1, x2, y1 + 2*radius, fill=fill, outline=fill, tags="all_shapes")
        self.canvas.create_oval(x1, y2 - 2*radius, x1 + 2*radius, y2, fill=fill, outline=fill, tags="all_shapes")
        self.canvas.create_oval(x2 - 2*radius, y2 - 2*radius, x2, y2, fill=fill, outline=fill, tags="all_shapes")
        
        # Re-create and return the main rect item for primary binding
        return self.canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=fill, outline=fill)

    def on_click(self, event):
        self.command()

    def on_enter(self, event):
        # Redraw shapes with active fill color
        self._draw_rounded_rectangle(0, 0, self.width, self.height, self.radius, self.active_fill)
        # Ensure text is on top
        self.canvas.tag_raise(self.button_text)

    def on_leave(self, event):
        # Redraw shapes with normal fill color
        self._draw_rounded_rectangle(0, 0, self.width, self.height, self.radius, self.fill)
        # Ensure text is on top
        self.canvas.tag_raise(self.button_text)
        
    def pack(self, **kwargs):
        """Allows button to be placed using pack() manager."""
        self.canvas.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Allows button to be placed using grid() manager (FIXED ERROR)."""
        self.canvas.grid(**kwargs)


# ---------------- Main Window Setup ----------------
root = tk.Tk()
root.title("Text Emotion Analyzer | Advanced Blue UI")
root.geometry("800x750")
root.config(bg=BG_COLOR)
root.minsize(700, 650) 

# Configure grid to be responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Main Container Frame (Padded and styled like a card)
main_frame = tk.Frame(root, bg=BG_COLOR, padx=40, pady=30)
main_frame.grid(row=0, column=0, sticky=N+S+E+W)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure(4, weight=1) # Allow result area to expand

# --- 1. Title ---
tk.Label(main_frame, text="🧠 Advanced Text Emotion Analysis", 
         font=TITLE_FONT, bg=BG_COLOR, fg=ACCENT_COLOR).grid(row=0, column=0, pady=(10, 20), sticky=W+E)

# --- 2. Instruction Label ---
tk.Label(main_frame, text="Enter the English text below:", 
         font=BODY_FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, sticky=W, pady=(5, 5))

# --- 3. Text Entry Area (with Scrollbar, Dark Card Style) ---
input_card = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="flat", highlightbackground=ACCENT_COLOR, highlightthickness=1)
input_card.grid(row=2, column=0, pady=(0, 20), sticky=W+E)
input_card.grid_columnconfigure(0, weight=1)

text_entry = Text(input_card, height=10, width=70, font=BODY_FONT, 
                     bg=FRAME_COLOR, fg=TEXT_COLOR, bd=0, relief="flat", padx=15, pady=15, insertbackground=ACCENT_COLOR)
text_entry.grid(row=0, column=0, sticky=N+S+E+W)
# Scrollbar
scrollbar = Scrollbar(input_card, command=text_entry.yview, bg=FRAME_COLOR, troughcolor=BG_COLOR)
scrollbar.grid(row=0, column=1, sticky='ns')
text_entry['yscrollcommand'] = scrollbar.set

# --- 4. Analyze Button (Rounded Canvas Button - NOW USING GRID) ---
analyze_button_wrapper = RoundButton(
    main_frame, 
    text="ANALYZE EMOTION", 
    command=analyze_emotion, 
    width=250, 
    height=55, 
    radius=25, 
    fill=BUTTON_COLOR, 
    active_fill=BUTTON_HOVER, 
    text_color=TEXT_COLOR
)
# Fixed the error by using grid() instead of pack()
analyze_button_wrapper.grid(row=3, column=0, pady=25) 

# --- 5. Result Display Area (Text widget for colored output) ---
result_card = tk.Frame(main_frame, bg=FRAME_COLOR, bd=2, relief="flat", highlightbackground=NEUTRAL_COLOR, highlightthickness=1)
result_card.grid(row=4, column=0, pady=(10, 10), sticky=W+E+N+S)
result_card.grid_columnconfigure(0, weight=1)
result_card.grid_rowconfigure(0, weight=1)

# Use Text widget for results to allow for colored highlighting
result_text = Text(result_card, font=RESULT_FONT, bg=FRAME_COLOR, fg=TEXT_COLOR, 
                    bd=0, relief="flat", padx=15, pady=15, wrap=tk.WORD, state=tk.DISABLED)
result_text.grid(row=0, column=0, sticky=W+E+N+S)

# Tag configurations for colored output
result_text.tag_config("summary", foreground=ACCENT_COLOR, font=("Helvetica", 12, "bold"))
result_text.tag_config("tag_prefix", foreground=TEXT_COLOR, font=("Courier New", 12, "bold"))
result_text.tag_config("positive", foreground=POSITIVE_COLOR)
result_text.tag_config("negative", foreground=NEGATIVE_COLOR)
result_text.tag_config("neutral", foreground=NEUTRAL_COLOR)
result_text.tag_config("warning", foreground=NEUTRAL_COLOR, font=("Arial", 12, "italic"))

# --- 6. Footer ---
footer_label = tk.Label(root, text="Developed by Imtiyaj Bin Islam", 
                        bg=BG_COLOR, fg="#444444", font=("Arial", 10, "italic"))
# Placed footer outside the main grid for simplicity
footer_label.grid(row=1, column=0, sticky=W+E) 

root.mainloop()