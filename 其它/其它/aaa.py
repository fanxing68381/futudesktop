import os

def modify_ek_key_lines(directory_path="D:\\Software\\KeymouseGo_v5_1_1-win\\scripts", filename="aaa1.txt"):
  """
  Reads a file, replaces the beginning of specific lines containing '"EK","key"',
  and prints all lines, preserving original newlines and blank lines.

  Args:
      directory_path (str, optional): The directory containing the file.
                                     Defaults to "D:\\Software\\KeymouseGo_v5_1_1-win\\scripts".
      filename (str, optional): The name of the file to process. Defaults to "aaa1.txt".

  Returns:
      None: Prints the modified content to the console.
  """

  file_path = os.path.join(directory_path, filename)

  try:
    with open(file_path, "r") as file:
      lines = file.readlines()
  except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    return

  modified_lines = []
  for line in lines:
    if '"EK","key' in line:
      modified_line = '[100,' + line[line.find('"EK","key'):]
      modified_lines.append(modified_line)
    else:
      modified_lines.append(line)

  for modified_line in modified_lines:
    print(modified_line, end='')

# Call the function to process the file
modify_ek_key_lines()