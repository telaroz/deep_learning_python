import os
from PIL import Image #get size of images, also opens them 
import glob


img_dir = "eu"
label_dir = 'eu'
output_label_dir = 'datasets/labels/unsplit'
default_yolo_class_ID = 0


#making sure target dir exists:

list_label = glob.glob(os.path.join(img_dir,"*.txt")) #gather all txt 


for txt_path in list_label:
    base = os.path.splitext(os.path.basename(txt_path))[0]
    img_path = os.path.join(img_dir, base + '.jpg')
    out_path = os.path.join(output_label_dir, base + '.txt')


    img = Image.open(img_path)
    w, h = img.size #width and height 
    img.close()


    data = open(txt_path).read().splitlines()



    if len(data) == 0:
        print("Empty labels in", txt_path, "- blank")
        open(out_path, 'w').close()
        conv_count += 1
        continue


    yolo_labels = []

    for idx, ln in enumerate(data):
        bits = ln.split()

        x_min = float(bits[1])
        y_min = float(bits[2])
        bw = float(bits[3])
        bh  = float(bits[4])


        x_center = x_min + bw/2
        y_center = y_min + bh/2
        x_center_norm = x_center / w
        y_center_norm = y_center / h
        w_norm = bw / w
        h_norm = bh / h

yolo_labels.append(f"0 {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}")

with open(output_label_dir, 'w') as f_out:
    f_out.write("\n".join(yolo_labels))