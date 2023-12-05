import zlib
import zipfile
import shutil
import os
import sys
import time

def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size

def generate_dummy_file(filename, size):
    with open(filename, 'w') as dummy:
        for _ in range(1024):
            dummy.write((size * 1024 * 1024) * '0')

def get_filename_without_extension(name):
    return name[:name.rfind('.')]

def get_extension(name):
    return name[name.rfind('.') + 1:]

def compress_file(infile, outfile):
    zf = zipfile.ZipFile(outfile, mode='x', allowZip64=True)
    zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()

def make_copies_and_compress(infile, outfile, n_copies):
    zf = zipfile.ZipFile(outfile, mode='x', allowZip64=True)
    for i in range(n_copies):
        f_name = f'{get_filename_without_extension(infile)}-{i}.{get_extension(infile)}'
        shutil.copy(infile, f_name)
        zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(f_name)
    zf.close()

if __name__ == '__main__':
    n_levels = int(sys.argv[1])
    out_zip_file = sys.argv[2]
    dummy_name = 'dummy.txt'
    start_time = time.time()
    generate_dummy_file(dummy_name, 1)
    level_1_zip = '1.zip'
    compress_file(dummy_name, level_1_zip)
    os.remove(dummy_name)
    decompressed_size = 1
    for i in range(1, n_levels + 1):
        make_copies_and_compress(f'{i}.zip', f'{i + 1}.zip', 10)
        decompressed_size *= 10
        os.remove(f'{i}.zip')
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename(f'{n_levels + 1}.zip', out_zip_file)
    end_time = time.time()
    print(f'Compressed File Size: {get_file_size(out_zip_file) / 1024.0:.2f} KB')
    print(f'Size After Decompression: {decompressed_size} GB')
    print(f'Generation Time: {end_time - start_time:.2f}s')
