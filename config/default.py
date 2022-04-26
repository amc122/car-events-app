###########
# dataset #
###########
COMPRESSED_DATA_DIR = '/home/hdd/Datasets/Audio/GlobalSense'
COMPRESSED_DATA_VERSION = 'latest'

CLASS_NAMES = []

DATASET_PATH = 'assets/dataset'
DATASET_VERSION = 'default'


######################
# feature extraction #
######################
#FEATEXT_METHODS = ['Spectrogram', 'MelSpectrogram', 'MFCC']



################
# augmentation #
################
AUGMENTATION_METHODS = [
    'White noise',
    'Background noise',
    'Gain',
    'Time shift',
    'Pitch',
    'Speed'
]