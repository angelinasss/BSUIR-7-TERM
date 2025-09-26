import random
import tkinter as tk

def generate_events(probabilities, N: int = 10 ** 6):
    k = len(probabilities)
    events = []
    
    for _ in range(N):
        trial_result = [
            random.random() < p
            for p in probabilities
        ]
        events.append(trial_result)
    
    return events

def calculate_frequencies(events, k):
    frequencies = [0] * k
    total_trials = len(events)
    
    for trial in events:
        for i in range(k):
            if trial[i]:
                frequencies[i] += 1
    
    return [freq / total_trials for freq in frequencies]

def on_run_button_click():
    try:
        input_text = probabilities_entry.get().strip()
        probabilities = list(map(float, input_text.split(',')))
        k = len(probabilities)

        if not all(0 <= p <= 1 for p in probabilities):
            result_label.config(text='Error! All probabilities must be between 0 and 1')
            return
        
        if k == 0:
            result_label.config(text='Error! Please enter at least one probability')
            return

        # Event generation
        events = generate_events(probabilities)
        # Calculation of empirical probabilities
        frequencies = calculate_frequencies(events, k)
        
        result_text = f"Simulation of {k} independent events:\n\n"
        for i, (theory, practice) in enumerate(zip(probabilities, frequencies), 1):
            difference = abs(theory - practice)
            result_text += (f"Event {i}:\ntheoretical probability = {theory:.4f}, "
                          f"empirical probability = {practice:.4f}, "
                          f"deviation = {difference:.4f}\n")
        
        result_label.config(text=result_text)

    except ValueError:
        result_label.config(text='Error! Please enter valid numbers separated by commas')

root = tk.Tk()
root.title('Simulation of a complex event')
root.geometry('550x350')

title_label = tk.Label(root, text='Simulation of k independent random events', 
                      font=('Arial', 14, 'bold'))
title_label.pack()

description_label = tk.Label(root, 
                           text='Enter the probabilities of k independent events separated by commas',
                           font=('Arial', 10))
description_label.pack()

probabilities_entry = tk.Entry(root, width=50, font=('Arial', 10))
probabilities_entry.pack(pady=10)

run_button = tk.Button(root, text='Run', 
                      command=on_run_button_click, 
                      bg='lightblue', 
                      font=('Arial', 10, 'bold'))
run_button.pack(pady=10)

result_label = tk.Label(root, text='The results will appear here', 
                       font=('Arial', 10), 
                       justify='left',
                       bg='lightyellow',
                       wraplength=500)
result_label.pack(pady=10, fill='both', expand=True)

root.mainloop()