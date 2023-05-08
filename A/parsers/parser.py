class ParserAPI:
    def __init__(self):
        super().__init__()
        self.parsers = {}
        self.active_parsers = {}
        self.data = None
        self.batch_size = 150000

    def register_parser(self, file_type, parser, name):
        if file_type not in self.parsers:
            self.parsers[file_type] = {}
        self.parsers[file_type][name] = parser

        # Set the first registered parser for a file type as the active parser by default
        if file_type not in self.active_parsers:
            self.set_active_parser(file_type, name)

    def set_active_parser(self, file_type, name):
        if file_type not in self.parsers or name not in self.parsers[file_type]:
            raise ValueError(f"No parser with name '{name}' registered for file type: {file_type}")

        self.active_parsers[file_type] = self.parsers[file_type][name]

    def parse_file(self, file_path):
        file_type = self.get_file_type(file_path)

        if file_type not in self.active_parsers:
            raise ValueError(f"No active parser set for file type: {file_type}")

        parser = self.active_parsers[file_type]
        self.data = parser.parse(file_path, self.batch_size)
        return self.data

    def set_batch_size(self, batch_size):
        self.batch_size = batch_size

    @staticmethod
    def get_file_type(file_path):
        return file_path.split('.')[-1].lower()
