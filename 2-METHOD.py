import matplotlib.pyplot as plt
import scipy.io.wavfile as scp
import numpy as np
import math
import os
import sys
import importlib
import time
import tracemalloc
from sympy import nextprime
import random

main = importlib.import_module("1-MAIN")

def get_params():

    if len(sys.argv) > 1:
        isEmbedding = int(sys.argv[1])
        if isEmbedding == 1:                    #proses embedding
            isSingleEmbed = int(sys.argv[2])
            if isSingleEmbed == 1:
                audio = int(sys.argv[3])
                payload = int(sys.argv[4])
            elif isSingleEmbed == 2:
                total_audio = int(sys.argv[3])
                total_payload = int(sys.argv[4])
            else:
                print("Jenis embedding tidak valid")
                exit()
        elif isEmbedding == 2:                  #proses ekstraksi
            isSingleExtract = int(sys.argv[2])
            if isSingleExtract == 1:
                audio = int(sys.argv[3])
                payload = int(sys.argv[4])
            elif isSingleExtract == 2:
                total_audio = int(sys.argv[3])
                total_payload = int(sys.argv[4])
            else:
                print("Jenis ekstraksi tidak valid")
                exit()
        else:
            print("Jenis embedding tidak valid")
            exit()

        nilai_n = int(sys.argv[5]) 
        nilai_k = int(sys.argv[6])
        if nilai_n < nilai_k:
            print("Nilai n harus lebih besar atau sama dengan nilai k")
            exit()

    else:
        isEmbedding = int(input("Pilih proses\n1. Proses Embedding\n2. Proses Ekstraksi\nPilih: "))
        if isEmbedding == 1:
            print("=============================== PROSES EMBEDDING ===============================")
            isSingleEmbed = int(input("Pilih jenis embedding\n1. Single embedding\n2. Multi embedding\nPilih: "))
            if isSingleEmbed == 1:
                print("=============================== SINGLE EMBEDDING ===============================")
                audio, payload = map(int, input("Masukkan nomor audio dan payload: ").split())
            elif isSingleEmbed == 2:
                print("=============================== MULTI EMBEDDING ===============================")
                total_audio, total_payload = map(int, input("Masukkan total audio dan payload: ").split())
            else:
                print("Jenis embedding tidak valid")
                exit()
        elif isEmbedding == 2:
            print("=============================== PROSES EKSTRAKSI ===============================")
            isSingleExtract = int(input("Pilih jenis ekstraksi\n1. Single ekstraksi\n2. Multi ekstraksi\nPilih: "))
            if isSingleExtract == 1:
                print("=============================== SINGLE EKSTRAKSI ===============================")
                audio, payload = map(int, input("Masukkan nomor audio dan payload: ").split())
            elif isSingleExtract == 2:
                print("=============================== MULTI EKSTRAKSI ===============================")
                total_audio, total_payload = map(int, input("Masukkan total audio dan payload: ").split())
            else:
                print("Jenis ekstraksi tidak valid")
                exit()
        else:
            print("Jenis proses tidak valid")
            exit()
        print("\n=============================== PARAMETER SECRET SHARING ===============================")
        nilai_n, nilai_k = map(int, input("Masukkan nilai n dan k untuk Secret Sharing: ").split())
        if nilai_n < nilai_k:
            print("Nilai n harus lebih besar atau sama dengan nilai k")
            exit()
    
    if isEmbedding == 1:
        if isSingleEmbed == 1:
            pre_embed(audio, payload, nilai_n, nilai_k)
        elif isSingleEmbed == 2:
            multi_embed(total_audio, total_payload, nilai_n, nilai_k)
    elif isEmbedding == 2:
        if isSingleExtract == 1:
            pre_extract(audio, payload)
        elif isSingleExtract == 2:
            multi_extract(total_audio, total_payload)

def start_time():
    start = time.time()
    tracemalloc.start()

def end_time():
    end = time.time()
    tracemalloc.stop()

def multi_embed(total_audio, total_payload, nilai_n, nilai_k):
    for i in range(1, total_audio+1):
        for j in range(1, total_payload+1):
            results = pre_embed(i, j, nilai_n, nilai_k)
            if not results:
                return

