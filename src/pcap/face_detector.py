import cv2
import os
import sys

ROOT = '/root/Desktop/pictures'
FACES = '/root/Desktop/faces'
TRAIN = '/root/Desktop/training'

image_formats = [
    ".JPG",
    ".JPEG",
    ".PNG",
    ".GIF",
    ".BMP",
    ".TIFF",
    ".WEBP",
]

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):

        file_ext = os.path.splitext(fname)[1].upper()
        if file_ext not in image_formats:
            continue

        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)

        try:
            img = cv2.imread(fullname)
            if img is None:
                print(f"[!] Unable to read {fname}.")
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml')
            cascade = cv2.CascadeClassifier(training)
            rects = cascade.detectMultiScale(gray, 1.3, 5)
            try:
                if rects.any():
                    print('[Yay] Got a face')
                    rects[:, 2:] += rects[:, :2]
            except AttributeError:
                print(f'[*] No faces found in {fname}.')
                continue

            # highlight the faces in the image
            for x1, y1, x2, y2 in rects:
                cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

            cv2.imwrite(newname, img)
        except Exception as e:
            print(f"[!] Error processing {fname}: {str(e)}")
            continue
        except KeyboardInterrupt:
            sys.stdout.write("[*] Stopped image processing.")
            sys.stdout.flush()
            sys.exit()


if __name__ == '__main__':
    detect()
