import os
import cv2
from flask import Flask, render_template, request
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
from keras.models import load_model
from sklearn.externals import joblib
import numpy as np


UPLOAD_FOLDER = 'static/user_uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def check_or_make_folder(foldername):
    if not os.path.exists(foldername):
        os.mkdir(foldername)

check_or_make_folder(UPLOAD_FOLDER)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = load_model('saved_models/small_last4.h5') #Change to model being used

EXTRA_DETAILS_LOCATION = "disease_extra_details.csv"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def main():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        pic = preprocess_single_image(filepath)
        classes = model.predict(pic, batch_size=1)
        pred_class = np.where(classes == np.amax(classes))
        pred_class=pred_class[1]
        
     
       # pred_class = model.predict_classes(pic)[0]
        #pred_class_name = get_pred_class_name(pred_class)
        #pred_class_extra_details_dic = get_pred_class_extra_details(pred_class_name)
        #pred_class_extra_details_dic["Disease"] = pred_class_extra_details_dic["Disease"].replace("%20"," ")
        print("Predicted class is {}".format(pred_class))
        #joblib.dump(pred_class_extra_details_dic,'diseaseinfo_for_messenger.pkl') #super hacky
        pred_class=check(pred_class)
        joblib.dump(pred_class,'diseaseinfo.pkl') #super hacy
        joblib.dump(filepath,'image.pkl') #super hacy
        #print(pred_class_extra_details_dic)
        
        if request.method == 'POST':
          return render_template('home.html',dic=pred_class)

    return "upload rejected"

def check(pred):
    if pred==0:
       return "Acne and Rosacea Photos"
    elif pred==1:
       return "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions"
    elif pred==2:
       return "Atopic Dermatitis Photos"
    elif pred==3:
       return "Bullous Disease Photos"
    elif pred==4:
       return "Cellulitis Impetigo and other Bacterial Infections"
    elif pred==5:
       return "Eczema Photos"
    elif pred==6:
       return "Exanthems and Drug Eruptions"
    elif pred==7:
       return "Hair Loss Photos Alopecia and other Hair Diseases"
    elif pred==8:
       return "Herpes HPV and other STDs Photos"
    elif pred==9:
       return "Light Diseases and Disorders of Pigmentation"
    elif pred==10:
       return "Lupus and other Connective Tissue diseases"
    elif pred==11:
       return "Melanoma Skin Cancer Nevi and Moles"
    elif pred==12:
       return "Nail Fungus and other Nail Disease"
    elif pred==13:
       return "Poison Ivy Photos and other Contact Dermatitis"
    elif pred==14:
       return "Psoriasis pictures Lichen Planus and related diseases"
    elif pred==15:
       return "Scabies Lyme Disease and other Infestations and Bites"
    elif pred==16:
       return "Seborrheic Keratoses and other Benign Tumors"
    elif pred==17:
       return "Systemic Disease"
    elif pred==18:
       return "Tinea Ringworm Candidiasis and other Fungal Infections"
    elif pred==19:
       return "Urticaria Hives"
    elif pred==20:
       return "Vascular Tumors"
    elif pred==21:
       return "Vasculitis Photos"
    elif pred==22:
       return "Warts Molluscum and other Viral Infections"
    else:
        return "Class Not Found"

@app.route("/home")
def test():
    dic = 'the diagnose is : '+joblib.load("diseaseinfo.pkl")
    xx=joblib.load("image.pkl")
    return render_template('home.html',dic=dic,xx=xx)

def preprocess_single_image(filepath):
    pic = cv2.imread(filepath)
    pic = cv2.resize(pic, (224,224))
    pic = pic.astype('float32')
    pic /= 255
    pic = pic.reshape(-1,224,224,3)
    return pic

    
if __name__ == "__main__":
    server = WSGIServer(("",5000), app)
    print('Server is up')
    server.serve_forever()
