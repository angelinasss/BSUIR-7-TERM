import tkinter as tk
import random

BG_COLOR = "#f0f0f0"
ACCENT_COLOR = "#4CAF50"
TEXT_COLOR = "#333333"
ENTRY_BG = "#ffffff"

def get_event_freq(events, N: int = 10**6):
    return sum(events) / N


def generate_simple_events(probability: float, N: int = 10**6):
    events = [random.random() < probability for _ in range(N)]
    frequency = get_event_freq(events)

    return frequency


def on_run_button_click():
    probability = slider.get()
    theoretical_value = probability
    frequency = generate_simple_events(probability)

    result_label.config(text=f'Event frequency: {frequency:.6f}',
        foreground=ACCENT_COLOR if abs(frequency - theoretical_value) < 0.01 else "#FF6B6B")
    theoretical_label.config(text=f'Theoretical value of event frequency: {theoretical_value:.6f}')

    difference = abs(frequency - theoretical_value)
    accuracy_label.config(text=f'Deviation: {difference:.6f}')


root = tk.Tk()
root.title('Simple random event generator')
root.configure(bg=BG_COLOR)
root.resizable(True, True)
root.minsize(400, 200)

slider_label = tk.Label(root, text='Select the probability of an event from 0 to 1')
slider_label.pack()

slider = tk.Scale(root, from_=0, to=1, orient='horizontal', resolution=0.01, length=300)
slider.set(0.75)
slider.pack()

run_button = tk.Button(root, text='Run', command=on_run_button_click)
run_button.pack(pady=10)

result_label = tk.Label(root, text='Event frequency: --')
result_label.pack()

theoretical_label = tk.Label(root, text='Theoretical value of event frequency: --')
theoretical_label.pack()

accuracy_label = tk.Label(root, text='Deviation: --')
accuracy_label.pack()

root.mainloop()