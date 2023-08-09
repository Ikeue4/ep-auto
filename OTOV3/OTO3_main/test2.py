from OTO import OTORead

file_path = 'OTOV3/custom_file.OTO'
lines_data = {
    'line1': ('This is line one', 'line4'),
    'line2': ('This is line two', 'line5'),
    'line3': ('This is line three', 'line6'),
    'line4': ('This is line four', 'line1'),
    'line5': ('This is line five', 'line2'),
    'line6': ('This is line six', 'line3'),
}

OTORead.write_OTO(file_path, lines_data)
read_data = OTORead.read_OTO(file_path)
print(read_data)