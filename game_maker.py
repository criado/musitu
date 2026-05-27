import math
import random
import sys
from collections import Counter
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image

sys.dont_write_bytecode = True
from sitelen import kule, nimi


NANPA_SITELEN = 133
K = 12
SAMPLE_COUNT = 52
EXTRA_COUNT = 15
SEED = 1495835

BASE_CANVAS_SIZE = 850
CANVAS_SIZE = 1125
SCALE = CANVAS_SIZE / BASE_CANVAS_SIZE
CONTENT_SCALE = 0.9
CENTER = CANVAS_SIZE / 2
OUTER_RING_RADIUS = 346 * SCALE * CONTENT_SCALE
INNER_RING_RADIUS = 160 * SCALE * CONTENT_SCALE
GLYPH_SIZE = round(150 * SCALE * CONTENT_SCALE)

SITELEN_FOLDER = Path("sitelen")
OUTPUT_FOLDER = Path("pini_game_maker")
GAME_1_FOLDER = OUTPUT_FOLDER / "game 1"
GAME_2_FOLDER = OUTPUT_FOLDER / "game 2"


def lon_e_lipu():
    lipu = []

    for i in range(K - 1):
        lipu.append([(K - 1) * (K - 1) + K - 1] + [i * (K - 1) + l for l in range(K - 1)])

    for j in range(K - 1):
        for i in range(K - 1):
            lipu.append([(K - 1) * (K - 1) + j] + [(l * (K - 1)) + (i + j * l) % (K - 1) for l in range(K - 1)])

    lipu.append([(K - 1) * (K - 1) + l for l in range(K)])

    assert len(lipu) == NANPA_SITELEN
    assert all(len(l) == K for l in lipu)
    return lipu


def shuffled_lipu_order(lipu):
    rng = random.Random(SEED)
    rng.shuffle(list(range(len(nimi))))  # match the random state consumed by sitelen.py

    ale_lipu = []
    for lipu_wan in lipu:
        lipu_sin = lipu_wan.copy()
        rng.shuffle(lipu_sin)
        ale_lipu.append(lipu_sin)
    return ale_lipu


def sitelen_svg(symbol_index):
    svg_path = SITELEN_FOLDER / f"{nimi[symbol_index][0]}.svg"
    png_bytes = cairosvg.svg2png(url=str(svg_path), output_width=GLYPH_SIZE, output_height=GLYPH_SIZE)
    img = Image.open(BytesIO(png_bytes)).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    mask = img.split()[3]
    color = Image.new("RGBA", img.size, kule[nimi[symbol_index][1]] + (255,))
    img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    img.paste(color, mask=mask)
    return img


def sitelen_sike(canvas, radius, lipu, ante=0):
    for i, symbol_index in enumerate(lipu):
        angle = ante + 2 * math.pi * i / len(lipu)
        x = CENTER + radius * math.cos(angle)
        y = CENTER + radius * math.sin(angle)

        img = sitelen_svg(symbol_index)
        degrees = math.degrees(angle) - 90
        img = img.rotate(-degrees, expand=True)

        canvas.paste(img, (int(x - img.width / 2), int(y - img.height / 2)), img)


def o_sitelen_e_lipu(lipu, nanpa_lipu, output_folder):
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (255, 255, 255))

    sitelen_sike(canvas, OUTER_RING_RADIUS, lipu[:8], ante=math.tau / 16)
    sitelen_sike(canvas, INNER_RING_RADIUS, lipu[8:])

    canvas.save(output_folder / f"{nanpa_lipu}[face, 1].png")


def sampled_card_indices():
    sample_rng = random.Random(SEED)
    return sorted(sample_rng.sample(range(NANPA_SITELEN), SAMPLE_COUNT))


def symbol_counts(lipu, card_indices):
    counts = Counter()
    for card_index in card_indices:
        counts.update(lipu[card_index])
    for symbol_index in range(NANPA_SITELEN):
        counts.setdefault(symbol_index, 0)
    return counts


def choose_greedy_card(lipu, remaining_indices, counts):
    for threshold in range(2, max(counts.values()) + 1):
        target_symbols = {symbol_index for symbol_index, count in counts.items() if count <= threshold}
        candidates = [
            card_index
            for card_index in remaining_indices
            if sum(symbol_index in target_symbols for symbol_index in lipu[card_index]) >= 2
        ]
        if candidates:
            break
    else:
        target_symbols = {symbol_index for symbol_index, count in counts.items() if count == min(counts.values())}
        candidates = list(remaining_indices)

    def score(card_index):
        card = lipu[card_index]
        target_hits = sum(symbol_index in target_symbols for symbol_index in card)
        low_count_sum = sum(counts[symbol_index] for symbol_index in card)
        updated_counts = counts.copy()
        updated_counts.update(card)
        return (
            -target_hits,
            low_count_sum,
            max(updated_counts.values()) - min(updated_counts.values()),
            max(updated_counts.values()),
            card_index,
        )

    return min(candidates, key=score)


def greedy_extra_card_indices(lipu, base_indices):
    counts = symbol_counts(lipu, base_indices)
    remaining_indices = set(range(NANPA_SITELEN)) - set(base_indices)
    extra_indices = []

    for _ in range(EXTRA_COUNT):
        card_index = choose_greedy_card(lipu, remaining_indices, counts)
        extra_indices.append(card_index)
        remaining_indices.remove(card_index)
        counts.update(lipu[card_index])

    return extra_indices


def generated_card_indices(lipu):
    base_indices = sampled_card_indices()
    return base_indices + greedy_extra_card_indices(lipu, base_indices)


def remaining_card_indices(game_1_indices):
    game_1_set = set(game_1_indices)
    return [card_index for card_index in range(NANPA_SITELEN) if card_index not in game_1_set]


def clean_face_images(folder):
    folder.mkdir(exist_ok=True)
    for old_png in folder.glob("*.png"):
        if old_png.name.startswith("lipu-") or old_png.name.endswith("[face, 1].png"):
            old_png.unlink()


def main():
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    clean_face_images(OUTPUT_FOLDER)
    clean_face_images(GAME_1_FOLDER)
    clean_face_images(GAME_2_FOLDER)

    lipu = lon_e_lipu()
    lipu_order = shuffled_lipu_order(lipu)
    game_1_indices = generated_card_indices(lipu)
    game_2_indices = remaining_card_indices(game_1_indices)

    for output_index, card_index in enumerate(game_1_indices, start=1):
        o_sitelen_e_lipu(lipu_order[card_index], output_index, GAME_1_FOLDER)

    for output_index, card_index in enumerate(game_2_indices, start=1):
        o_sitelen_e_lipu(lipu_order[card_index], output_index, GAME_2_FOLDER)

    print(f"Generated {len(game_1_indices)} images in {GAME_1_FOLDER}")
    print(f"Generated {len(game_2_indices)} images in {GAME_2_FOLDER}")


if __name__ == "__main__":
    main()