def pre_embed(audio, payload, nilai_n, nilai_k):
    file_payload, file_audio, file_stego_audio = init_embedding_file(audio, payload)
    results = main.start_embed(file_payload, file_audio, file_stego_audio, nilai_n, nilai_k)
    if results :
        print("Embedding Audio " + str(audio) + ", Payload " + str(payload)+ " sukses")
    else:
        print("Embedding Audio " + str(audio) + ", Payload " + str(payload)+ " gagal")
    return results

def init_stego_audio(audio, payload):
    file_stego_audio = 'embeddingResults/stego_audio' + str(audio) + '_payload'+ str(payload) +'.wav'
    return file_stego_audio

def init_extracting_file(audio, payload):
    file_payload = 'extractingResults/stego_audio'+str(audio)+'_payload'+str(payload)+'/payload.txt'
    file_audio = 'extractingResults/stego_audio'+str(audio)+'_payload'+str(payload)+'/audio.wav'
    file_stego_audio = init_stego_audio(audio, payload)
    return file_payload, file_audio, file_stego_audio

def init_embedding_file(audio, payload):
    file_payload = 'stegoaudioDataset/Payload/payload'+ str(payload) +'.txt'
    file_audio = 'stegoaudioDataset/Audio/data' + str(audio) +'_mono.wav'
    file_stego_audio = init_stego_audio(audio, payload) #path untuk menyimpan stego audio hasil embedding
    return file_payload, file_audio, file_stego_audio
    
def sampling_audio(file_audio):
    rate, data = scp.read(file_audio)
    data = np.add(np.int16(data),[32768])
    return rate, data

def read_payload(file_payload):
    is_binary = is_binary_file(file_payload)

    content = list(open(file_payload))[0]

    if is_binary:
        binary_data = content.split('\t')
        binary_data = [x.strip('ÿþ') for x in binary_data]

        binary_data = [x.strip('\x00') for x in binary_data]
        binary_data = ''.join(binary_data)
    else:
        binary_data = string_to_binary(content)
    return binary_data
    
def string_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def is_binary_file(filepath):
    with open(filepath, 'rb') as f:
        chunk = f.read(1024)
        # Jika banyak karakter non-printable, anggap biner
        textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)))
        if not chunk:
            return False
        non_text = sum(1 for byte in chunk if byte not in textchars)
        return non_text > len(chunk) / 4

def get_avg_difference(sample):
    difference = []
    for i in range(len(sample) - 1):
        difference.append(abs(sample[i] - sample[i + 1]))

    return np.average(difference)

def catmull_rom_interpolation(signal, L):

    signal = np.array(signal, dtype=float)
    n = len(signal)
    
    interpolated = []

    for i in range(n - 1):
        # sample_diff = abs(signal[i]-signal[i+1])
        # current_L = 3 if sample_diff > avg_difference else 2

        # Ambil 4 titik (boundary handling: clamp)
        P0 = signal[i - 1] if i - 1 >= 0 else signal[i]
        P1 = signal[i]
        P2 = signal[i + 1]
        P3 = signal[i + 2] if i + 2 < n else signal[i + 1]

        for j in range(1, L + 1):
            t = j / (L + 1)

            t2 = t * t
            t3 = t2 * t

            value = 0.5 * (
                (2 * P1) +
                (-P0 + P2) * t +
                (2*P0 - 5*P1 + 4*P2 - P3) * t2 +
                (-P0 + 3*P1 - 3*P2 + P3) * t3
            )
            if value < 0:
                value = 0
            elif value > 65535:
                value = 65535
            interpolated.append(value)
    
    return [int(round(x)) for x in interpolated]

def sample_space_determination(interpolated_sample):
    bit = []
    for x in range(len(interpolated_sample)):
        if interpolated_sample[x] == 0:
            bit.append(0)
        else:
            bit.append(math.floor(math.sqrt(math.log(interpolated_sample[x],2))))
    
    return bit

def segmentation(payload, bit):
    index = 0
    processed_payload = []
    for x in bit:
        if index >= len(payload):
            break
        
        if x <= 0:
            continue
        
        processed_payload.append(payload[index:index+x])
        index += x
    
    # print(processed_payload[16970:16975], len(processed_payload))
    return processed_payload, len(processed_payload[-1])

