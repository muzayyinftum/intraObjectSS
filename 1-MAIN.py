import importlib
methods = importlib.import_module("2-METHOD")

# ================== embedding ==================
# py 0-MAIN.py 1 1 1 1 1 1 (embedding)(single embedding)(audio 1)(payload 1)(nilai n 1)(nilai k 1)
# py 0-MAIN.py 1 2 15 11 1 1 (embedding)(multi embedding)(total audio 15)(total payload 11)(nilai n 1)(nilai k 1)

# ================== ekstraksi ==================
# py 0-MAIN.py 2 1 1 1 1 1 (ekstraksi)(single ekstraksi)(audio 1)(payload 1)(nilai n 1)(nilai k 1)
# py 0-MAIN.py 2 2 15 11 1 1 (ekstraksi)(multi ekstraksi)(total audio 15)(total payload 11)(nilai n 1)(nilai k 1)

def start_embed(file_payload, file_audio, file_stego_audio, nilai_n, nilai_k):
    frame_rate,original_sample = methods.sampling_audio(file_audio)
    binary_payload = methods.read_payload(file_payload)
    interpolated_sample = methods.catmull_rom_interpolation(original_sample)

    bit = methods.sample_space_determination(interpolated_sample)

    segmented_payload, last_bit = methods.segmentation(binary_payload, bit)
    decimal_payload, isZeroInLast = methods.convert_bin_to_dec(segmented_payload)

    prime_number = methods.get_prime_number(decimal_payload)

    data_shares = methods.shamir_secret_sharing(decimal_payload, prime_number, nilai_n, nilai_k)
    embedded_sample = methods.embedding_process(data_shares,interpolated_sample, last_bit, isZeroInLast, prime_number, nilai_n, nilai_k)

    stego_data = methods.combine(embedded_sample, original_sample)
    stego_audio = methods.create_stego_audio(stego_data, file_stego_audio, frame_rate)

def start_extract(file_payload, file_audio, file_stego_audio):
    frame_rate, stego_sample = methods.sampling_audio(file_stego_audio)
    original_sample, embedded = methods.separate(stego_sample)
    interpolated_sample = methods.catmull_rom_interpolation(original_sample)

    difference, n, k, last_bit = methods.calculate_difference(embedded, interpolated_sample)
    bit = methods.sample_space_determination(interpolated_sample)
    
    decimal_payload = methods.secret_reconstruction(difference, bit, n, k)
    binary_payload = methods.decimal_to_binary(decimal_payload, bit, last_bit)

    methods.create_payload(binary_payload, file_payload)
    methods.create_cover_audio(original_sample, file_audio)

if __name__ == "__main__":
    methods.get_params()
    
