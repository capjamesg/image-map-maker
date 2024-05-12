import optparse

# support for command line arguments
parser = optparse.OptionParser()

parser.add_option("-i", "--image", dest="image", help="Image path")

(options, args) = parser.parse_args()

# if no image, break
if not options.image:
    parser.error("Image path not given")

from fastsam import FastSAM, FastSAMPrompt
from flask import Flask, request, jsonify, render_template, send_from_directory
import supervision as sv
import os
import cv2

app = Flask(__name__)

model = FastSAM("./FastSAM-s.pt")
DEVICE = "cpu"
IMAGE_PATH = options.image
image = cv2.imread(IMAGE_PATH)

imgsz = image.shape[:2]

everything_results = model(
    IMAGE_PATH, device=DEVICE, retina_masks=True, imgsz=imgsz, conf=0.4, iou=0.9
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        json_data = request.get_json()
        points = json_data["points"]

        new_points = [x[:-1] for x in points]
        points = new_points

        prompt_process = FastSAMPrompt(IMAGE_PATH, everything_results, device=DEVICE)

        final_labels = []

        # if a point is in the region of another point, set label to 0; else, set to 1
        for l in new_points:
            x, y = l
            # check if point is in the region of another point
            has_chosen = False
            for p in points:
                # if x, y are wihtin any of the points, set label to 0
                if p != l and abs(p[0] - x) < 10 and abs(p[1] - y) < 10:
                    final_labels.append(0)
                    has_chosen = True
                    break

            if not has_chosen:
                final_labels.append(1)

        ann = prompt_process.point_prompt(points=points, pointlabel=final_labels)

        polygons = sv.mask_to_polygons(ann[0])

        return jsonify({"coords": [x.tolist() for x in polygons]})

    return render_template("sam.html", image=IMAGE_PATH)


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


if __name__ == "__main__":
    app.run(debug=True)
