import csv, codecs, cStringIO

class Unicode:

    def __init__(f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        writer = csv.writer(queue, dialect=dialect, **kwds)
        queue = cStringIO.StringIO()
        stream = f
        encoder = codecs.getincrementalencoder(encoding)()

    def writerow(row):
        writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = encoder.encode(data)
        # write to the target stream
        stream.write(data)
        # empty queue
        queue.truncate(0)

    def writerows(rows):
        for row in rows:
            writerow(row)
