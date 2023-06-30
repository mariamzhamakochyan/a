from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

class FileSystem:
    def __init__(self):
        self.root_directory = {'/': 'directory'}
        self.current_directory = '/'
        self.command_history = []
        self.file_system = {}
        self.output = ''

    def run_command(self, command):
        self.command_history.append(command)
        parts = command.split(' ')
        command_name = parts[0]
        options = []
        arguments = []

        for part in parts[1:]:
            if part.startswith('-'):
                options.append(part)
            else:
                arguments.append(part)

        if command_name == 'cd':
            self.change_directory(arguments)
            return ''
        elif command_name == 'ls':
            self.list_directory(options)
            return self.output
        elif command_name == 'pwd':
            self.print_working_directory()
            return self.output
        elif command_name == 'history':
            self.print_command_history()
            return self.output
        elif command_name == 'mkdir':
            self.make_directory(arguments)
            return ''
        elif command_name == 'touch':
            self.create_file(arguments)
            return self.output
        elif command_name == 'exit':
            self.exit_terminal()
            return self.output
        else:
            self.output = f"Command not found: {command_name}"
            return self.output

        

    def change_directory(self, arguments):
        if len(arguments) == 0:
            self.current_directory = '/'
        elif len(arguments) > 0:
            directory = arguments[0]

            if directory == '/':
                self.current_directory = '/'
            elif directory == './':
                pass
            elif directory == '.':
                pass
            elif directory == '..' or directory == '../':
                parent_directory = self.get_parent_directory(self.current_directory)
                if parent_directory:
                    self.current_directory = parent_directory
                else:
                    self.output = "Cannot move up from the root directory."
            elif directory.startswith('../'):
                path = directory[3:]
                parent_directory = self.get_parent_directory(self.current_directory)
                if parent_directory:
                    target_directory = self.get_child_directory(parent_directory, path)
                    if target_directory is not None:
                        self.current_directory = target_directory
                    else:
                        self.output = f"Directory '{path}' does not exist."
                else:
                    self.output = "Cannot move up from the root directory."
            elif directory.startswith('./'):
                path = directory[2:]
                target_directory = self.get_child_directory(self.current_directory, path)
                if target_directory is not None:
                    self.current_directory = target_directory
                else:
                    self.output = f"Directory '{path}' does not exist."
            elif directory == '-':
                previous_directory = self.get_previous_directory()
                if previous_directory:
                    self.current_directory = previous_directory
                else:
                    self.output = "No previous directory available."
            else:
                target_directory = self.get_child_directory(self.current_directory, directory)
                if target_directory is not None:
                    self.current_directory = target_directory
                else:
                    self.output = f"Directory '{directory}' does not exist."

    def list_directory(self, options):
        output = ''

        for item in self.file_system.keys():
            if item.startswith(self.current_directory) and item != self.current_directory:
                if '/' not in item[len(self.current_directory):][1:]:
                    if '-l' in options:
                        item_type = self.file_system.get(item)
                        output += f"{item.split('/')[-1]}\t({item_type})\n"
                    else:
                        output += item.split('/')[-1] + '\n'

        self.output = output


    def print_working_directory(self):
        self.output = self.current_directory

    def print_command_history(self):
        output = ''
        for command in self.command_history:
            output += command + '\n'
        self.output = output

    def exit_terminal(self):
        self.output = "Exiting terminal..."

    def make_directory(self, arguments):
        if len(arguments) > 0:
            directory_name = arguments[0]
            directory_path = self.get_absolute_path(directory_name)
            if directory_path in self.file_system:
                self.output = f"Directory '{directory_name}' already exists."
            else:
                self.file_system[directory_path] = 'directory'
        else:
            self.output = "Usage: mkdir <directory>"

    def create_file(self, arguments):
        if len(arguments) > 0:
            file_name = arguments[0]
            file_path = self.get_absolute_path(file_name)
            if file_path in self.file_system:
                self.output = f"File '{file_name}' already exists."
            else:
                self.file_system[file_path] = 'file'
                self.output = f"File '{file_name}' created successfully."
        else:
            self.output = "Usage: touch <filename>"

    def get_absolute_path(self, path):
        if path.startswith('/'):
            return path

        absolute_path = self.current_directory
        if not absolute_path.endswith('/'):
            absolute_path += '/'

        absolute_path += path

        return absolute_path

    def get_child_directory(self, directory, child_name):
        if not directory.endswith('/'):
            directory += '/'

        child_directory = directory + child_name
        if child_directory in self.file_system and self.file_system[child_directory] == 'directory':
            return child_directory

    def get_parent_directory(self, directory):
        parent_directory = '/'.join(directory.split('/')[:-1])
        if parent_directory == '':
            parent_directory = '/'
        return parent_directory

    def get_previous_directory(self):
        if len(self.command_history) > 1:
            previous_command = self.command_history[-2]
            parts = previous_command.split(' ')
            if parts[0] == 'cd' and len(parts) > 1:
                return parts[1]
        return None


filesystem = FileSystem()

@app.route('/')
def index():
    return render_template("index.html")

@app.context_processor
def inject_time():
    def get_current_time():
        return datetime.datetime.now().strftime('%I:%M %p')
    return {'current_time': get_current_time}

@app.route('/terminal')
def terminal():
    return render_template("terminal.html")

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    output = filesystem.run_command(command)
    return jsonify(output=output)


if __name__ == '__main__':
    app.run(debug=True)
