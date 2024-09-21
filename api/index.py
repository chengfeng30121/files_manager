from flask import *
from mkhtml import generate_html_template as generate_html
from urllib.parse import quote
import tools
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/download/<path:filename>')
def download(filename: str):
    real_filename = tools.get_real_filename(filename)
    if not os.path.exists(real_filename):
        return abort(404)
    if os.path.isfile(real_filename):
        file_range =  request.headers.get("Range", None)
        print(file_range)
        if file_range is not None:
            start, end = file_range.split("=")[1].split("/")[0].split("-")
            if end == "":
                # end = str(int(start)+1024*20)
                end = os.path.getsize(real_filename)
            if int(start) > int(end):
                return abort(416)
            status = 206
        else:
            start = 0
            end = os.path.getsize(real_filename)
            end = 1024 * 20 > end and end or 1024 * 20
            status = 200
        file_content = tools.read_io(real_filename, f"{start}-{end}")
        if file_content == 413:
            return abort(413)
        response = make_response(file_content)
        print(tools.read_content_type(real_filename))
        response.headers.set('Content-Type', tools.read_content_type(real_filename))
        downloaded = request.args.get("downloaded", "True")
        downloaded = downloaded.lower() == "true"
        print(downloaded)
        if downloaded:
            response.headers.set('Content-Length', os.path.getsize(real_filename))
            response.headers.set('Content-Range', f"bytes {start}-{end}/{os.path.getsize(real_filename)}")
            response.headers.set('Accept-Ranges', 'bytes')
            response.status_code = status
            filename = filename.split("/")[-1]
            encoded_file_name = quote(filename)
            print(encoded_file_name)
            response.headers['Content-Disposition'] = f'attachment; filename={encoded_file_name}'
        print(response.headers)
        return response
    elif os.path.isdir(real_filename):
        return redirect(url_for("contents_page", path=filename))
    return abort(404)

@app.route('/<path:path>')
def contents_page(path: str):
    if not os.path.exists(tools.get_real_filename(path)):
        return abort(404)
    if os.path.isfile(tools.get_real_filename(path)):
        return redirect(url_for("download", filename=path, downloaded=False))
    return generate_html(tools.get_real_filename(path))

@app.route('/')
def index():
    return generate_html(tools.get_real_filename(""))

@app.route("/favicon.ico")
def favicon():
    return send_file(os.path.join(os.getcwd(), "templates", "favicon.ico"))

if __name__ == '__main__':
    app.run(debug=True)