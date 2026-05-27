from math import hypot
from pathlib import Path

from PIL import Image

from card_back_maker import BACKGROUNDS


ASSET_FOLDER = Path("the_game_maker")
SOURCE = ASSET_FOLDER / "card-back-laso.png"
OUTPUT = ASSET_FOLDER / "card-back-laso-kasi.png"
GREEN_BACKGROUND = BACKGROUNDS[2][1]
BLUE_SOURCE = (8, 7, 164)


def yellow_circle_bounds(img):
    xs = []
    ys = []
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a and r > 190 and g > 170 and b < 120:
                xs.append(x)
                ys.append(y)

    if not xs:
        raise ValueError(f"No yellow circle found in {SOURCE}")

    return min(xs), max(xs), min(ys), max(ys)


def recolor_blue_outside_yellow_circle(img):
    left, right, top, bottom = yellow_circle_bounds(img)
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    radius = max(right - left, bottom - top) / 2 + 1
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            if hypot(x - center_x, y - center_y) <= radius:
                continue

            r, g, b, a = pixels[x, y]
            if not a:
                pixels[x, y] = GREEN_BACKGROUND + (255,)
            elif b > 90 and r < 90 and g < 90:
                shade = max(-55, min(55, round((b - BLUE_SOURCE[2]) * 0.55)))
                green = tuple(max(0, min(255, channel + shade)) for channel in GREEN_BACKGROUND)
                pixels[x, y] = green + (a,)

    return img


def main():
    img = Image.open(SOURCE).convert("RGBA")
    recolor_blue_outside_yellow_circle(img).save(OUTPUT)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
