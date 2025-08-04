import math
import os
from PIL import Image
import cairosvg

# nanpa sitelen

kule= [
# (200, 50, 50), # loje
# (150, 40, 40), # loje pi pona nanpa wan
(175, 45, 45), # loje meso
(90, 100, 230), # laso telo
# (60, 150, 60), # laso kasi
# (180, 220, 160), # laso kasi pi pona nanpa wan
# (160, 200, 140), # laso kasi pi pona nanpa tu
(110, 175, 180), # laso kasi pi pona nanpa tu wan
(220, 200, 60), # jelo
(230, 120, 40), # jelo loje
(130, 80, 160), # loje laso
(0  , 0 ,   0) # pimeja
]

nimi = [
("tan", 0),
("telo", 1),
("kasi", 2),
("taso", 3),
("tenpo", 4),
("toki", 5),
("tomo", 6),
### 
("loje", 0),
("laso", 1),
("alasa", 2),
("jelo", 3),
("oko", 4),
("leko", 5),
("pimeja", 6),
### 
("lupa", 0),
("nena", 1),
("soko", 2),
("meso", 3),
("misikeke", 4),
("monsuta", 5),
("kule", 6),
### 
("pan", 0),
("sama", 1),
("mi", 2),
("sina", 3),
("ona", 4),
("pilin", 5),
("pini", 6),
### 
("palisa", 0),
("nimi", 1),
("li", 2),
("lili", 3),
("suli", 4),
("lanpan", 5),
("walo", 6),
### 
("ike", 0),
("pona", 1),
("la", 2),
("wawa", 3),
("wile", 4),
("kijetesantakalu", 5),
("kipisi", 6),
### 
("open", 0),
("poki", 1),
("poka", 2),
("anpa", 3),
("sinpin", 4),
("monsi", 5),
("wan", 6),
### 
("ala", 0),
("en", 1),
("lipu", 2),
("sitelen", 3),
("sona", 4),
("insa", 5),
("utala", 6),
### 
("weka", 0),
("namako", 1),
("kama", 2),
("awen", 3),
("tawa", 4),
("majuna", 5),
("unpa", 6),
### 
("a", 0),
("o", 1),
("n", 2),
("kin", 3),
("jan", 4),
("mani", 5),
("mije", 6),
### 
("kepeken", 0),
("ilo", 1),
("moku", 2),
("uta", 3),
("pana", 4),
("kalama", 5),
("suwi", 6),
### 
("mute", 1),
("tu", 0),
("suno", 3),
("tonsi", 2),
("sijelo", 4),
("selo", 5),
("supa", 6),
### 
("ni", 0),
("nasin", 1),
("kala", 2),
("soweli", 3),
("akesi", 4),
("waso", 5),
("pipi", 6),
### 
("mu", 2),
("musi", 1),
("seli", 0),
("seme", 3),
("sewi", 4),
("sike", 5),
("sin", 6),
### 
("ale", 0),
("ante", 1),
("anu", 2),
("e", 3),
("esun", 4),
("ijo", 5),
("jaki", 6),
### 
("jo", 0),
("ken", 1),
("kili", 2),
("kiwen", 3),
("ko", 4),
("kon", 5),
("kulupu", 6),
### 
("kute", 0),
("lape", 1),
("lawa", 2),
("len", 3),
("lete", 4),
("linja", 5),
("pi", 6),
### 
("lon", 0),
("luka", 1),
("lukin", 2),
("ma", 3),
("mama", 4),
("meli", 5),
("pakala", 6),
### 
("moli", 0),
("mun", 1),
("nanpa", 2),
("nasa", 3),
("noka", 4),
("olin", 5),
("pali", 6),
####
]

# lipu sin
canvas_size = 850
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
      angle = math.tau * i / 8 + math.pi/8 # rotate so a vertex is on top
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
        color = Image.new("RGBA", img.size, kule[nimi[lipu[i]][1]] + (255,))
        img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        img.paste(color, mask=mask)


        # Rotate so bottom points outward
        degrees = math.degrees(angle) - 90  # +90 so "bottom" points outward
        img = img.rotate(-degrees, expand=True)

        # paste center of image at (x, y)
        canvas.paste(img, (int(x - img.width / 2), int(y - img.height / 2)), img)

        os.remove(png_path)  # clean temp file
  
  sitelen_sike(360, lipu[:8], ante= math.tau/16)
  sitelen_sike(160, lipu[8:])

  # save result
  canvas.save(f"pini/lipu-{nanpa_lipu}.png")
