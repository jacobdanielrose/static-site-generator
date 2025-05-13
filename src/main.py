import os
import shutil

def main():
    copy_dir, write_dir = os.path.join(os.getcwd(),"static"), os.path.join(os.getcwd(),"public")

    if os.path.exists(write_dir):
        shutil.rmtree(write_dir)
    os.mkdir(write_dir)
    copy_files(copy_dir, write_dir)


def copy_files(copy_dir, write_dir):
    paths = os.listdir(copy_dir)
    for path in paths:
        full_path = os.path.join(copy_dir, path)
        if os.path.isfile(full_path):
            print(f"Copying {full_path}")
            shutil.copy(full_path, write_dir)
        else:
            full_write_dir = os.path.join(write_dir, path)
            os.mkdir(full_write_dir)
            copy_files(full_path, full_write_dir)




if __name__ == "__main__":
    main()
