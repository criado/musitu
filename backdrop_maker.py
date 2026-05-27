from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from card_back_maker import BACKGROUNDS, paste_center, rgba


WIDTH = 1600
HEIGHT = 600
OUTPUT = Path("the_game_maker/backdrop.png")
ASSET_FOLDER = Path("the_game_maker")
GAME_1_FOLDER = ASSET_FOLDER / "game 1"
GAME_2_FOLDER = ASSET_FOLDER / "game 2"

INNER_BACKGROUND_ALPHA = 185
GREEN_BACKGROUND = BACKGROUNDS[2][1]
GREEN_INNER_BACKGROUND = BACKGROUNDS[2][2]
BLUE_SOURCE = (8, 7, 164)


def asset_path(filename):
    path = ASSET_FOLDER / filename
    if path.exists():
        return path

    backup_path = ASSET_FOLDER / f"{filename}~"
    if backup_path.exists():
        return backup_path

    return path


def green_laso_card(path):
    img = Image.open(path).convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a and b > 90 and r < 90 and g < 90:
                shade = max(-55, min(55, round((b - BLUE_SOURCE[2]) * 0.55)))
                pixels[x, y] = tuple(max(0, min(255, channel + shade)) for channel in GREEN_BACKGROUND) + (a,)

    return img


def card_circle(source, diameter):
    if isinstance(source, Image.Image):
        img = source.convert("RGBA")
    else:
        img = Image.open(source).convert("RGBA")
    img = img.resize((diameter, diameter), Image.Resampling.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    img.putalpha(mask)
    return img


def shadowed_card(path, diameter):
    card = card_circle(path, diameter)
    shadow = Image.new("RGBA", (diameter + 28, diameter + 28), (0, 0, 0, 0))
    shadow_mask = Image.new("L", (diameter + 28, diameter + 28), 0)
    draw = ImageDraw.Draw(shadow_mask)
    draw.ellipse((14, 14, diameter + 13, diameter + 13), fill=150)
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(9))
    shadow.paste((0, 0, 0, 95), mask=shadow_mask)
    shadow.alpha_composite(card, (8, 6))
    return shadow


def paste_card(canvas, path, center, diameter, angle):
    card = shadowed_card(path, diameter)
    card = card.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    paste_center(canvas, card, center[0], center[1])


def draw_background(canvas, background, inner_background):
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((-160, -360, WIDTH + 260, HEIGHT + 460), fill=rgba(inner_background, INNER_BACKGROUND_ALPHA))
    draw.ellipse((-300, 330, 260, 850), fill=rgba(background))


def make_backdrop(output, background, inner_background, back_filename, card_folder=GAME_1_FOLDER, recolor_back=False):
    output.parent.mkdir(exist_ok=True)
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), rgba(background))
    draw_background(canvas, background, inner_background)

    back_path = asset_path(back_filename)
    back_source = green_laso_card(back_path) if recolor_back else back_path
    paste_card(canvas, back_source, (1190, 210), 330, -8)
    paste_card(canvas, card_folder / "52[face, 1].png", (565, 360), 220, -18)
    paste_card(canvas, card_folder / "1[face, 1].png", (820, 292), 260, 7)
    paste_card(canvas, card_folder / "17[face, 1].png", (1070, 345), 230, -14)
    paste_card(canvas, card_folder / "36[face, 1].png", (1390, 330), 230, 12)

    canvas.convert("RGB").save(output)
    print(f"Generated {output}")


def main():
    make_backdrop(OUTPUT, BACKGROUNDS[1][1], BACKGROUNDS[1][2], "card-back-laso.png")
    make_backdrop(
        ASSET_FOLDER / "backdrop-green.png",
        GREEN_BACKGROUND,
        GREEN_INNER_BACKGROUND,
        "card-back-laso-kasi.png",
        card_folder=GAME_2_FOLDER,
    )


if __name__ == "__main__":
    main()
