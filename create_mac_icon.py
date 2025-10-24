from PIL import Image
import os

# Load the PNG logo we created
img = Image.open('app_icon.png')

# Create iconset directory for macOS
iconset_dir = 'app_icon.iconset'
os.makedirs(iconset_dir, exist_ok=True)

# macOS requires specific sizes
sizes = [
    (16, '16x16'),
    (32, '16x16@2x'),
    (32, '32x32'),
    (64, '32x32@2x'),
    (128, '128x128'),
    (256, '128x128@2x'),
    (256, '256x256'),
    (512, '256x256@2x'),
    (512, '512x512'),
    (1024, '512x512@2x'),
]

print('Creating macOS icon set...')
for size, name in sizes:
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(f'{iconset_dir}/icon_{name}.png')
    print(f'  ✓ Created icon_{name}.png ({size}x{size})')

print('\n✓ Icon set created in app_icon.iconset/')
print('\nTo convert to .icns on macOS, run:')
print('  iconutil -c icns app_icon.iconset')
print('\nFor Windows/Linux, app_icon.ico is already ready!')
