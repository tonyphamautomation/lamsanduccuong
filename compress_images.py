"""
Nén ảnh cho website - giảm kích thước file, giữ chất lượng tốt
"""
from PIL import Image
import os

FOLDER = os.path.dirname(os.path.abspath(__file__))

# Cấu hình nén
TARGETS = {
    'logo.png':   dict(max_w=200,  max_h=200,  quality=90, fmt='PNG'),
    'img14.png':  dict(max_w=1920, max_h=1080, quality=82, fmt='JPEG', out='img14.jpg'),
    'img1.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img2.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img3.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img4.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img5.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img6.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img7.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img8.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img9.jpg':   dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img10.jpg':  dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img11.jpg':  dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img12.jpg':  dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
    'img13.jpg':  dict(max_w=1200, max_h=900,  quality=80, fmt='JPEG'),
}

saved_total = 0

for fname, cfg in TARGETS.items():
    src = os.path.join(FOLDER, fname)
    if not os.path.exists(src):
        print(f'  SKIP {fname} (not found)')
        continue

    out_name = cfg.get('out', fname)
    # Nếu convert png→jpg thì đổi tên
    if out_name != fname:
        out_path = os.path.join(FOLDER, out_name)
    else:
        out_path = src

    original_size = os.path.getsize(src)

    img = Image.open(src)

    # Xử lý transparency khi convert sang JPEG
    if cfg['fmt'] == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        bg.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = bg
    elif cfg['fmt'] == 'JPEG' and img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize nếu quá lớn
    w, h = img.size
    max_w, max_h = cfg['max_w'], cfg['max_h']
    if w > max_w or h > max_h:
        img.thumbnail((max_w, max_h), Image.LANCZOS)

    # Lưu
    save_kwargs = {'quality': cfg['quality'], 'optimize': True} if cfg['fmt'] == 'JPEG' else {'optimize': True}
    if cfg['fmt'] == 'JPEG':
        save_kwargs['progressive'] = True
    img.save(out_path, format=cfg['fmt'], **save_kwargs)

    new_size = os.path.getsize(out_path)
    saved = original_size - new_size
    saved_total += saved
    ratio = (1 - new_size/original_size) * 100

    print(f'  {fname:20s} → {out_name:20s}  {original_size//1024:>5}KB → {new_size//1024:>5}KB  (giảm {ratio:.0f}%)')

    # Xóa file gốc nếu đổi tên
    if out_name != fname and os.path.exists(src):
        os.remove(src)

print(f'\n✅ Tổng tiết kiệm: {saved_total//1024} KB ({saved_total//1048576} MB)')
