import math
import random
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFilter

from sitelen import kule, nimi


SEED = 20260524
SIZE = 1125
CENTER = SIZE // 2
CONTENT_SCALE = 0.9
OUTPUT_FOLDER = Path("pini_game_maker")
SITELEN = Path("sitelen")

BACKGROUNDS = [
    ("paper", (252, 249, 237), (239, 249, 248)),
    ("laso", (8, 7, 164), (255, 255, 82)),
    ("laso-green", (92, 184, 118), (255, 255, 82)),
    ("jelo", (255, 250, 225), (252, 244, 236)),
]
INNER_CIRCLE_RADIUS = 515
INNER_CIRCLE_ALPHA = 185
TITLE_BACKING = (255, 255, 255)
COLOR_BY_NAME = {name: kule[color_index] for name, color_index in nimi}
EXCLUDED_DECORATIVE_NAMES = {"lipu", "musi", "namako", "o"}
NAMES_BY_COLOR_INDEX = {}
for name, color_index in nimi:
    if name not in EXCLUDED_DECORATIVE_NAMES:
        NAMES_BY_COLOR_INDEX.setdefault(color_index, []).append(name)


def rgba(color, alpha=255):
    return color + (alpha,)


def scale_length(value):
    return round(value * CONTENT_SCALE)


def scale_offset(value):
    return value * CONTENT_SCALE


def scale_coord(value):
    return CENTER + (value - CENTER) * CONTENT_SCALE


def scale_box(box):
    return tuple(scale_coord(value) for value in box)


def scale_inset(inset):
    return round(CENTER - (CENTER - inset) * CONTENT_SCALE)


def load_png_symbol(name, size, color, alpha=255, matte=(255, 255, 255)):
    img = Image.open(SITELEN / f"{name}.png").convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.thumbnail((size, size), Image.Resampling.LANCZOS)
    mask = img.split()[3]
    effective_mask = mask.point(lambda value: round(value * alpha / 255))
    colored = Image.new("RGBA", img.size, rgba(color))
    matte_img = Image.new("RGBA", img.size, rgba(matte))
    out = Image.composite(colored, matte_img, effective_mask)
    out.putalpha(mask.point(lambda value: 255 if value else 0))
    return out


def load_svg_symbol(name, size, color, alpha=255, outline=None, outline_width=0):
    png = cairosvg.svg2png(
        url=str(SITELEN / f"{name}.svg"),
        output_width=size,
        output_height=size,
    )
    img = Image.open(BytesIO(png)).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    mask = img.split()[3]
    pad = outline_width + 8
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))

    if outline and outline_width:
        outline_mask = Image.new("L", out.size, 0)
        outline_mask.paste(mask, (pad, pad))
        outline_mask = outline_mask.filter(ImageFilter.MaxFilter(outline_width * 2 + 1))
        out.paste(Image.new("RGBA", out.size, rgba(outline, alpha)), mask=outline_mask)

    fill = Image.new("RGBA", img.size, rgba(color, alpha))
    out.paste(fill, (pad, pad), mask)
    return out


def paste_center(canvas, img, x, y):
    canvas.alpha_composite(img, (round(x - img.width / 2), round(y - img.height / 2)))


def rotate_symbol(img, angle):
    return img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)


def symbol_color(name):
    return COLOR_BY_NAME[name]


def pick_decorative_names(rng, count, used_names=None):
    color_indices = list(NAMES_BY_COLOR_INDEX)
    picks = []
    used_names = set() if used_names is None else used_names
    previous_color_index = None

    for _ in range(count):
        color_choices = [
            color_index
            for color_index in color_indices
            if color_index != previous_color_index
            and any(name not in used_names for name in NAMES_BY_COLOR_INDEX[color_index])
        ]
        color_index = rng.choice(color_choices)
        name_choices = [name for name in NAMES_BY_COLOR_INDEX[color_index] if name not in used_names]
        name = rng.choice(name_choices)
        picks.append(name)
        used_names.add(name)
        previous_color_index = color_index

    return picks


def scatter_edge_symbols(canvas):
    rng = random.Random(SEED)
    used_names = set()
    outer_names = pick_decorative_names(rng, 28, used_names)
    inner_names = pick_decorative_names(rng, 16, used_names)

    # A loose outer wreath, kept inside the inscribed circular cut.
    for i in range(28):
        angle = math.tau * i / 28 + rng.uniform(-0.035, 0.035)
        radius = scale_offset(rng.choice([408, 430, 452]))
        name = outer_names[i]
        color = symbol_color(name)
        size = scale_length(rng.randint(92, 132))
        symbol = load_png_symbol(name, size, color, alpha=230)
        symbol = rotate_symbol(symbol, math.degrees(angle) - 90 + rng.uniform(-18, 18))
        paste_center(canvas, symbol, CENTER + radius * math.cos(angle), CENTER + radius * math.sin(angle))

    for i in range(16):
        angle = math.tau * i / 16 + math.tau / 32
        name = inner_names[i]
        color = symbol_color(name)
        symbol = load_png_symbol(name, scale_length(82), color, alpha=215)
        symbol = rotate_symbol(symbol, math.degrees(angle) + 90)
        radius = scale_offset(320)
        paste_center(canvas, symbol, CENTER + radius * math.cos(angle), CENTER + radius * math.sin(angle))


def draw_inner_background(canvas, inner_background):
    draw = ImageDraw.Draw(canvas)
    radius = scale_length(INNER_CIRCLE_RADIUS)
    draw.ellipse(
        (
            CENTER - radius,
            CENTER - radius,
            CENTER + radius,
            CENTER + radius,
        ),
        fill=rgba(inner_background, INNER_CIRCLE_ALPHA),
    )


def draw_center_title(canvas):
    title = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

    musi = load_svg_symbol("musi", scale_length(425), symbol_color("musi"), outline=TITLE_BACKING, outline_width=scale_length(8))
    tu = load_svg_symbol("tu", scale_length(325), symbol_color("tu"), outline=TITLE_BACKING, outline_width=scale_length(8))
    paste_center(title, musi, CENTER, CENTER + scale_offset(-126))
    paste_center(title, tu, CENTER, CENTER + scale_offset(152))

    accent = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(accent)
    draw.ellipse(scale_box((538, 538, 587, 587)), fill=rgba(kule[5]))

    canvas.alpha_composite(accent)
    canvas.alpha_composite(title)


def make_card(background, inner_background):
    canvas = Image.new("RGBA", (SIZE, SIZE), rgba(background))
    draw_inner_background(canvas, inner_background)
    scatter_edge_symbols(canvas)
    draw_center_title(canvas)
    return canvas.convert("RGB")


def main():
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    outputs = []
    for name, background, inner_background in BACKGROUNDS:
        path = OUTPUT_FOLDER / f"card-back-{name}.png"
        make_card(background, inner_background).save(path)
        outputs.append(path)

    main_output = OUTPUT_FOLDER / "card-back.png"
    make_card(BACKGROUNDS[0][1], BACKGROUNDS[0][2]).save(main_output)
    outputs.append(main_output)

    print("Generated:")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
