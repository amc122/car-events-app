from torchaudio.transforms import Spectrogram, MelSpectrogram, MFCC, LFCC

FEATEXT_METHODS = [
    'Spectrogram',
    'MelSpectrogram',
    'MFCC',
    'LFCC'
]

def get_featext(method, sample_rate, n_fft, win_length, hop_length, n_filter=128, n_fcc=40):
    
    if method == 'Spectrogram':
        return Spectrogram(n_fft=n_fft, win_length=win_length, hop_length=hop_length)

    elif method == 'MelSpectrogram':
        return MelSpectrogram(sample_rate=sample_rate, n_fft=n_fft, win_length=win_length, hop_length=hop_length, n_mels=n_filter)

    elif method == 'MFCC':
        return MFCC(sample_rate=sample_rate, n_fft=n_fft, win_length=win_length, hop_length=hop_length, n_mels=n_filter, n_mfcc=n_fcc)

    elif method == 'LFCC':
        return LFCC(sample_rate=sample_rate, n_fft=n_fft, win_length=win_length, hop_length=hop_length, n_filter=n_filter, n_lfcc=n_fcc)

    else:
        raise NotImplementedError
    