import scipy.io.wavfile
import numpy as np
import os

def sampling_audio(fileaudio):
    rate, data = scipy.io.wavfile.read(fileaudio)
    data = np.array(data,dtype=np.int16)
    nilaimax=[32768]
    data=np.add(data,nilaimax)
    return data

def read_number_data(file):
    test = np.loadtxt(file,dtype=np.int)
    return test

def compare_data(data1, data2):
    hasil = 1
    if len(data1) != len(data2):
        print('panjang Original = ', len(data1))
        print('panjang extracted = ', len(data2))
        return 0
    else:
        miss_data = 0
        for x in range (len(data1)):
            if data1[x] != data2[x]:
                print('miss pada index : ', x)
                print('data1 = ', data1[x], '| data2 = ', data2[x])
                miss_data += 1
                hasil = 0
    return hasil

def read_number_data(file):
    test = np.loadtxt(file,dtype=np.int)
    return test

def create_payload(translated_payload, filepath):
    os.makedirs(os.path.dirname(filepath),exist_ok=True)
    with open(filepath, 'w') as file:
        file.write(translated_payload)
        file.close()
    return

def read_payload(file_payload):
    with open(file_payload, mode='r') as file:
        data_payload = file.read()
    data_payload=[data_payload[x] for x in range (len(data_payload)) if data_payload[x]!='\t']
    data_payload=[x.strip('\x00') for x in data_payload]
    binary_data = '0b'+''.join(data_payload)
    binary_data = [x.strip('ÿþ') for x in binary_data]
    binary_data = binary_data[2::]
    if(binary_data[0]!='1' and binary_data[0]!='0') and (binary_data[1]!='1' and binary_data[1]!='0'):
        binary_data = binary_data[2::]

    return binary_data

def audioCompare(audio, payload):
    original_audio = 'stegoaudioDataset/Audio/data'+audio+'_mono.wav'
    extract_audio = 'extractingResults/stego_audio'+audio+'_payload'+payload+'/audio.wav'

    original_sample = sampling_audio(original_audio)
    extracted_sample = sampling_audio(extract_audio)

    hasil_audio = compare_data(original_sample, extracted_sample)

    if hasil_audio == 0:
        print('Extracted Audio '+str(audio)+' Payload '+str(payload)+' GAGAL')
        return False
    else:
        print('Extracted Audio '+str(audio)+' Payload '+str(payload)+' SUKSES')
        return True

def payloadCompare(audio, payload):
    original_payload = 'stegoaudioDataset/Payload/payload'+payload+'.txt'
    extract_payload = 'extractingResults/stego_audio'+audio+'_payload'+payload+'/payload.txt'

    data_ori_payload = read_payload(original_payload)
    data_ext_payload = read_payload(extract_payload)
    
    hasil_payload = compare_data(data_ori_payload, data_ext_payload)

    if hasil_payload == 0:
        print('Extracted Audio '+str(audio)+' Payload '+str(payload)+' GAGAL')
        return False
    else:
        print('Extracted Audio '+str(audio)+' Payload '+str(payload)+' SUKSES')
        return True

def main():
    print('================= Compare Data =================')
    type = input('1. audio\n2. payload \nPilih : ')

    print('================= Input Data =================')
    user_input = input('Number of audio and payload (Enter for all): ').strip()

    if user_input == "":
        audio, payload = "all", "all"
    else:
        parts = user_input.split()
        if len(parts) != 2:
            raise ValueError("Harus isi 2 nilai: audio dan payload")
        audio, payload = parts

    if type == '1':
        if audio == 'all' and payload == 'all':
            for i in range(1, 16):
                for j in range(1, 12):
                    results = audioCompare(str(i), str(j))
                    if not results:
                        return
        else:
            audioCompare(audio, payload)
    elif type == '2':
        if audio == 'all' and payload == 'all':
            for i in range(1, 16):
                for j in range(1, 12):
                    results = payloadCompare(str(i), str(j))
                    if not results:
                        return
        else:
            payloadCompare(audio, payload)

if __name__ == "__main__":
    main()