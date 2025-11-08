import subprocess


class AudioPlaybackHelper:
    @staticmethod
    def play_audio(
        file_path: str,
    ) -> bool:
        players = ["paplay", "ffplay -nodisp -autoexit", "aplay", "mpg123", "play"]

        for player in players:
            try:
                subprocess.run(f"{player} {file_path}", shell=True, capture_output=True, timeout=300, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue

        return False
