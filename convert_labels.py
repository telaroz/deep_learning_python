import os
from PIL import Image #get size of images, also opens them 
import glob


img_dir = "eu"
label_dir = 'eu'
output_label_dir = 'datasets/labels/unsplit'
default_yolo_class_ID = 0


#making sure target dir exists:
if not os.path.isdir(output_label_dir):
    os.makedirs(output_label_dir)
    print(f'created {output_label_dir}') 


list_label = glob.glob(os.path.join(img_dir,"*.txt")) #gather all txt 
print(f'scan labels in: {img_dir}')
print(len(list_label))
print("Using class ID =", default_yolo_class_ID, "(all the same)")

#converion that worked, error detected while trying to converse 
conv_count= 0
err_count = 0

for txt_path in list_label:
    base = os.path.splitext(os.path.basename(txt_path))[0]
    img_path = os.path.join(img_dir, base + '.jpg')
    out_path = os.path.join(output_label_dir, base + '.txt')



#if os.path.isfile(img_path):
    #process_

    if not os.path.isfile(img_path):
            print("Whoops no image for", txt_path)
            err_count += 1
            continue  
    
    try:
        img = Image.open(img_path)
        w, h = img.size #width and height , no need for channel 
        img.close()
    except Exception as e:
        print(f"Error opening {img_path}: {e}")
        err_count += 1
        continue  # passe au label suivant

        if w == 0 or h == 0:
            print('error')
            err_count += 1
            continue


    try:
        data = open(txt_path).read().splitlines()

    except Exception as e:
        print("Err reading", txt_path, ":", e)
        err_count += 1
        continue

    if len(data) == 0:
        print("Empty labels in", txt_path, "- blank")
        open(out_path, 'w').close()
        conv_count += 1
        continue


    yolo_lines = []

    for idx, ln in enumerate(data):
        bits = ln.split()

        if len(bits) < 5:
            print("Malformed line", idx+1, "--->", bits)
            continue
        imgname= bits[0]
        if not imgname.endswith('.jpg'):
            print("Line", idx+1, "no .jpg, skip")
            continue

        try:
            x_min = float(bits[1]); y_min= float(bits[2])
            bw = float(bits[3]); bh  = float(bits[4])
        except:
            print("Non-numeric coordinates on line", idx+1)
            continue


        x_center = x_min + bw/2
        y_center = y_min + bh/2
        x_center_norm = x_center / w
        y_center_norm = y_center / h
        w_norm = bw / w
        h_norm = bh / h

        if x_center_norm < 0: x_center_norm = 0
        if x_center_norm > 1: x_center_norm = 1
        if y_center_norm < 0: y_center_norm = 0
        if y_center_norm > 1: y_center_norm = 1
        if w_norm < 0:       w_norm = 0
        if w_norm > 1:       w_norm = 1
        if h_norm < 0:       h_norm = 0
        if h_norm > 1:       h_norm = 1

        line = str(default_yolo_class_ID) + " " + \
               f"{x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}"
        yolo_lines.append(line)
         


    
    
        if len(yolo_lines) > 0:
            fout = open(out_path, 'w')
            
        for l in yolo_lines:
            fout.write(l + "\n")
        fout.close()
        conv_count += 1
        print(f"Wrote {len(yolo_lines)} labels to {out_path}")
    else:
        if not os.path.isfile(out_path):
            open(out_path, 'w').close()
        conv_count += 1
        print("No valid annotations, created empty", out_path)

# final summary
print("\n=== All done! ===")
print("Processed", conv_count, "files.")
print("Errors/skipped", err_count, "files.")
print("Check labels in", output_label_dir)



        