def convert_bin_to_dec(payload):
    isZeroInLast = False
    
    decimal = [int(payload[x], 2) for x in range(len(payload))]

    if(decimal[-1] == 0): # apakah last decimal bit adalah 0 ? karena untuk last index
        isZeroInLast = True
    return decimal, isZeroInLast

def validate(decimal_payload, interpolated_sample, nilai_n):
    required_sample = len(decimal_payload) * nilai_n
    available_sample = len(interpolated_sample) - 6 # 6 sample terakhir untuk menyimpan informasi tambahan (berapa banyak 0 di last bit, apakah ada 0 di last bit atau tidak, last bit, nilai n, nilai k, dan nilai L)
    return required_sample <= available_sample

def get_prime_number(decimal_payload):
    max_value = max(decimal_payload)
    prime = nextprime(max_value)
    return prime

def shamir_secret_sharing(decimal_payload, prime, total_shares, min_shares):
    all_data_shares = []
    for x in range(len(decimal_payload)):
        data = split_secret(decimal_payload[x], prime, total_shares, min_shares)
        all_data_shares.append(data)
    
    return all_data_shares

def split_secret(secret, prime, total_shares, min_shares):

    coefficients = [secret]  # Koefisien pertama adalah rahasia
    # Tambahkan k-1 koefisien acak lainnya
    for _ in range(min_shares - 1):
        random_coefficient = random.randint(1, prime - 1)  # Koefisien acak antara 1 dan prime-1
        coefficients.append(random_coefficient)
    
    shares = []
    for m in range(1, total_shares + 1):
        # Hitung nilai polinomial untuk x
        y = evaluate_polynomial(coefficients, m, prime)
        
        # Tambahkan pasangan (x, y) ke dalam daftar shares
        shares.append(y)
    return shares

# Fungsi untuk menghitung nilai polinomial
def evaluate_polynomial(coefficients, x, prime):
    result = 0  # Inisialisasi hasil awal
    for i, c in enumerate(coefficients):
        term = (c * (x ** i)) % prime  # Hitung setiap suku polinomial (c * x^i) mod prime
        result = (result + term) % prime  # Tambahkan suku ke hasil dengan modulus prime
    return result

