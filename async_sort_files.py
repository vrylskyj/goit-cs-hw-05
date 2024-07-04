import asyncio
import aiofiles
import os
import argparse

async def read_folder(source_folder, target_folder):
    try:
        async for root, _, files in aiofiles.os.walk(source_folder):
            for file_name in files:
                source_path = os.path.join(root, file_name)
                await copy_file(source_path, target_folder)
    except Exception as e:
        print(f"Error while reading folder: {e}")

async def copy_file(source_path, target_folder):
    try:
        _, ext = os.path.splitext(source_path)
        extension = ext[1:]  # Видаляємо крапку з початку розширення

        target_subfolder = os.path.join(target_folder, extension)
        os.makedirs(target_subfolder, exist_ok=True)

        target_path = os.path.join(target_subfolder, os.path.basename(source_path))

        async with aiofiles.open(source_path, 'rb') as source_file, aiofiles.open(target_path, 'wb') as target_file:
            contents = await source_file.read()
            await target_file.write(contents)
    except Exception as e:
        print(f"Error while copying file {source_path}: {e}")

async def main(source_folder, target_folder):
    await read_folder(source_folder, target_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async file sorting script")
    parser.add_argument("source_folder", type=str, help="Source folder to read files from")
    parser.add_argument("target_folder", type=str, help="Target folder to save sorted files")

    args = parser.parse_args()

    source_folder = args.source_folder
    target_folder = args.target_folder

    asyncio.run(main(source_folder, target_folder))
