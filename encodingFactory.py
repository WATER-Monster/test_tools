encode_set = {
    "utf-8",
    "gbk"
}


class EncodingFactory:
    @staticmethod
    def file_reader(file_path):
        for encode in encode_set:
            try:
                with open(file_path ,"r",encoding=encode) as f:
                    ret = f.read()
                    return ret
            except UnicodeDecodeError:
                continue
        else:
            raise Exception("don't support this type of encoding")
