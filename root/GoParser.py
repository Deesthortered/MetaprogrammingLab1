import os


class GoParser:
    # Global

    def start_folder(self, input_folder_path, destination_folder_path):
        # print(os.listdir(input_folder))
        pass

    def start_file(self, input_file_path, destination_file_path):
        input_file = open(input_file_path, encoding='utf-8', mode='r')
        self.parse_file(input_file)

        input_file.close()
        pass

    # Local
    def parse_file(self, file):
        # Result
        result_set = []

        # clear start empty lines
        lines = file.readlines()
        while lines[0].rstrip() == "":
            lines = lines[1:]

        comment_queue = []
        was_begin = True

        for i in range(len(lines)):
            dirty_line = lines[i]
            line = dirty_line.strip()

            if self.line_is_comment(line):
                comment_queue.append(self.strip_comment_line(line))
            elif self.line_is_long_comment(line):
                if line != "/*" and line != "*/":
                    comment_queue.append(line)
            else:
                if was_begin and line == "":
                    result_set.append(("File overview", comment_queue))
                    comment_queue = []
                    continue
                if line != "":
                    was_begin = False

                if self.first_word(line) == "func":
                    result_set.append(("function", line[:-2], comment_queue))
                elif self.first_word(line) == "package":
                    result_set.append(("package", line, comment_queue))

                comment_queue = []

        for i in result_set:
            print(i)

    def line_is_comment(self, line):
        return len(line) >= 2 and line[0] == line[1] == '/'

    long_comment_memory = False
    def line_is_long_comment(self, line):
        if line == "/*":
            self.long_comment_memory = True
            return True
        elif line == "*/":
            self.long_comment_memory = False
            return True
        return self.long_comment_memory

    def strip_comment_line(self, line):
        if len(line) < 3:
            return ""
        elif line[2] == " ":
            return line[3:]
        return line[2:]

    def first_word(self, line):
        return line.split(' ', 1)[0]
