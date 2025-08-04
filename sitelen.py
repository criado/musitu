import math
import os
from PIL import Image
import cairosvg

# nanpa sitelen

kule= [
(200, 50, 50), # loje
(60, 150, 60), # laso
(60, 100, 200), # laso 2
(220, 200, 60), # jelo
(230, 120, 40), # jelo loje
(130, 80, 160), # loje laso
(0  , 0 ,   0) # pimeja
]

nimi=[
("a", "0"),
("akesi", "1"),
("ala", "2"), 
("alasa", "3"), 
("ale", "4"), 
("anpa", "5"), 
("ante", "6"), 
("anu", "0"), 
("awen", "1"), 
("e", "2"), 
("en", "3"), 
("esun", "4"), 
("ijo", "5"), 
("ike", "6"), 
("ilo", "0"), 
("insa", "1"), 
("jaki", "2"), 
("jan", "3"), 
("jelo", "4"), 
("jo", "5"), 
("kala", "6"), 
("kalama", "0"), 
("kama", "1"), 
("kasi", "2"), 
("ken", "3"), 
("kepeken", "4"), 
("kili", "5"), 
("kiwen", "6"), 
("ko", "0"), 
("kon", "1"), 
("kule", "2"), 
("kulupu", "3"), 
("kute", "4"), 
("la", "5"), 
("lape", "6"), 
("laso", "0"), 
("lawa", "1"), 
("len", "2"), 
("lete", "3"), 
("li", "4"), 
("lili", "5"), 
("linja", "6"), 
("lipu", "0"), 
("loje", "1"), 
("lon", "2"), 
("luka", "3"), 
("lukin", "4"), 
("lupa", "5"), 
("ma", "6"), 
("mama", "0"), 
("mani", "1"), 
("meli", "2"), 
("mi", "3"), 
("mije", "4"), 
("moku", "5"), 
("moli", "6"), 
("monsi", "0"), 
("mu", "1"), 
("mun", "2"), 
("musi", "3"), 
("mute", "4"), 
("nanpa", "5"), 
("nasa", "6"), 
("nasin", "0"), 
("nena", "1"), 
("ni", "2"), 
("nimi", "3"), 
("noka", "4"), 
("o", "5"), 
("olin", "6"), 
("ona", "0"), 
("open", "1"), 
("pakala", "2"), 
("pali", "3"), 
("palisa", "4"), 
("pan", "5"), 
("pana", "6"), 
("pi", "0"), 
("pilin", "1"), 
("pimeja", "2"), 
("pini", "3"), 
("pipi", "4"), 
("poka", "5"), 
("poki", "6"), 
("pona", "0"), 
("sama", "1"), 
("seli", "2"), 
("selo", "3"), 
("seme", "4"), 
("sewi", "5"), 
("sijelo", "6"), 
("sike", "0"), 
("sin", "1"), 
("sina", "2"), 
("sinpin", "3"), 
("sitelen", "4"), 
("sona", "5"), 
("soweli", "6"), 
("suli", "0"), 
("suno", "1"), 
("supa", "2"), 
("suwi", "3"), 
("tan", "4"), 
("taso", "5"), 
("tawa", "6"), 
("telo", "0"), 
("tenpo", "1"), 
("toki", "2"), 
("tomo", "3"), 
("tu", "4"), 
("unpa", "5"), 
("uta", "6"), 
("utala", "0"), 
("walo", "1"), 
("wan", "2"), 
("waso", "3"), 
("wawa", "4"), 
("weka", "5"), 
("wile", "6"), 
("kijetesantakalu", "0"), 
("kin", "1"), 
("kipisi", "2"), 
("lanpan", "3"), 
("leko", "4"), 
("majuna", "5"), 
("meso", "6"), 
("misikeke", "0"), 
("monsuta", "1"), 
("n", "2"), 
("namako", "3"), 
("oko", "4"), 
("soko", "5"), 
("tonsi", "6"), 
]


# lipu sin
canvas_size = 1000
radius = 400
center = canvas_size // 2

def o_sitelen_e_lipu(lipu, nanpa_lipu):
  assert(len(lipu)==12)
  # pali e lipu sin
  canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255, 0))

  from PIL import ImageDraw

  # draw the outer circle
  #draw = ImageDraw.Draw(canvas)
  #outer_radius = radius + 60

  # draw the outer octagon
  draw = ImageDraw.Draw(canvas)
  outer_radius = radius + 60
  octagon = []

  for i in range(8):
      angle = math.tau * i / 8 - math.pi / 4  # rotate so a vertex is on top
      x = center + outer_radius * math.cos(angle)
      y = center + outer_radius * math.sin(angle)
      octagon.append((x, y))

  draw.polygon(octagon, outline=(0, 0, 0), width=4)

  bbox = [
      center - outer_radius,
      center - outer_radius,
      center + outer_radius,
      center + outer_radius
  ]
  #draw.ellipse(bbox, outline=(0, 0, 0), width=4)  # black circle, 4 px wide

  def sitelen_sike(radius, lipu, ante=0):
    # lukin e sitelen SVG mute
    for i in range(len(lipu)):
        angle = ante + 2 * math.pi * i / len(lipu)
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)

        # Convert SVG to PNG (temporal)
        svg_path = f"sitelen/{nimi[lipu[i]][0]}.svg"
        png_path = f"temp_{i+1}.png"
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=150, output_height=150)

        # Open PNG and rotate
        img = Image.open(png_path).convert("RGBA")
        bbox = img.getbbox()
        img = img.crop(bbox)

        # Apply color tint
        #tint = Image.new("RGBA", img.size, kule[int(nimi[lipu[i]][1])] + (0,))
        #tint = Image.new("RGBA", img.size, (200, 50,50)+ (0,))
        #img = Image.composite(tint, img, img.split()[3])
        # Convert to grayscale alpha mask
        mask = img.split()[3]  # alpha channel as mask
        color = Image.new("RGBA", img.size, kule[int(nimi[lipu[i]][1])] + (255,))
        img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        img.paste(color, mask=mask)


        # Rotate so bottom points outward
        degrees = math.degrees(angle) - 90  # +90 so "bottom" points outward
        img = img.rotate(-degrees, expand=True)

        # paste center of image at (x, y)
        canvas.paste(img, (int(x - img.width / 2), int(y - img.height / 2)), img)

        os.remove(png_path)  # clean temp file
  
  sitelen_sike(360, lipu[:8])
  sitelen_sike(160, lipu[8:], ante= math.tau/16)

  # save result
  canvas.save(f"pini/lipu-{nanpa_lipu}.png")
