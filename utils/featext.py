import torch
from torchaudio.transforms import Spectrogram, MelSpectrogram, MFCC, LFCC

FEATEXT_METHODS = [
    'Spectrogram',
    'MelSpectrogram',
    'MFCC',
    'LFCC'
]


class LogTransform(torch.nn.Module):

    def __init__(self):
        super(LogTransform, self).__init__()

    def forward(self, x):
        return torch.log(x + 1e-6)


def get_featext(method, sample_rate, n_fft, win_length, hop_length, n_filter=128, n_fcc=40):
    
    speckwargs = {
        'n_fft': n_fft,
        'win_length': win_length,
        'hop_length': hop_length,
    }


    if method == 'Spectrogram':
        return torch.jit.script(torch.nn.Sequential(
            Spectrogram(**speckwargs),
            LogTransform()
        ))
    
    else:

        melkwargs = speckwargs.copy()
        melkwargs['sample_rate'] = sample_rate 
        melkwargs['n_mels'] = n_filter

        if method == 'MelSpectrogram':
            return torch.jit.script(torch.nn.Sequential(
                MelSpectrogram(**melkwargs),
                LogTransform()
            ))

        elif method == 'MFCC':
            melkwargs.pop('sample_rate')
            return MFCC(sample_rate=sample_rate, n_mfcc=n_fcc, log_mels=True, melkwargs=melkwargs)

        elif method == 'LFCC':
            return LFCC(sample_rate=sample_rate, n_filter=n_filter, log_lf=True, n_lfcc=n_fcc, speckwargs=speckwargs)

        else:
            raise NotImplementedError
    