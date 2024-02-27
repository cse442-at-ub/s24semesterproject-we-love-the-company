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
        self.assertTrue(AssetCache.is_image_cached("src/game/Assets/button.png"))
        self.assertFalse(AssetCache.is_image_cached("src/game/background.jpg"))
    
    def test_uncache_image(self):
        AssetCache.get_image("src/game/Assets/button.png")
        AssetCache.uncache_image("src/game/Assets/button.png")
        self.assertNotIn("src/game/Assets/button.png",AssetCache.image_cache)
    
    def test_flush_images(self):
        AssetCache.get_image("src/game/Assets/button.png")
        AssetCache.get_image("src/game/background.jpg")
        self.assertEqual(AssetCache.flush_image_cache(),2)
        self.assertEqual(AssetCache.flush_image_cache(),0)
    
    def test_cache_sound(self):
        AssetCache.get_audio("src/game/Assets/button_click.mp3")
        self.assertIn("src/game/Assets/button_click.mp3",AssetCache.audio_cache)
        self.assertTrue(AssetCache.is_audio_cached("src/game/Assets/button_click.mp3"))
        self.assertFalse(AssetCache.is_audio_cached("src/game/Assets/Background_music_menu.wav"))
    
    def test_uncache_sound(self):
        AssetCache.get_audio("src/game/Assets/button_click.mp3")
        AssetCache.uncache_audio("src/game/Assets/button_click.mp3")
        self.assertNotIn("src/game/Assets/button_click.mp3",AssetCache.audio_cache)

    def test_flush_audio(self):
        AssetCache.get_audio("src/game/Assets/button_click.mp3")
        AssetCache.get_audio("src/game/Assets/Background_music_menu.wav")
        self.assertEqual(AssetCache.flush_audio_cache(),2)
        self.assertEqual(AssetCache.flush_audio_cache(),0)
