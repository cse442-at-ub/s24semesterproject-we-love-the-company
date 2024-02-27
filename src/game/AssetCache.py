from pygame import image, mixer

image_cache = dict()

def get_image(path):
    """Load an image from path."""
    """Skips loading the image again if the image is already stored in the cache."""
    if path not in image_cache:
        image_cache[path] = image.load(path)
    
    return image_cache[path]

def uncache_image(path):
    """Removes a given image path from the image cache."""
    """If the path is not already cached, an error is thrown."""
    if path in image_cache:
        del image_cache[path]
    else:
        raise ValueError("The given path is not present in the image cache.")

def flush_image_cache():
    """Removes all entries from the image cache."""
    """Returns the number of elements in the cache before flushing."""
    output = len(image_cache)
    image_cache = dict()
    return output

audio_cache = dict()

def get_audio(path):
    """Load a sound from path."""
    """Skips loading the sound again if the sound is already stored in the cache."""
    if path not in audio_cache:
        audio_cache[path] = mixer.Sound(path)
    
    return audio_cache[path]

def uncache_audio(path):
    """Removes a given sound path from the sound cache."""
    """If the path is not already cached, an error is thrown."""
    if path in audio_cache:
        del audio_cache[path]
    else:
        raise ValueError("The given path is not present in the audio cache.")

def flush_audio_cache():
    """Removes all entries from the audio cache."""
    """Returns the number of elements in the cache before flushing."""
    output = len(audio_cache)
    audio_cache = dict()
    return output