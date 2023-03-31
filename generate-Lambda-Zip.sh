#!/bin/bash

if [[ ${PWD##*/} != Generate-McDonalds-Mobile-Screenshot ]]; then
	echo "This script can only be run in a directory named Generate-McDonalds-Mobile-Screenshot"
	exit
fi



zip_exceptions=("example_screenshot.jpg" "README.md" "generate-Lambda-Zip.sh" "requirements.txt")
delete_exceptions=("resources" "example_screenshot.jpg" "lambda_function.py" "mcd_generate.py" "README.md" "requirements.txt" "generate-Lambda-Zip.sh" "archive.zip")

pip3 install -r requirements.txt -t .

# loop through all files in the current directory
for file in *; do
	# check if the file is in the zip_exceptions array
	if [[ ! " ${zip_exceptions[@]} " =~ " ${file} " ]]; then
		# add the file to the zip archive
		zip -r archive.zip "$file"
	fi
done

# Loop through all files and folders in the current directory
for item in *; do
	# Check if the item is not in the exceptions array
	if [[ ! " ${delete_exceptions[@]} " =~ " ${item} " ]]; then
		# Delete the item with -f option to force and -r option to recurse
		rm -rf "$item"
	fi
done  
