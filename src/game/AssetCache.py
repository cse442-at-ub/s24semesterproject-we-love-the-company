from pygame import image, mixer

image_cache = dict()

def get_image(path):
    if path not in image_cache:
        image_cache[path] = image.load(path)
    
    return image_cache[path]

audio_cache = dict()

def get_audio(path):
    if path not in audio_cache:
        audio_cache[path] = mixer.Sound(path)
    
    return audio_cache[path]