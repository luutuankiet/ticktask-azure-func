import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="init")
def init(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    html_form = """
    <html>
    <body>
    <form action="/api/getinput" method="post">
        <label for="input_text">Enter Text:</label><br>
        <input type="text" id="input_text" name="input_text"><br>
        <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    """

    return func.HttpResponse(html_form, mimetype="text/html")

@app.route(route="getinput", methods=['POST'])
def getinput(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    input_text = req.form.get('input_text')

    # Make an HTTP POST request to the webhook URL
    webhook_url = "https://hook.us1.make.com/mt0sveegbtqbsdhgobsqtph9nycwx7t6"
    response = requests.post(webhook_url, f'{input_text}')

    # Check if the request was successful
    if response.status_code == 200:
        return func.HttpResponse("Input sent to webhook successfully", status_code=200)
    else:
        return func.HttpResponse("Failed to send input to webhook", status_code=500)