def embedding_process(secret, interpolated_sample, last_bit, isZeroInLast, prime_number, nilai_n, nilai_k, current_L):
    data_shares_flat = [x for row in secret for x in row]
    new_data_shares_flat = [x - (prime_number // 2) for x in data_shares_flat]
    
    # print(len(new_data_shares_flat), len(interpolated_sample),"hhehe") #1002 264596
    
    howManyZeroInLastShares = 0
    for i in range(len(new_data_shares_flat)-1,-1,-1):
        if new_data_shares_flat[i] == 0:
            howManyZeroInLastShares += 1
        else:
            break

    embedded_sample = []

    for i in range(len(interpolated_sample)):
        if i <= len(new_data_shares_flat)-1:
            embedded_sample.append(interpolated_sample[i] + new_data_shares_flat[i])
        else:
            if i == len(interpolated_sample)-6:
                embedded_sample.append(interpolated_sample[i] + current_L)
            elif i == len(interpolated_sample)-5 and howManyZeroInLastShares > 0:
                embedded_sample.append(interpolated_sample[i] + howManyZeroInLastShares)
            elif i == len(interpolated_sample)-4 and isZeroInLast:
                embedded_sample.append(interpolated_sample[i] + 1)
            elif i == len(interpolated_sample)-3:
                embedded_sample.append(interpolated_sample[i] + int(last_bit))
            elif i == len(interpolated_sample)-2:
                embedded_sample.append(interpolated_sample[i] + nilai_n)
            elif i == len(interpolated_sample)-1:
                embedded_sample.append(interpolated_sample[i] + nilai_k)
            else:
                embedded_sample.append(interpolated_sample[i])

    return embedded_sample

def combine_old(embedded_sample, original_sample, current_L):
    combined = []

    for i in range(len(original_sample) - 1):
        combined.append(original_sample[i])
        combined.append(embedded_sample[2 * i])
        combined.append(embedded_sample[2 * i + 1])

    combined.append(original_sample[-1])

    return combined

def combine(embedded_sample, original_sample, current_L=2):
    combined = []

    for i in range(len(original_sample) - 1):
        combined.append(original_sample[i])
        for j in range(current_L):
            combined.append(embedded_sample[(current_L * i) + j])

    combined.append(original_sample[-1])

    return combined

def create_stego_audio(stego_data, file_stego_audio, frame_rate, current_L):
    process_1 = np.subtract(stego_data, [32768])
    stego_audio = np.array(process_1, dtype=np.int16)

    os.makedirs(os.path.dirname(file_stego_audio), exist_ok=True)

    stego_sample_rate = frame_rate * (current_L + 1)
    scp.write(file_stego_audio, stego_sample_rate, stego_audio)
    return True

# -------------------------------- EKSTRAKSI ---------------------------------
def pre_extract(audio, payload):
    file_payload, file_audio, file_stego_audio = init_extracting_file(audio, payload)
    results = main.start_extract(file_payload, file_audio, file_stego_audio)
    if results:
        print("Extracting Audio " + str(audio) + ", Payload " + str(payload)+ " sukses")
    else:
        print("Extracting Audio " + str(audio) + ", Payload " + str(payload)+ " gagal")
    return results

def multi_extract(total_audio, total_payload):
    for i in range(1, total_audio+1):
        for j in range(1, total_payload+1):
            results = pre_extract(i, j)
            if not results:
                return

def get_wrapped_difference(embedded_value, interpolated_value):
    difference = embedded_value - interpolated_value
    if difference > 32767:
        difference -= 65536
    elif difference < -32768:
        difference += 65536
    return difference

def separate(stego_sample, max_L=20, frame_rate=None):
    candidates = []

    candidates.extend([L for L in range(1, max_L + 1) if L not in candidates])

    for current_L in candidates:
        if frame_rate is not None and frame_rate % (current_L + 1) != 0:
            continue

        step = current_L + 1
        original_sample = stego_sample[::step]
        embedded = [stego_sample[i] for i in range(len(stego_sample)) if i % step != 0]

        if len(original_sample) < 2 or len(embedded) < 6:
            continue

        interpolated_sample = catmull_rom_interpolation(original_sample, current_L)

        if len(embedded) != len(interpolated_sample):
            continue

        extracted_L = get_wrapped_difference(embedded[-6], interpolated_sample[-6])

        nilai_n = get_wrapped_difference(embedded[-2], interpolated_sample[-2])
        nilai_k = get_wrapped_difference(embedded[-1], interpolated_sample[-1])
        last_bit = get_wrapped_difference(embedded[-3], interpolated_sample[-3])
        max_bit = max(sample_space_determination(interpolated_sample))

        is_valid_metadata = (
            extracted_L == current_L and
            nilai_n >= nilai_k and
            nilai_k > 0 and
            0 < last_bit <= max_bit
        )

        if is_valid_metadata:
            return original_sample, embedded, current_L

    raise ValueError("Nilai L tidak dapat dideteksi dari stego audio.")

def check_last_index(embedded, interpolated_sample):
    for i in range(len(embedded)-1, -1, -1):
        value = get_wrapped_difference(embedded[i], interpolated_sample[i])

        # jika value bukan 0, maka return index tersebut
        # index 1 terakhir = k
        # index 2 terakhir = n
        # index 3 terakhir = last bit
        # index 4 terakhir = apakah ada 0 di last bit atau tidak
        if value != 0 and i != len(embedded)-1 and i != len(embedded)-2 and i != len(embedded)-3 and i != len(embedded)-4 and i != len(embedded)-5 and i != len(embedded)-6:
            return i
    return None

def calculate_difference(embedded, interpolated_sample):
    last_index = check_last_index(embedded, interpolated_sample)
    difference = []
    nilai_n = get_wrapped_difference(embedded[-2], interpolated_sample[-2])
    nilai_k = get_wrapped_difference(embedded[-1], interpolated_sample[-1])
    last_bit = get_wrapped_difference(embedded[-3], interpolated_sample[-3])
    isZeroInLast = False if get_wrapped_difference(embedded[-4], interpolated_sample[-4]) == 0 else True
    howManyZeroInLastShares = get_wrapped_difference(embedded[-5], interpolated_sample[-5])

    if howManyZeroInLastShares > 0:
        last_index += howManyZeroInLastShares

    for i in range(len(embedded)):
        if i <= last_index:
            difference.append(get_wrapped_difference(embedded[i], interpolated_sample[i]))

    # return [embedded[i] - interpolated_sample[i] for i in range(len(embedded))]

    return difference, nilai_n, nilai_k, last_bit

def secret_reconstruction(difference, bit, n, k):
    prime_number = nextprime(2 ** max(bit) - 1)
    normalized_difference = [x + (prime_number // 2) for x in difference]
    
    secret = [normalized_difference[i:i+n] for i in range(0, len(normalized_difference), n)]
    all_data = []
    for i in range(len(secret)):
        if len(secret[i]) >= k:
            reconstructed_secret = reconstruct_secret2(list(enumerate(secret[i], start=1)), prime_number)
            all_data.append(reconstructed_secret)
        else:
            print("Jumlah shares yang diperoleh kurang dari k, tidak dapat merekonstruksi rahasia.")
            return

    return all_data

    
def reconstruct_secret2(shares, prime):    
    def lagrange_interpolation(x, x_s, y_s, prime):
        total = 0
        for i in range(len(x_s)):
            xi, yi = x_s[i], y_s[i]
            prod = yi
            for j in range(len(x_s)):
                if i != j:
                    xj = x_s[j]
                    prod *= (x - xj) * pow(xi - xj, -1, prime)
                    prod %= prime
            total += prod
            total %= prime
        return total

    x_s, y_s = zip(*shares)
    return lagrange_interpolation(0, x_s, y_s, prime)

def decimal_to_binary(decimal_payload, bit, last_bit):
    binary_payload = []
    for i in range(len(decimal_payload)):
        if i == len(decimal_payload)-1:
            binary_payload.append(np.binary_repr(decimal_payload[i], width=last_bit))
        else:
            binary_payload.append(np.binary_repr(decimal_payload[i], width=bit[i]))
    translated_payload = ''.join(binary_payload)
    return translated_payload

def create_payload(byte_payload, filepath):
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    with open(filepath, 'w+') as file:
        file.write(byte_payload)
        file.close()  
    return True

def create_cover_audio(original_sample, filepath, frame_rate):
    unnormalize_data = np.subtract(original_sample,[32768])
    new_data_sample = np.array(unnormalize_data,dtype=np.int16)
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    scp.write(filepath, frame_rate, new_data_sample)
    return True



# Cetak grafik waveform audio denan method plot_audio_waveform(original_sample, title="Original Audio Waveform")
def plot_audio_waveform(audio_data, title="Audio Waveform", save_path=None):
    """
    Membuat grafik waveform audio seperti gambar
    - Warna biru pada background putih
    - Grafik area yang terisi (filled area)
    - Menampilkan semua data
    - Tanpa sumbu x dan y
    """
    # Normalisasi data ke range -1 sampai 1 untuk visualisasi yang lebih baik
    # Karena audio sudah dinormalisasi (ditambah 32768), kita kurangi lagi untuk visualisasi
    audio_normalized = audio_data.astype(np.float32) - 32768
    audio_normalized = audio_normalized / 32768.0  # Normalisasi ke -1 sampai 1
    
    # Buat array waktu (sample index)
    time = np.arange(len(audio_normalized))
    
    # Buat figure dengan background putih
    plt.figure(figsize=(14, 6))
    plt.style.use('default')
    
    # Warna biru yang lebih mirip dengan gambar
    blue_color = '#0066CC'  # Biru yang lebih cerah
    
    # Plot waveform dengan filled area (biru) - simetris di atas dan bawah
    plt.fill_between(time, audio_normalized, 0, 
                     where=(audio_normalized >= 0), 
                     color=blue_color, alpha=0.8, interpolate=True)
    plt.fill_between(time, audio_normalized, 0, 
                     where=(audio_normalized < 0), 
                     color=blue_color, alpha=0.8, interpolate=True)
    
    # Plot garis waveform (opsional, untuk detail lebih halus)
    plt.plot(time, audio_normalized, color=blue_color, linewidth=0.3, alpha=0.6)
    
    # Hilangkan semua sumbu dan label
    plt.axis('off')
    
    # Set background putih
    plt.gca().set_facecolor('white')
    plt.gcf().patch.set_facecolor('white')
    
    # Set axis limits untuk tampilan yang lebih baik
    plt.ylim(-1.1, 1.1)
    
    # Adjust layout
    plt.tight_layout()
    
    # Simpan atau tampilkan
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Grafik disimpan ke: {save_path}")
    
    plt.show()
