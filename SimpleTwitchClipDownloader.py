import json
import urllib.request
import os

# Clips JSON lists
clip_list_file = "../../clips.json"


# clip file extension. DO NOT CHANGE
ext = ".mp4"

# save directory. 
# ex1. absolute dir: "C:\\Clips"
# ex2. relative dir to source code : "../folder"
save_dir = "../../"

# counters
num_saved_clips = 0
num_total_clips = 0
num_error_clips = 0
num_skipped_clips = 0

# save error list as a json file
error_list = []

with open(clip_list_file, encoding="utf-8") as json_file:
    json_data = json.load(json_file)
    num_total_clips = len(json_data)
    print("total", num_total_clips,  "clips!")

    for clips in json_data :
        date = clips["created_at"]
        title = clips["title"]
        url = clips["download_url"]
        game_name = clips["game"]["name"]

        filename = date + "_" + game_name + "_" + title + ext
        # remove all not available charcters for Windows
        replaced_filename = filename.replace(":", "").replace("<", "").replace(">", "").replace("\"", "").replace("\\", "").replace("|", "").replace("?","").replace("*", "").replace("/", "")
        # directory
        replaced_filename = save_dir + replaced_filename
        print(replaced_filename)

        try:
            # if file is not exist or file size is zero (i.e error while writing)
            if (not os.path.exists(replaced_filename)) or (os.stat(replaced_filename).st_size is 0) :
                clip_file = urllib.request.urlopen(url)
                with open(replaced_filename, 'wb') as output:
                    output.write(clip_file.read())
            else:
                num_skipped_clips = num_skipped_clips + 1

        except IOError as e :
            error_list.append(clips)
            num_error_clips = num_error_clips  + 1
            
        num_saved_clips = num_saved_clips + 1
        print("(%d / %d), Err : %d " % (num_saved_clips, num_total_clips,num_error_clips), end='\n')

print("saving clips done...skipped %d, total %d errors occured" % (num_skipped_clips,num_error_clips), end="\n")

# save error clip list as a json array
with open(save_dir + "errors.json", "w", encoding="utf-8") as error_file:
    json.dump(error_list, error_file, ensure_ascii=False)