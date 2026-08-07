from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "icons")
os.makedirs(OUT, exist_ok=True)

INK = (26, 26, 26, 255)      # #1a1a1a
ACCENT = (163, 35, 31, 255)  # #a3231f
PAPER = (251, 250, 247, 255) # #fbfaf7

FONT_PATH = "C:/Windows/Fonts/georgiab.ttf"

def draw_monogram(size, bg, fg, safe_ratio=1.0):
    img = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(img)
    text = "LP"
    max_w = size * 0.72 * safe_ratio
    font_size = int(size * 0.5)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    while tw > max_w and font_size > 10:
        font_size -= 2
        font = ImageFont.truetype(FONT_PATH, font_size)
        bbox = d.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1]
    d.text((x, y), text, font=font, fill=fg)
    # thin rule under the monogram, evoking the masthead double rule
    rule_w = tw * 0.9
    rule_y = y + th + size * 0.06
    d.rectangle(
        [(size / 2 - rule_w / 2, rule_y), (size / 2 + rule_w / 2, rule_y + max(2, size // 90))],
        fill=fg,
    )
    return img

# Standard icons (full bleed accent red background)
icon_512 = draw_monogram(512, ACCENT, PAPER)
icon_512.convert("RGB").save(os.path.join(OUT, "icon-512.png"))
icon_512.resize((192, 192), Image.LANCZOS).convert("RGB").save(os.path.join(OUT, "icon-192.png"))

# Maskable icon: keep monogram within the ~80% safe zone
icon_maskable = draw_monogram(512, ACCENT, PAPER, safe_ratio=0.72)
icon_maskable.convert("RGB").save(os.path.join(OUT, "icon-512-maskable.png"))

# Apple touch icon (opaque, 180x180)
apple = draw_monogram(180, ACCENT, PAPER)
apple.convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))

# Favicons
for s in (16, 32, 48):
    fav = draw_monogram(s, ACCENT, PAPER)
    fav.convert("RGB").save(os.path.join(OUT, f"favicon-{s}.png"))

# Multi-size .ico
fav_imgs = [draw_monogram(s, ACCENT, PAPER).convert("RGB") for s in (16, 32, 48)]
fav_imgs[0].save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

print("Icons written to", os.path.abspath(OUT))
