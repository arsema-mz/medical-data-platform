from ultralytics import YOLO
from pathlib import Path
import pandas as pd

# Load the YOLOv8 model (use 'yolov8m' for better accuracy)
model = YOLO("yolov8m.pt")

# Path to image folder
image_dir = Path("data/raw/telegram_messages/media")
image_files = list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))

# Store detection results
results_list = []

print(f"🔍 Found {len(image_files)} image(s) in: {image_dir}")

for img_path in image_files:
    print(f"🖼️ Processing {img_path.name}...")
    try:
        results = model(img_path)
        for r in results:
            for box in r.boxes:
                cls = model.names[int(box.cls)]
                conf = float(box.conf)
                results_list.append({
                    "image_path": str(img_path),
                    "detected_object_class": cls,
                    "confidence_score": round(conf, 3)
                })
    except Exception as e:
        print(f"⚠️ Error processing {img_path.name}: {e}")

# Save to CSV
output_path = Path("data/processed/image_detections.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(results_list)
df.to_csv(output_path, index=False)

print(f"\n✅ Saved {len(df)} detections to {output_path}")
