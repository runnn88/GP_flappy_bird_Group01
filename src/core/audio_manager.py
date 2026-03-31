import math
from array import array
from pathlib import Path

import pygame


class AudioManager:
    def __init__(self, context):
        self.context = context
        self.available = False
        self.music_tracks = {}
        self.sfx = {}
        self.active_track = None
        self.music_channel = None
        self.using_music_stream = False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self.available = True
        except pygame.error:
            return

        self.music_tracks = self._load_music_tracks()
        self.sfx = self._load_sfx()
        self._apply_state()

    def play_music(self, track_name, restart=False):
        if track_name == self.active_track and not restart:
            self._apply_state()
            return

        self.active_track = track_name
        self.stop()
        self._apply_state()

    def set_sound_enabled(self, enabled):
        self.context.sound_enabled = enabled
        self._apply_state()

    def set_music_volume(self, volume):
        self.context.music_volume = max(0.0, min(1.0, volume))
        self._apply_state()

    def play_sfx(self, name):
        if not self.available or not self.context.sound_enabled:
            return

        sound = self.sfx.get(name)
        if sound is None:
            return

        sound.set_volume(min(1.0, self.context.music_volume * 1.2))
        sound.play()

    def stop(self):
        if self.using_music_stream:
            pygame.mixer.music.stop()
            self.using_music_stream = False
        if self.music_channel is not None:
            self.music_channel.stop()
            self.music_channel = None

    def _apply_state(self):
        if not self.available or not self.music_tracks:
            return

        if not self.context.sound_enabled:
            self.stop()
            return

        track_name = self.active_track or "menu"
        track = self.music_tracks.get(track_name) or self.music_tracks.get("menu")
        if track is None:
            return

        if track["kind"] == "file":
            try:
                if not self.using_music_stream:
                    self.stop()
                pygame.mixer.music.load(track["path"])
                pygame.mixer.music.set_volume(self.context.music_volume)
                pygame.mixer.music.play(-1, start=track.get("start", 0.0))
                self.using_music_stream = True
                self.music_channel = None
                return
            except pygame.error:
                fallback_track = track.get("fallback")
                if fallback_track is None:
                    return
                track = fallback_track

        sound = track["sound"]
        self.using_music_stream = False
        sound.set_volume(self.context.music_volume)
        if self.music_channel is None or not self.music_channel.get_busy():
            self.music_channel = sound.play(loops=-1)
        if self.music_channel is not None:
            self.music_channel.set_volume(self.context.music_volume)

    def _load_music_tracks(self):
        audio_root = Path("assets/audio")
        tracks = {
            "menu": self._load_file_or_fallback(
                audio_root / "prettyjohn1-background-music-505061.mp3",
                [261.63, 329.63, 392.00, 329.63, 293.66, 329.63, 392.00, 329.63],
                beat_seconds=0.42,
                start=0.3,
            ),
            "game": self._load_file_or_fallback(
                audio_root / "nesrality-rimsky-korsakov-flight-of-the-bumble-bee-remix-110689.mp3",
                [329.63, 392.00, 440.00, 392.00, 349.23, 392.00, 440.00, 392.00],
                beat_seconds=0.26,
                start=1.3,
            ),
        }
        return tracks

    def _load_sfx(self):
        return {
            "boom": self._build_boom_sfx(),
        }

    def _load_file_or_fallback(self, path, melody, beat_seconds, start=0.0):
        fallback_sound = self._build_music_loop(melody, beat_seconds)
        if path.exists():
            return {
                "kind": "file",
                "path": str(path),
                "start": start,
                "fallback": {"kind": "sound", "sound": fallback_sound},
            }
        return {"kind": "sound", "sound": fallback_sound}

    def _build_music_loop(self, melody, beat_seconds):
        sample_rate = 22050
        samples = array("h")
        max_amplitude = 32767

        for frequency in melody:
            note_samples = int(sample_rate * beat_seconds)
            for index in range(note_samples):
                t = index / sample_rate
                envelope = min(1.0, index / 400) * min(1.0, (note_samples - index) / 800)
                tone = (
                    math.sin(2 * math.pi * frequency * t)
                    + 0.18 * math.sin(4 * math.pi * frequency * t)
                    + 0.08 * math.sin(math.pi * frequency * t)
                )
                value = int(max_amplitude * 0.065 * envelope * tone)
                samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _build_boom_sfx(self):
        sample_rate = 22050
        duration = 0.42
        total_samples = int(sample_rate * duration)
        samples = array("h")
        max_amplitude = 32767

        for index in range(total_samples):
            t = index / sample_rate
            progress = index / total_samples
            envelope = max(0.0, 1.0 - progress) ** 2.2
            frequency = 120 - (85 * progress)
            tone = math.sin(2 * math.pi * frequency * t)
            rumble = math.sin(2 * math.pi * (frequency * 0.45) * t)
            noise = math.sin(2 * math.pi * (37 + (index % 17)) * t)
            value = int(max_amplitude * envelope * (0.22 * tone + 0.14 * rumble + 0.06 * noise))
            samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())
