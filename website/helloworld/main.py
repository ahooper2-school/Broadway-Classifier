import sys
from flask import render_template


# [START functions_classify_image]
def classify_image(request):
    return render_template('main.html')
# [END functions_classify_image]
