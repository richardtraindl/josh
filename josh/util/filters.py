

#from .. import app


#@app.template_filter()
def fmttime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hour, minutes = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hour, minutes, seconds)
