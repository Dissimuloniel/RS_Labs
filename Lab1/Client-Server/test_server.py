from flask import Flask, request, render_template_string
app = Flask(__name__)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Client-Server Demo</title>
</head>
<body>
    <h2>Клиент-серверное приложение</h2>

    <form method="POST">
        <input type="text" name="message" placeholder="Введите сообщение">
        <button type="submit">Отправить</button>
    </form>

    {% if response %}
        <h3>Ответ сервера:</h3>
        <p>{{ response }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        user_message = request.form["message"]

        response = f"Сервер получил сообщение: {user_message}"
    return render_template_string(HTML_PAGE, response=response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
