###########
# dataset #
###########
COMPRESSED_DATA_DIR = '../data_rootdir'#'/home/hdd/Datasets/Audio/GlobalSense'
COMPRESSED_DATA_VERSION = 'latest'

CLASS_NAMES = []

DATASET_PATH = 'assets/dataset'
DATASET_AUGMENTATION_PATH = '../data_augmented'
DATASET_VERSION = 'default'


######################
# feature extraction #
######################
#FEATEXT_METHODS = ['Spectrogram', 'MelSpectrogram', 'MFCC']



################
# augmentation #
################
AUGMENTATION_METHODS_DICT = {
    'White noise'      : 'white_noise',
    'Background noise' : 'background_noise',
    'Gain'             : 'gain',
    'Time shift'       : 'time_shift',
    'Pitch'            : 'pitch',
    'Speed'            : 'speed'
}
AUGMENTATION_METHODS = list(AUGMENTATION_METHODS_DICT.keys())
AUGMENTATION_IDS = list(AUGMENTATION_METHODS_DICT.values())