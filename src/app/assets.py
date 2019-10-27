from flask_assets import Bundle

app_css = Bundle('app.scss', filters='scss', output='css/app.css')
app_js = Bundle('app.js', filters='jsmin', output='js/app.js')
