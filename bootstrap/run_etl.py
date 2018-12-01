import os


THRESHOLD = 10
TEMP_PATH = 'temp'


if not os.path.exists(TEMP_PATH):
    os.makedirs(TEMP_PATH)


def main():

    with open('input/test_warc.txt') as fp:
        data = fp.readlines()

    tout = []
    for i, line in enumerate(data):
        tout.append(line)

        if (i + 1) % THRESHOLD == 0:
            with open(TEMP_PATH + '/t{0}'.format(i), 'w') as file_handler:
                for item in tout:
                    file_handler.write("{}\n".format(item))

        elif i == len(data) - 1:
            with open(TEMP_PATH + '/t{0}'.format(i), 'w') as file_handler:
                for item in tout:
                    file_handler.write("{}\n".format(item))


if __name__ == "__main__":
    main()
