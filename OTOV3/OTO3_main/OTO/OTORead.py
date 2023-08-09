def read_OTO(file_path):
    lines = {}
    with open(file_path, 'r') as file:
        for line in file:
            line_data = line.strip().split(':')
            line_id, content, linked_line_id = line_data
            lines[line_id] = (content, linked_line_id)
    return lines

def write_OTO(file_path, lines_data):
    with open(file_path, 'w') as file:
        for line_id, (content, linked_line_id) in lines_data.items():
            file.write(f"{line_id}:{content}:{linked_line_id}\n")
            
def link_read_OTO(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            print(line)
            
def add_numbers(a, b):
    return a + b