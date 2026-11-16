from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

#importing pickle files
model = pickle.load(open('classifier.pkl','rb'))
ferti = pickle.load(open('fertilizer.pkl','rb'))

@app.route('/')
def home():
    return render_template('plantindex.html')

@app.route('/Model1')
def Model1():
    return render_template('Model1.html')

@app.route('/Detail')
def Detail():
    return render_template('Detail.html')



@app.route('/predict',methods=['POST'])
def predict():
    temp = request.form.get('temp')
    humi = request.form.get('humid')
    mois = request.form.get('mois')
    soil = request.form.get('soil')
    crop = request.form.get('crop')
    nitro = request.form.get('nitro')
    pota = request.form.get('pota')
    phosp = request.form.get('phos')
    # Validate and convert inputs to integers
    try:
        vals = [temp, humi, mois, soil, crop, nitro, pota, phosp]
        if any(v is None or v == '' for v in vals):
            return render_template('Model1.html', x='Invalid input. Please provide values for all fields.')

        input_vals = [int(float(v)) for v in vals]
    except ValueError:
        return render_template('Model1.html', x='Invalid input. Please provide numeric values for all fields.')

    # Predict and decode label using the saved LabelEncoder
    try:
        pred_encoded = model.predict([input_vals])[0]
        # ferti is a LabelEncoder; use inverse_transform for safety
        try:
            pred_label = ferti.inverse_transform([pred_encoded])[0]
        except Exception:
            # fallback: if ferti has classes_ attribute, index into it
            pred_label = getattr(ferti, 'classes_', [str(pred_encoded)])[int(pred_encoded)]
    except Exception as e:
        return render_template('Model1.html', x=f'Prediction error: {e}')

    return render_template('Model1.html', x=pred_label)
# Define the search route (even if it just returns the index for now)
@app.route('/search')
def search():
    # Example: get the query parameter
    query = request.args.get('q') 
    
    # In a real app, you would process the search query here
    
    # For now, let's just confirm the search worked
    # return f"You searched for: {query}" 
    
    # Or redirect back to home/details
    return render_template('plantindex.html', search_query=query)

if __name__ == "__main__":
    app.run(debug=True)