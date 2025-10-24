from PIL import Image, ImageDraw, ImageFont

# Create a 256x256 image with transparency
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw rounded rectangle background with modern blue color
draw.rounded_rectangle(
    [(20, 20), (236, 236)], 
    radius=40, 
    fill='#6B9BD1'
)

# Try to load a nice font, fallback to default
try:
    # Try different font options
    font = None
    for font_name in ['arial.ttf', 'segoeui.ttf', 'calibri.ttf']:
        try:
            font = ImageFont.truetype(font_name, 140)
            break
        except:
            continue
    if font is None:
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 140)
except:
    # Fallback to default font
    font = ImageFont.load_default()

# Draw "PX" text in white with subtle stroke
draw.text(
    (128, 128), 
    'PX', 
    fill='white', 
    font=font, 
    anchor='mm',
    stroke_width=2,
    stroke_fill='#5A88BD'
)

# Save as PNG
img.save('app_icon.png')
print('✓ PNG created: app_icon.png')

# Save as ICO with multiple sizes
img.save('app_icon.ico', format='ICO', sizes=[
    (256, 256), 
    (128, 128), 
    (64, 64), 
    (48, 48), 
    (32, 32), 
    (16, 16)
])
print('✓ ICO created: app_icon.ico')
print('\nNew PX logo created successfully!')
