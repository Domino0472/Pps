import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import scipy.fftpack

def butter_lowpass(cutoff, fs, order=5):
    """
        Projektowanie filtru dolnoprzepustowego Butterwortha.
            Zgodnie z instrukcją: częstotliwość znormalizowana = cutoff / (fs/2).
                """
                    nyq = 0.5 * fs
                        normal_cutoff = cutoff / nyq
                            b, a = butter(order, normal_cutoff, btype='low', analog=False)
                                return b, a

                                def butter_lowpass_filter(data, cutoff, fs, order=5):
                                    """
                                        Zastosowanie filtru do danych (sygnału).
                                            """
                                                b, a = butter_lowpass(cutoff, fs, order=order)
                                                    y = lfilter(b, a, data)
                                                        return y

                                                        # --- 1. Konfiguracja parametrów ---
                                                        fs = 1000.0       # Częstotliwość próbkowania (Hz)
                                                        T = 1.0           # Czas trwania sygnału (s)
                                                        n = int(T * fs)   # Liczba próbek
                                                        t = np.linspace(0, T, n, endpoint=False) # Oś czasu

                                                        # Parametry filtru (do edycji w części analitycznej zadania)
                                                        cutoff_freq = 10.0  # Częstotliwość odcięcia w Hz (powyżej 5, poniżej 15)
                                                        filter_order = 5    # Rząd filtru

                                                        # --- 2. Generowanie sygnału (Zadanie pkt 1 i 2) ---
                                                        # [span_0](start_span)Składowe: 5 Hz, 15 Hz, 30 Hz[span_0](end_span)
                                                        f1, f2, f3 = 5.0, 15.0, 30.0
                                                        sig_raw = np.sin(2 * np.pi * f1 * t) + \
                                                                  np.sin(2 * np.pi * f2 * t) + \
                                                                            np.sin(2 * np.pi * f3 * t)

                                                                            # --- 3. Filtracja sygnału (Zadanie pkt 3) ---
                                                                            # Filtr dolnoprzepustowy: przepuszcza 5Hz, tłumi 15Hz i 30Hz
                                                                            sig_filtered = butter_lowpass_filter(sig_raw, cutoff_freq, fs, order=filter_order)

                                                                            # --- 4. Obliczenie FFT (Zadanie pkt 4) ---
                                                                            # Funkcja pomocnicza do obliczania jednostronnego widma
                                                                            def calculate_fft(signal, fs):
                                                                                N = len(signal)
                                                                                    yf = np.fft.fft(signal)
                                                                                        xf = np.fft.fftfreq(N, 1 / fs)
                                                                                            
                                                                                                # [span_1](start_span)Bierzemy tylko pierwszą połowę (widmo jednostronne)[span_1](end_span)
                                                                                                    half_n = N // 2
                                                                                                        return xf[:half_n], 2.0/N * np.abs(yf[:half_n])

                                                                                                        x_freq, y_fft_raw = calculate_fft(sig_raw, fs)
                                                                                                        _, y_fft_filt = calculate_fft(sig_filtered, fs)

                                                                                                        # --- 5. Wyświetlanie wyników (Zadanie pkt 5 i 6) ---

                                                                                                        # Wykres 1: Dziedzina czasu (Sygnały)
                                                                                                        plt.figure(figsize=(10, 6))
                                                                                                        plt.subplot(2, 1, 1)
                                                                                                        plt.plot(t, sig_raw, label='Sygnał oryginalny')
                                                                                                        plt.title('Sygnał w dziedzinie czasu (przed filtracją)')
                                                                                                        plt.xlabel('Czas [s]')
                                                                                                        plt.ylabel('Amplituda')
                                                                                                        plt.grid()

                                                                                                        plt.subplot(2, 1, 2)
                                                                                                        plt.plot(t, sig_filtered, label='Sygnał przefiltrowany', color='orange')
                                                                                                        plt.title(f'Sygnał po filtracji (Order={filter_order}, Cutoff={cutoff_freq}Hz)')
                                                                                                        plt.xlabel('Czas [s]')
                                                                                                        plt.ylabel('Amplituda')
                                                                                                        plt.grid()
                                                                                                        plt.tight_layout()

                                                                                                        # [span_2](start_span)Wykres 2: Dziedzina częstotliwości (FFT) - Układ zgodny z Rysunkiem 1[span_2](end_span)
                                                                                                        plt.figure(figsize=(10, 8))

                                                                                                        # Widmo przed filtracją
                                                                                                        plt.subplot(2, 1, 1)
                                                                                                        plt.plot(x_freq, y_fft_raw)
                                                                                                        plt.title('FFT of Raw Signal')
                                                                                                        plt.ylabel('Amplitude')
                                                                                                        plt.grid()
                                                                                                        plt.xlim(0, 60) # Ograniczenie osi X dla lepszej czytelności (składowe są do 30Hz)

                                                                                                        # Widmo po filtracji
                                                                                                        plt.subplot(2, 1, 2)
                                                                                                        plt.plot(x_freq, y_fft_filt)
                                                                                                        plt.title('FFT of Filtered Signal')
                                                                                                        plt.xlabel('Frequency (Hz)')
                                                                                                        plt.ylabel('Amplitude')
                                                                                                        plt.grid()
                                                                                                        plt.xlim(0, 60)

                                                                                                        plt.tight_layout()
                                                                                                        plt.show()
                                                                                                        