from dateutil import parser


def timestamp(data):
    date = parser.parse(data['created_at'])
    stamp = date.isoformat()
    return {'@timestamp': stamp}
