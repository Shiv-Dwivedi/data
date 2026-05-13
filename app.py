from flask import Flask, request, Response
import requests

app = Flask(__name__)

FILE_URL = "https://github.com/Shiv-Dwivedi/data/releases/download/v1/botsv1.stream_http.json"


@app.route("/")
def home():
    return """
    <h2>JSON Line Viewer</h2>

    Examples:<br><br>

    <a href="/line?line=0">/line?line=0</a><br>
    <a href="/line?line=1">/line?line=1</a><br>
    <a href="/line?line=2">/line?line=2</a><br><br>

    Use:
    /line?line=NUMBER
    """


@app.route("/line")
def line():

    line_no = request.args.get("line", default=0, type=int)

    if line_no < 0:
        return Response("Invalid line number", status=400)

    chunk_size = 1024 * 1024  # 1MB chunks

    current_byte = 0
    current_line = 0

    buffer = b""

    while True:

        headers = {
            "Range": f"bytes={current_byte}-{current_byte + chunk_size - 1}"
        }

        r = requests.get(FILE_URL, headers=headers, stream=True)

        if r.status_code not in (200, 206):
            return Response(
                f"GitHub request failed: {r.status_code}",
                status=500
            )

        chunk = r.content

        if not chunk:
            break

        buffer += chunk

        while b"\n" in buffer:

            line_bytes, buffer = buffer.split(b"\n", 1)

            if current_line == line_no:

                return Response(
                    line_bytes.decode("utf-8", errors="replace"),
                    content_type="application/json; charset=utf-8"
                )

            current_line += 1

        current_byte += len(chunk)

    return Response("Line not found", status=404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
