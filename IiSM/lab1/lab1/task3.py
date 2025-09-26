import tkinter as tk
import random


def generate_dependent_events(P_A, P_B_A, N: int = 10**6):
    P_B_A_neg = 1 - P_B_A
    indicators = []

    for _ in range(N):
        A = random.random() < P_A

        if A:
            B = random.random() < P_B_A
        else:
            B = random.random() < P_B_A_neg

        if A and B:
            indicators.append(3)
            # A_B_count += 1
        elif A and not B:
            indicators.append(2)
            # A_B_neg_count += 1
        elif not A and B:
            indicators.append(1)
            # A_neg_B_count += 1
        else:
            indicators.append(0)
            # A_neg_B_neg_count += 1

    freq_A_B = indicators.count(3) / N
    freq_A_B_neg = indicators.count(2) / N
    freq_A_neg_B = indicators.count(1) / N
    freq_A_neg_B_neg = indicators.count(0) / N

    return freq_A_B, freq_A_B_neg, freq_A_neg_B, freq_A_neg_B_neg


def on_run_button_click():
    P_A = slider_P_A.get()
    P_B_A = slider_P_B_A.get()

    P_A_neg = 1 - P_A
    P_B_neg_A = 1 - P_B_A

    freq_A_B, freq_A_B_neg, freq_A_neg_B, freq_A_neg_B_neg = generate_dependent_events(P_A, P_B_A)

    result_A_B_label.config(text=f'Event AB. Empirical probability: {freq_A_B}. Theoretical probability: {P_A * P_B_A}')
    result_A_B_neg_label.config(text=f'Event AB-. Empirical probability: {freq_A_B_neg}. Theoretical probability: {P_A * P_B_neg_A}')
    result_A_neg_B_label.config(text=f'Event A-B. Empirical probability: {freq_A_neg_B}. Theoretical probability: {P_A_neg * P_B_neg_A}')
    result_A_neg_B_neg_label.config(text=f'Event A-B-. Empirical probability: {freq_A_neg_B_neg}. Theoretical probability: {P_A_neg * P_B_A}')


root = tk.Tk()
root.title('Simulation of a complex event consisting of dependent events')

slider_P_A_label = tk.Label(root, text='Select the probability P(A) from 0 to 1')
slider_P_A_label.pack()

slider_P_A = tk.Scale(root, from_=0, to=1, orient='horizontal', resolution=0.01, length=300)
slider_P_A.set(0.7)
slider_P_A.pack()

slider_P_B_A_label = tk.Label(root, text='Select the probability P(B|A) from 0 to 1')
slider_P_B_A_label.pack()

slider_P_B_A = tk.Scale(root, from_=0, to=1, orient='horizontal', resolution=0.01, length=300)
slider_P_B_A.set(0.4)
slider_P_B_A.pack()

run_button = tk.Button(root, text='Run', command=on_run_button_click)
run_button.pack(pady=10)

result_A_B_label = tk.Label(root, text='Event AB. Empirical probability: --. Theoretical probability: --')
result_A_B_label.pack()

result_A_B_neg_label = tk.Label(root, text='Event AB-. Empirical probability: --. Theoretical probability: --')
result_A_B_neg_label.pack()

result_A_neg_B_label = tk.Label(root, text='Event A-B. Empirical probability: --. Theoretical probability: --')
result_A_neg_B_label.pack()

result_A_neg_B_neg_label = tk.Label(root, text='Event A-B-. Empirical probability: --. Theoretical probability: --')
result_A_neg_B_neg_label.pack()

root.mainloop()