import face_recognition
import cv2
import os
import shutil
import zipfile

# Paths
PHOTOS_DIR = "photos"
REFERENCE_DIR = "reference"
OUTPUT_DIR = "output"
ZIP_FILE = "matched_photos.zip"

def main():
    # --- Step 1: Output folder fresh banao ---
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)  # purana delete
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Step 2: Reference face load karna ---
    ref_images = [f for f in os.listdir(REFERENCE_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not ref_images:
        print("❌ Reference folder empty hai!")
        return
    ref_path = os.path.join(REFERENCE_DIR, ref_images[0])
    ref_img = face_recognition.load_image_file(ref_path)
    ref_encodings = face_recognition.face_encodings(ref_img)

    if not ref_encodings:
        print("❌ Reference photo me face detect nahi hua!")
        return
    ref_encoding = ref_encodings[0]
    print(f"✅ Reference face loaded from {ref_path}")

    # --- Step 3: Photos folder process karna ---
    photo_files = [f for f in os.listdir(PHOTOS_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    print(f"🔍 Total {len(photo_files)} photos found... scanning now!")

    match_count = 0
    for file in photo_files:
        path = os.path.join(PHOTOS_DIR, file)
        try:
            img = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(img)

            for enc in encodings:
                result = face_recognition.compare_faces([ref_encoding], enc, tolerance=0.5)
                if result[0]:  # match mila
                    shutil.copy(path, os.path.join(OUTPUT_DIR, file))
                    match_count += 1
                    print(f"✅ Match found in: {file}")
                    break  # ek match kaafi hai, dusre faces skip
        except Exception as e:
            print(f"⚠️ Error in {file}: {e}")

    # --- Step 4: Zip banana ---
    with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
        for root, _, files in os.walk(OUTPUT_DIR):
            for f in files:
                file_path = os.path.join(root, f)
                zipf.write(file_path, os.path.relpath(file_path, OUTPUT_DIR))

    print(f"\n🎉 Done! {match_count} matched photos copied to '{OUTPUT_DIR}' and zipped into '{ZIP_FILE}'")

if __name__ == "__main__":
    main()
