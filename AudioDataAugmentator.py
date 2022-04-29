import os
import numpy as np
import librosa
import soundfile
from tqdm import tqdm

#import matplotlib.pyplot as plt


DEFAULT_SEED = 2
FORMAT = 'wav'
AVAILABLE_MANIPULATIONS = [
  "noise_injection",
  "background_injection",
  "gain_change",
  "time_shift",
  "pitch_change",
  "speed_change"
]


class AudioDataAugmentator:
  def __init__(self, sampling_rate, target_filecount):
    self.sampling_rate = sampling_rate
    self.target_filecount = target_filecount
    self.rng = np.random.default_rng(seed=DEFAULT_SEED)
    

  def set_dirpath(self, rootdir, class_name):
    self.rootdir = rootdir
    self.dirpath = os.path.join(rootdir, class_name)
    self.file_list = [
      file_name for file_name in os.listdir(self.dirpath) 
        if file_name.split('.')[-1] == FORMAT]


  def load_background(self, background_dir, manipulation_sequence):
    # initialize the background wave dictionary just in case
    # background injection is required
    # NOTE: it is a dictionary because there might be more than one
    # type of augmentation with background_injection
    self.background_wave_dict = {}

    # check if the required manipulations are available
    for manipulation in manipulation_sequence:
      # check requred manipulation methods
      method, args = manipulation
      assert method in AVAILABLE_MANIPULATIONS
      if method == 'background_injection':
        # load the required background files in memory
        if args[1] not in list(self.background_wave_dict.keys()):
          background_subdir = os.path.join(background_dir, args[1])
          background_subdir_listdir = os.listdir(background_subdir)
          sizes = np.zeros(len(background_subdir_listdir), dtype=int)
          for i, background_filename in enumerate(background_subdir_listdir):
            path = os.path.join(background_subdir, background_filename)
            aux, _ = librosa.load(path, sr=self.sampling_rate, mono=True)
            sizes[i] = aux.shape[0]
          self.background_wave_dict[args[1]] = np.zeros(sizes.sum())
          left = 0
          for i, background_filename in enumerate(background_subdir_listdir):
            path = os.path.join(background_subdir, background_filename)
            right = left + sizes[i]
            self.background_wave_dict[args[1]][left:right], _ = librosa.load(path, sr=self.sampling_rate, mono=True)
            left += sizes[i]


  def augment(self, manipulation_sequence):

    # create a new directory for the augmented data
    new_dirpath = "{}_augmented".format(self.dirpath)
    if not os.path.exists(new_dirpath):
      os.makedirs(new_dirpath)

    # count number of files to augment and manipulations to be applied
    file_count = len(self.file_list)
    manipulation_count = len(manipulation_sequence)

    # start processing
    for i in tqdm(range(file_count)):
      file_name = self.file_list[i]
      file_path = self.dirpath + '/' + file_name
      self.wave, _ = librosa.load(file_path, sr=self.sampling_rate, mono=True)

      for manipulation in manipulation_sequence:
        method, args = manipulation

        args_str = ""
        for arg in args:
          if len(str(arg)) < 32:
            args_str += "_{}".format(arg)

        new_filepath = "{}/{}{}_{}".format(new_dirpath, method, args_str, file_name)

        if not os.path.isfile(new_filepath):
          if method == "noise_injection":
            augmented_wave = self._noise_injection(args[0], args[1])

          if method == "background_injection":
            augmented_wave = self._background_injection(args[0], args[1])

          elif method == "gain_change":
            augmented_wave = self._gain_change(args[0])

          elif method == "time_shift":
            augmented_wave = self._time_shift(args[0], args[1])

          elif method == "pitch_change":
            augmented_wave = self._pitch_change(args[0])

          elif method == "speed_change":
            augmented_wave = self._speed_change(args[0])

          soundfile.write(new_filepath, augmented_wave, self.sampling_rate)
        
        else:
          print("{} already exists, its manipulation has been omitted...".format(new_filepath))


  def _noise_injection(self, snr_db, noise_type):
    if noise_type == "white":
      noise = self.rng.standard_normal(len(self.wave))
    elif noise_type == "pink":
      raise NotImplementedError
    else:
      raise NotImplementedError
    snr = 10.0**(snr_db / 10.0)
    pow_input = np.mean((self.wave - np.mean(self.wave))**2.0)
    noise_factor = np.sqrt(pow_input / snr)
    augmented_wave = self.wave + noise_factor * noise
    augmented_wave = augmented_wave.astype(type(self.wave[0]))
    return augmented_wave


  def _background_injection(self, snr_db, background_class):
    #background_path = np.random.choice(list(self.background_wave_dict.keys()))
    #background_wave = self.background_wave_dict[background_path]
    background_wave = self.background_wave_dict[background_class]
    wave_len = self.wave.shape[0]
    background_wave_len = background_wave.shape[0]
    index_start_max = background_wave_len - wave_len
    assert index_start_max > 0
    index_start = np.random.randint(low=0, high=index_start_max)
    background_wave_segment = background_wave[index_start:index_start+wave_len]
    snr = 10.0**(snr_db / 10.0)
    pow_input = np.mean((self.wave - np.mean(self.wave))**2.0)
    pow_background = np.mean((background_wave_segment - np.mean(background_wave_segment))**2.0)
    background_factor = np.sqrt(pow_input / (snr * pow_background))
    return self.wave + background_factor * background_wave_segment


  def _gain_change(self, gain_factor):
    return gain_factor * self.wave


  def _time_shift(self, shift_max, shift_direction):
    shift = self.rng.integers(low=0, high=self.sampling_rate*shift_max)
    if shift_direction == "right":
      shift = -shift 
    elif shift_direction == "both":
      direction = self.rng.integers(low=0, high=2)
      if direction == 1:
        shift = -shift
    augmented_wave = np.roll(self.wave, shift)
    if shift > 0:
      augmented_wave[:shift] = 0
    else:
      augmented_wave[shift:] = 0
    return augmented_wave 


  def _pitch_change(self, n_steps): # TODO check if new librosa version is ok
    return librosa.effects.pitch_shift(self.wave, sr=self.sampling_rate, n_steps=n_steps, bins_per_octave=12)


  def _speed_change(self, speed_factor):
    return librosa.effects.time_stretch(self.wave, rate=speed_factor)


if __name__ == '__main__':
  ada = AudioDataAugmentator(16000, 1000)
  manipulation_sequence = [
    ['background_injection', [10, 'Music_Background']],
    ['background_injection', [10, 'Safety_Noise']]
  ]
  ada.load_background('./assets/dataset', manipulation_sequence)
  print(ada.background_wave_dict['Music_Background'].shape, ada.background_wave_dict['Music_Background'])
  print(ada.background_wave_dict['Safety_Noise'].shape, ada.background_wave_dict['Safety_Noise'])
  #ada.set_dirpath('./dataset', 'Tire')

  