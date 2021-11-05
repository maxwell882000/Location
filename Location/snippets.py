import uuid


def name_of_file(instance, filename):
    return "media/{folder}/{random}_{filename}".format(folder=instance.folder,
                                                       filename=filename,
                                                       random=uuid.uuid1())
