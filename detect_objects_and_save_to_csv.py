import cv2
import csv
import time
from ultralytics import YOLO

def detect_objects_and_save_video(model_path, output_csv_path, output_video_path):
    # Load YOLO model
    yolo = YOLO(model_path)

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Define CSV file header
    csv_header = ['Frame', 'Object', 'Confidence', 'X', 'Y', 'Width', 'Height']

    # Open CSV file for writing
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)

        # Get video frame properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        # Main loop
        frame_count = 0
        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 번호를 0부터 시작하여 증가시킴
            frame_count += 1

            if frame_count % 10 == 0:
                end_time = time.time()
                fps = frame_count / (end_time - start_time)
                print(f"FPS: {fps:.2f}")
                start_time = end_time

            # Detect objects
            results = yolo(frame)
            
            # Save detected objects to CSV
            for result in results:
                detected_objects = result.boxes.cpu()
                if detected_objects is None:
                    writer.writerow([frame_count, "No object detected", "", "", "", ""])
                else:
                    for obj in detected_objects:
                        label = int(obj.cls)
                        confidence = obj.conf
                        bbox = obj.xyxy
                        writer.writerow([frame_count, yolo.names[label], confidence, *bbox])

            # Write frame with bounding boxes to video
            out_video.write(frame)

            # Display frame with bounding boxes
            # cv2.imshow('YOLOv8 Object Detection', frame_with_boxes)

            # Exit loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    out_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model_path = "C:/Users/rlati/yolov8/validation_results/content/runs/detect/yolov8n_custom/weights/best.pt"
    output_csv_path = "detected_objects.csv"  # Path to output CSV file
    output_video_path = "output_video.avi"  # Path to output video file
    detect_objects_and_save_video(model_path, output_csv_path, output_video_path)
