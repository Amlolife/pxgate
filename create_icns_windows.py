"""
Create macOS .icns file from PNG on Windows
This uses pillow to create an approximation that works with PyInstaller
"""

from PIL import Image
import struct
import os

def create_icns_from_png(png_path, icns_path):
    """
    Create a basic .icns file from PNG
    This is a simplified version that works with PyInstaller on macOS
    """
    
    # Load the source image
    img = Image.open(png_path)
    
    # Sizes needed for macOS icons
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create ICNS file
    with open(icns_path, 'wb') as icns:
        # Write ICNS header
        icns.write(b'icns')
        
        # We'll write the file size later
        size_pos = icns.tell()
        icns.write(b'\x00\x00\x00\x00')
        
        # For each size, create an icon
        for size in sizes:
            # Resize image
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Convert to PNG bytes
            from io import BytesIO
            png_bytes = BytesIO()
            resized.save(png_bytes, format='PNG')
            png_data = png_bytes.getvalue()
            
            # Determine OSType based on size
            if size == 16:
                ostype = b'icp4'  # 16x16
            elif size == 32:
                ostype = b'icp5'  # 32x32
            elif size == 64:
                ostype = b'icp6'  # 64x64
            elif size == 128:
                ostype = b'ic07'  # 128x128
            elif size == 256:
                ostype = b'ic08'  # 256x256
            elif size == 512:
                ostype = b'ic09'  # 512x512
            elif size == 1024:
                ostype = b'ic10'  # 1024x1024
            else:
                continue
            
            # Write icon element
            icns.write(ostype)
            icns.write(struct.pack('>I', len(png_data) + 8))
            icns.write(png_data)
        
        # Update file size in header
        end_pos = icns.tell()
        icns.seek(size_pos)
        icns.write(struct.pack('>I', end_pos))
    
    print(f'✓ Created {icns_path}')
    print(f'  File size: {end_pos} bytes')

if __name__ == '__main__':
    print('Creating macOS .icns file from PNG...')
    print()
    
    if not os.path.exists('app_icon.png'):
        print('❌ Error: app_icon.png not found!')
        print('   Run create_logo.py first')
        exit(1)
    
    create_icns_from_png('app_icon.png', 'app_icon.icns')
    
    print()
    print('✅ app_icon.icns created successfully!')
    print()
    print('This .icns file can be used with PyInstaller on macOS.')
    print('Note: For best results, use iconutil on macOS, but this')
    print('      version will work for distribution.')
