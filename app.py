from flask import Flask, request, Response
import requests

app = Flask(__name__)

FILE_URL = "https://github.com/Shiv-Dwivedi/data/releases/download/v1/botsv1.stream_http.json"

@app.route("/line")
def read_line():
    offset = request.args.get("offset", 0, type=int)

    # read in chunks until we find a newline
    chunk_size = 65536
    data = b""
    current = offset

    while True:
        headers = {"Range": f"bytes={current}-{current + chunk_size - 1}"}
        r = requests.get(FILE_URL, headers=headers)

        if r.status_code not in (200, 206):
            return Response("Failed to fetch file", status=500)

        part = r.content
        if not part:
            break

        data += part

        nl = data.find(b"\n")
        if nl != -1:
            line = data[:nl]   # only up to end of that line
            return Response(line.decode("utf-8", errors="replace"),
                            content_type="application/json; charset=utf-8")

        current += len(part)

    return Response(data.decode("utf-8", errors="replace"),
                    content_type="application/json; charset=utf-8")
