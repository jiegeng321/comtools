#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
from encrypter import AEScoder


def encrypt(origin, output=""):
    if not output:
        output = origin + ".encrypted"
    encrypter = AEScoder()
    with open(origin, "rb") as f:
        encrypted_data = encrypter.encrypt(f.read())
    with open(output, "wb") as f:
        f.write(encrypted_data)
    return output


def test():
    import pickle
    import io
    data = {"key1": "value1", "key2": "value2"}
    with open("model.pb", "wb") as f:
        pickle.dump(data, f, 1)
    ef = encrypt("model.pb")
    with open(ef, "rb") as f:
        decrypter = AEScoder()
        d = pickle.load(io.BytesIO(decrypter.decrypt(f.read())))
        print(d)


if __name__ == "__main__":
    # test()
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="file need to encrypt")
    parser.add_argument("-o", "--output", help="path of output encrypted file")
    args = parser.parse_args()
    if args.output:
        output = args.output
    else:
        output = args.source + ".encrypted"
    d = encrypt(args.source, output)
    print("encrypt file to > " + d)
