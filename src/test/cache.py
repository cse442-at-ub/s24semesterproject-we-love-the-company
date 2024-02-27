import unittest

import os
import sys

# python is such a well designed language
sys.path.append(os.getcwd() + "/src/game")

import unittest
import AssetCache

class AssetCacheTests(unittest.TestCase):
    def setUp(self):
        AssetCache.image_cache = dict()
        AssetCache.audio_cache = dict()

    def test_cache_image(self):
        AssetCache.get_image("src/game/Assets/button.png")
        self.assertIn("src/game/Assets/button.png",AssetCache.image_cache)
    
    def test_uncache_image(self):
        AssetCache.get_image("src/game/Assets/button.png")
        self.assertIn("src/game/Assets/button.png",AssetCache.image_cache)

        AssetCache.uncache_image("src/game/Assets/button.png")
        self.assertNotIn("src/game/Assets/button.png",AssetCache.image_cache)
    
    def test_cache_sound(self):
        AssetCache.get_audio("src/game/Assets/button_click.mp3")
        self.assertIn("src/game/Assets/button_click.mp3",AssetCache.audio_cache)
    
    def test_uncache_sound(self):
        AssetCache.get_audio("src/game/Assets/button_click.mp3")
        self.assertIn("src/game/Assets/button_click.mp3",AssetCache.audio_cache)

        AssetCache.uncache_audio("src/game/Assets/button_click.mp3")
        self.assertNotIn("src/game/Assets/button_click.mp3",AssetCache.audio_cache)
