#!/usr/bin/env python3

import os
import re

def list_files(dn):
    todo = [([], dn)]
    while len(todo) > 0:
        stack, dn = todo.pop(0)
        for cur in sorted(os.listdir(dn)):
            cur_fn = os.path.join(dn, cur)
            if os.path.isdir(cur_fn):
                use = True
                if cur in {".venv"}:
                    use = False
                if "/".join(stack + [cur]) in {"main_page/aoc", "main_page/screenshots", "animations"}:
                    use = False
                if use:
                    todo.append((stack + [cur], cur_fn))
            else:
                use = True
                if re.search("^day_[0-9]{2}", cur):
                    use = False
                if len(stack) > 0 and stack[0] == "main_page" and re.search("\\.(exe|png|ttf|css|js|mp4)$", cur):
                    use = False
                if use:
                    yield stack + [cur]

def main():
    for cur in sorted(os.listdir(".")):
        if re.search("^[0-9]{4}$", cur):
            year = cur
    
    next_year = f"{int(year)+1}"
    yn = input(f"This will make {next_year} from {year}, do you want to continue? [y/n] ")
    if yn.lower() != "y":
        exit(0)

    for cur in list_files(year):
        fix_year = False
        if "/".join(cur) in {"advent_year.py", "README.md", "URL.txt", "example.txt"}:
            fix_year = True
        print(f"Copy: {year} -> {next_year}: " + "/".join(cur))
        source_fn = os.path.join(*([year] + cur))
        dest_fn = os.path.join(*([next_year] + cur))
        dest_dir = os.path.join(*([next_year] + cur[:-1]))
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        with open(source_fn, "rb") as f_src:
            data = f_src.read()
        if fix_year:
            data = data.replace(year.encode("utf-8"), next_year.encode("utf-8"))
        with open(dest_fn, "wb") as f_dest:
            f_dest.write(data)

    print("")
    print("Need to update images for README.md, and get cookie for current year!")


if __name__ == "__main__":
    main()