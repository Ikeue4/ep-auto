def read_OTO(file_path):
    lines_un = {}
    lines_link = {}
    with open(file_path, 'r', encoding="utf-16") as file:
        for line in file:
            line_data = line.strip().split('⑄')
            line_id, content, linked_line_id = line_data
            lines_un[line_id] = (content, linked_line_id)
            lines_link[line_id] = 
    return lines_un

def write_OTO(file_path, lines_data):
    with open(file_path, 'w', encoding="utf-16") as file:
        for line_id, (content, linked_line_id) in lines_data.items():
            file.write(f"{line_id}⑄{content}⑄{linked_line_id}\n")

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
write_OTO(file_path, lines_data)
print(read_OTO(file_path))