
import wave
from pathlib import Path

INPUT_FOLDER = Path(r"C:\ProgramData\Minimal\Current\Factory\Wavetables")
OUTPUT_FOLDER = INPUT_FOLDER / "Extracted WAV"

HEADER_SIZE = 102
SAMPLES_PER_FRAME = 2048
BYTES_PER_SAMPLE = 3  # 24-bit PCM

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

for source in INPUT_FOLDER.rglob("wavetable.ma_table"):
    if OUTPUT_FOLDER in source.parents:
        continue

    data = source.read_bytes()
    payload = data[HEADER_SIZE:]

    frame_size = SAMPLES_PER_FRAME * BYTES_PER_SAMPLE

    if not payload or len(payload) % frame_size != 0:
        print(f"Skipped: {source}")
        continue

    frame_count = len(payload) // frame_size

    # Name the WAV after its original parent folder's UUID
    output = OUTPUT_FOLDER / f"{source.parent.name}.wav"

    try:
        with wave.open(str(output), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(3)
            wav.setframerate(44100)
            wav.writeframes(payload)

        print(f"Extracted: {output.name} ({frame_count} frames)")

    except Exception as error:
        print(f"Error: {source}: {error}")

print("Extraction finished!")
