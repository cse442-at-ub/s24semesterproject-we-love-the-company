from pygame import image, mixer

image_cache = dict()

def get_image(path):
    if path not in image_cache:
        image_cache[path] = image.load(path)
    
    return image_cache[path]

def uncache_image(path):
    if path in image_cache:
        del image_cache[path]
    else:
        raise ValueError("The given path is not present in the image cache.")

audio_cache = dict()

def get_audio(path):
    if path not in audio_cache:
        audio_cache[path] = mixer.Sound(path)
    
    return audio_cache[path]

def uncache_audio(path):
    if path in audio_cache:
        del audio_cache[path]
    else:
        raise ValueError("The given path is not present in the audio cache.")