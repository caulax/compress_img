import os
import io
import time
from zipfile import ZipFile
import shutil
import glob

from PIL import Image

from app import app
from flask import render_template
from flask import request, redirect, send_file
from werkzeug.utils import secure_filename


app.config["ARCHIVE_UPLOADS"] = "./app/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["ZIP"]


# app.config["READY_ARCHIVE"] = "./app/r_archive"
# def clean_up():
#     files = glob.glob(os.path.join(app.config["READY_ARCHIVE"], "*"))
#     for f in files:
#         os.remove(f)


def change_resolution(filename):
    im = Image.open(filename)
    size = im.size
    im_resized = im.resize(size, Image.ANTIALIAS)
    # ext = filename.rsplit(".", 1)[1].upper()
    im_resized.save(filename, "JPEG")

def allowed_archive(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/upload-archive", methods=["GET", "POST"])
def upload_archive():
    if request.method == "POST":
        if request.files:
            archive = request.files["archive"]
            full_filename = os.path.join(app.config["ARCHIVE_UPLOADS"], archive.filename)
            # archive.save(full_filename)

            if archive.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_archive(archive.filename):                
                # create uniq dir
                uniq_folder_name = str(int(time.time()))

                full_uniq_folder_name = os.path.join(app.config["ARCHIVE_UPLOADS"], uniq_folder_name)
                os.mkdir(full_uniq_folder_name)

                # save zip archive
                filename = secure_filename(archive.filename)
                full_filename = os.path.join(full_uniq_folder_name, filename)
                archive.save(full_filename)

                archive_folder = os.path.join(full_uniq_folder_name, "archive")
                os.mkdir(archive_folder)

                # unpack zip archive into folder
                with ZipFile(full_filename, 'r') as zipObj:
                    zipObj.extractall(archive_folder)

                # get all images
                all_files = [os.path.join(archive_folder, f) for f in os.listdir(archive_folder) if os.path.isfile(os.path.join(archive_folder, f))]
                print(all_files)

                # change it resolution
                for img in all_files:
                    change_resolution(img)

                # result_filename = os.path.join(app.config["READY_ARCHIVE"], filename)
                
                # pack changed files into zip
                data = io.BytesIO()
                with ZipFile(data, 'w') as zf:    
                    for img in all_files:
                        zf.write(img, arcname=os.path.basename(img))

                # clean up workspace
                shutil.rmtree(full_uniq_folder_name)

                # return zip file
                data.seek(0)
                return send_file(
                    data,
                    mimetype='application/zip',
                    as_attachment=True,
                    attachment_filename=filename
                )
            else:
                print("That file extension is not allowed")
                return redirect(request.url)


    return render_template("public/templates/upload_archive.html")


@app.route("/")
def index():
    return "Nothing"
