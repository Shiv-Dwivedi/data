from flask import Flask, request, Response
import requests

app = Flask(__name__)
FILE_URL = "https://github.com/Shiv-Dwivedi/data/releases/download/v1/botsv1.stream_http.json"

@app.route("/line")
def line():
    line_no = request.args.get("line", 0, type=int)

    # fetch file in chunks and stop at the requested line
    chunk_size = 65536
    data = b""
    current = 0
    found_line = 0

    while True:
        headers = {"Range": f"bytes={current}-{current + chunk_size - 1}"}
        r = requests.get(FILE_URL, headers=headers)
        part = r.content
        if not part:
            break

        data += part

        while True:
            nl = data.find(b"\n")
            if nl == -1:
                break

            if found_line == line_no:
                return Response(
                    data[:nl].decode("utf-8", errors="replace"),
                    content_type="application/json; charset=utf-8",
                )

            data = data[nl + 1:]
            found_line += 1

        current += len(part)

    return Response("Line not found", status=404)
