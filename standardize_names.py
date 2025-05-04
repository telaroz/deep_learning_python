import os, glob, re, sys, argparse, logging




def sort_naturel(s): #creating a function to sort files 

    pattern = re.compile(r'([0-9]+)') #using re to compile any sequence of digits 
    segment = pattern.split(s) #splitting the string to separate text from digit 
    l1 = [] 
    for i in segment: #looping through segment where we already separated the text from the digits with re 
        if i.isdigit():
            l1.append(int(i)) #if i only contains numbers, we execute this line, else we use i.lower() 

        else:

            l1.append(i.lower())
                       
    return l1


def structured_data():
    struct = argparse.ArgumentParser(description= 'rename any given jpg files into eu_XXX file')
    struct.add_argument('TARGET_DIR', #targeted file 
                         help = 'path file containing images and labels')
    return struct.parse_args()


def main(): #scan the file, reorder and rename the files 
    args = structured_data()
    target_dir = args.TARGET_DIR #retrieve value 

    #setting up loggin instead of endless print spam....
    logging.basicConfig(level=logging.INFO,format="%(levelname)s: %(message)s") 
    logger = logging.getLogger(__name__)
    logger.info(f" scanning dir: {target_dir}")

    #get all jpg images from the file:
    pattern = os.path.join(target_dir, '*.jpg')
    img_files = glob.glob(pattern)
    if not img_files:
        logger.error('no .jpg images was found')
        sys.exit(1) # if you run into the error message, type 1 to exit the program 

    #remove path and any existing extension then natural sorting
    base_names = [
        os.path.splitext(os.path.basename(p))[0]
        for p in img_files
        ]
   
    base_names.sort(key=sort_naturel)
    logger.info(f"{len(base_names)} file sorted and ready to get renamed.")



    renamed_count, skipped_count, error_count, missing_txt_count = [0] * 4

    
    for idx, old_base in enumerate(base_names, start=1): #base_names is the sorted list
                                                         #old_base is the old name
        new_base = f"eu_{idx:03d}" #building the new base with 3 being the number of 0 we want, d is for decimal int.
        old_jpg = os.path.join(target_dir, old_base + '.jpg')


        #creating an if statement in case we already have the right format:
        if old_base == new_base:
            logger.info(f"skip: old_base is already in the righht format")
            skipped +=1
            continue

        try:
            new_jpg_name = os.path.join(target_dir, new_base + '.jpg')
            if os.path.exists(new_jpg_name):
                raise FileExistsError(f"{new_jpg_name} exists, cannot overwrite.")
            os.rename(old_jpg, new_jpg_name)
            logger.info(f"IMG: {old_base}.jpg → {new_base}.jpg")
            rename += 1           
            img_ok = True
        except Exception as e:
            logger.error(f"Couldn't rename image {old_base}: {e}")
            errors += 1
            img_ok = False


        if img_ok:
            old_txt = os.path.join(target_dir, old_base + '.txt')
            new_txt = os.path.join(target_dir, new_base + '.txt')
            if os.path.exists(old_txt):
                try:
                    if os.path.exists(new_txt):
                        raise FileExistsError(f"{new_txt} exists, skipping text.")
                    os.rename(old_txt, new_txt)
                    logger.info(f" TXT: {old_base}.txt → {new_base}.txt")
                except Exception as e:
                    logger.error(f"Couldn't rename text {old_base}: {e}")
                    errors += 1
            else:
                logger.warning(f"No .txt for {old_base}, skipping text.")
                missing_text += 1



    logger.info("Rename Summary ")
    logger.info(f"Images renamed: {rename}")
    logger.info(f"Skipped:        {skipped}")
    logger.info(f"Errors:         {errors}")

if __name__ == "__main__":
    main()




