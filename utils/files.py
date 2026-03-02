
def join_path(elems, filename):
    elems.append(filename)
    all_together = "/".join(elems)
    folders = all_together.split("/")
    final_directory = []
    for folder in folders:
        slug_folder = folder.strip().replace(" ", "_")
        if slug_folder not in final_directory:
            final_directory.append(slug_folder)
    return "/".join(final_directory)


def join_path_simple(elems, filename):
    elems.append(filename)
    all_together = "/".join(elems)
    folders = all_together.split("/")
    return "/".join(folders)
