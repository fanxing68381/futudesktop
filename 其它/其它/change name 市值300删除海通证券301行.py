import os
import re


def update_batch_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "change name 市值300.bat":
                file_path = os.path.join(dirpath, filename)
                try:
                    # Read the file content with GBK encoding
                    with open(file_path, 'r', encoding='gbk') as f:
                        lines = f.readlines()

                    # Process the lines
                    updated_lines = []
                    for line in lines:
                        # Skip the line containing "海通证券"
                        if "海通证券" in line:
                            continue

                        # Match the line pattern
                        match = re.match(r'ren (\d{4}-\d{2}-\d{2})_(\$\d+)\.png (.+)_(\d+)_(\d{4}-\d{2}-\d{2})\.png',
                                         line.strip())
                        if match:
                            date = match.group(1)
                            seq_num_str = match.group(2)
                            company_name = match.group(3)
                            seq_num = int(match.group(4))
                            end_date = match.group(5)

                            # Verify date consistency
                            if date != end_date:
                                print(f"Warning: Date mismatch in {file_path}: {line.strip()}")
                                updated_lines.append(line)
                                continue

                            # Adjust sequence number for lines with $120 and above
                            if seq_num >= 120:
                                new_seq_num = seq_num - 1
                                new_line = f"ren {date}_${new_seq_num}.png {company_name}_{new_seq_num}_{date}.png\n"
                                updated_lines.append(new_line)
                            else:
                                updated_lines.append(line)
                        else:
                            # Keep non-matching lines unchanged
                            updated_lines.append(line)

                    # Write back to the file with GBK encoding
                    with open(file_path, 'w', encoding='gbk') as f:
                        f.writelines(updated_lines)
                    print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")


# Specify the root directory
root_directory = r"E:\图片\市值300资金历史记录\a"
update_batch_files(root_directory)