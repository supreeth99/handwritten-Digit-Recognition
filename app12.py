import re
import base64


#App route for the flask app to begin excecution 
@app.route('/predictdigits/', methods=['GET','POST'])
def predict_digits():

    K.clear_session()
    parseImage(request.get_data())
    
    img=cv2.imread('output.png',0)
   
    img=255-img
    img=cv2.resize(img,(28,28))
    img=img.reshape((1,28,28))
    #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img=(img/255.0)
    model=load_model()

    result=model.predict(img)
    label=np.argmax(result,axis=1)
    #print(label)
    return str(label)

def parseImage(imgData):
    # parse canvas bytes and save as output.png
    try:   
        imgstr = re.search(b'base64,(.*)', imgData).group(1)
    #imgstr=cv2.imencode('(.*)', imgData)[1].tostring()
        with open('output.png','wb') as output:
            output.write(base64.decodebytes(imgstr))
    except:
        imgstr=None
if __name__ == '__main__':
    app.run(debug=True,threaded=False)
