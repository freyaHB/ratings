def read_field_length(filename):

    my_file = open(filename)

    max_title = 0 
    max_imdb = 0 

    for line in my_file:
        if "|" in line:
            line = line.split("|")
        else:
            line = line.split()

        title = line[1]
        url = line[4]

        if len(title) > max_title:
            max_title = len(title)
        if len(url) > max_imdb:
            max_imdb = len(url)

    return max_title, max_imdb
