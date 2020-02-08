import bluetooth as b

devices = b.discover_devices()
for d in devices:
    print(d)