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
        line_mapping = {}
        for line in file:
            line = line.rstrip()

            parts = line.split(':')
            line_num = int(parts[0][4:])
            text = parts[1]
            linked_line_num = int(parts[2][4:])
            line_mapping[line_num] = (text, linked_line_num)

            for line_num, (text, linked_line_num) in line_mapping.items():
                linked_text, _ = line_mapping[linked_line_num]
                link = f'<a href="#line{linked_line_num}">{linked_text}</a>'
                print(f'line{line_num}:{text}:{link}')

# Example usage:
file_path = 'OTOV3/custom_file.OTO'
lines_data = {
    'line1': ('This is line one', 'line4'),
    'line2': ('This is line two', 'line5'),
    'line3': ('This is line three', 'line6'),
    'line4': ('This is line four', 'line1'),
    'line5': ('This is line five', 'line2'),
    'line6': ('This is line six', 'line3'),
}

link_read_OTO(file_path)