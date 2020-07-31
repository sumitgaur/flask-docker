import json
import logging
import os

from flask import Flask, request, flash, redirect, render_template_string
import boto3

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/v1/api', methods=['POST'])
def postSomeThing():
    content = request.json
    name = content['name']
    logger.info('name: %s', name)
    return "Hello %s" % name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(type(file))
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_tmp_path)
            object_name = "{}/{}".format(WATCH_DIR, file.filename)
            upload_to_s3(file_tmp_path, BUCKET, object_name)

            flash("File uploaded to S3 and submitted for extraction. \n S3 Object Key - " + "{}/{}/{}".format(BUCKET,
                                                                                                              WATCH_DIR,
                                                                                                              file.filename))
            trigger_dag(object_name)
            return redirect(request.url)

    return render_template_string('''
    <!doctype html>
    <html>
    <title>Upload file for extraction</title>
    <h1>Upload file for extraction</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
      {% with messages = get_flashed_messages() %}
         {% if messages %}
               {% for message in messages %}
               <p><label>{{ message }}</label></p>
               {% endfor %}
         {% endif %}
      {% endwith %}
    </form>
   </html>
    ''')


def upload_to_s3(file_name, bucket, object_name):
    """
    Function to upload a file to an S3 bucket
    """
    print(file_name, bucket, object_name)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response


def trigger_dag(object_name):
    """

    :param object_name:
    :return:
    """
    import requests, os
    airflow_server = os.environ.get('AIRFLOW_SERVER', None)
    if not airflow_server:
        raise KeyError("Airflow server address not passed.Please set AIRFLOW_SERVER env.")

    url = "http://{}/api/experimental/dags/s3_dag_test/dag_runs".format(airflow_server)
    print("hitting ")
    # payload = "{\"conf\":\"{\\\"s3_object_key\\\":\\\"Message from external using python code \\\"}\"}"
    payload = json.dumps({"conf": {"s3_object_key": object_name}})
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))


BUCKET = 'textract-gs'
WATCH_DIR = 'file-watch-dir'

trigger_dag("file-watch-dir/0110_099.png")
# upload_to_s3('/tmp/0110_099.png',BUCKET,'file-watch-dir/0110_099.png')
