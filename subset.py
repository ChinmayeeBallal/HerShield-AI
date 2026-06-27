import os, random, shutil

src = "dataset/images"   # adjust to actual dataset path
dst = "dataset/subset"
os.makedirs(dst, exist_ok=True)

files = random.sample(os.listdir(src), 100)
for f in files:
    shutil.copy(os.path.join(src, f), os.path.join(dst, f))

print("Copied 100 images into dataset/subset")
