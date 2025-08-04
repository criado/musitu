import math
import os
from PIL import Image
import cairosvg

# nanpa sitelen

nimi = [
"a",
"akesi",
"ala",
"alasa",
"ale",
"anpa",
"ante",
"anu",
"awen",
"e",
"en",
"esun",
"ijo",
"ike",
"ilo",
"insa",
"jaki",
"jan",
"jelo",
"jo",
"kala",
"kalama",
"kama",
"kasi",
"ken",
"kepeken",
"kili",
"kiwen",
"ko",
"kon",
"kule",
"kulupu",
"kute",
"la",
"lape",
"laso",
"lawa",
"len",
"lete",
"li",
"lili",
"linja",
"lipu",
"loje",
"lon",
"luka",
"lukin",
"lupa",
"ma",
"mama",
"mani",
"meli",
"mi",
"mije",
"moku",
"moli",
"monsi",
"mu",
"mun",
"musi",
"mute",
"nanpa",
"nasa",
"nasin",
"nena",
"ni",
"nimi",
"noka",
"o",
"olin",
"ona",
"open",
"pakala",
"pali",
"palisa",
"pan",
"pana",
"pi",
"pilin",
"pimeja",
"pini",
"pipi",
"poka",
"poki",
"pona",
"sama",
"seli",
"selo",
"seme",
"sewi",
"sijelo",
"sike",
"sin",
"sina",
"sinpin",
"sitelen",
"sona",
"soweli",
"suli",
"suno",
"supa",
"suwi",
"tan",
"taso",
"tawa",
"telo",
"tenpo",
"toki",
"tomo",
"tu",
"unpa",
"uta",
"utala",
"walo",
"wan",
"waso",
"wawa",
"weka",
"wile",
"kijetesantakalu",
"kin",
"kipisi",
"lanpan",
"leko",
"majuna",
"meso",
"misikeke",
"monsuta",
"n",
"namako",
"oko",
"soko",
"tonsi"
]

# lipu sin
canvas_size = 1000
radius = 400
center = canvas_size // 2

def o_sitelen_e_lipu(lipu, nanpa_lipu):
  # pali e lipu sin
  canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255, 0))

  # lukin e sitelen SVG mute
  for i in range(len(lipu)):
      angle = 2 * math.pi * i / len(lipu)
      x = center + radius * math.cos(angle)
      y = center + radius * math.sin(angle)

      # Convert SVG to PNG (temporal)
      svg_path = f"sitelen/{nimi[lipu[i]]}.svg"
      png_path = f"temp_{i+1}.png"
      cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=100, output_height=100)

      # Open PNG and paste
      img = Image.open(png_path).convert("RGBA")
      bbox = img.getbbox()
      img = img.crop(bbox)  # remove empty space if needed

      # paste center of image at (x, y)
      canvas.paste(img, (int(x - img.width / 2), int(y - img.height / 2)), img)

      os.remove(png_path)  # clean temp file

  # save result
  canvas.save(f"pini/lipu-{nanpa_lipu}.png")
