# To use Gitpython:
# pip install gitpython

import sys
from git import Repo

def main():
	
	# Receive argument
	textFile = sys.argv[1]

	# Open file	
	inFile = open(textFile, 'r')
	
	# Read and display text 
	text = inFile.readline()
	while text != '':
		text = text.rstrip('\n')
		print(text)
		text = inFile.readline()
	inFile.close()

	# Push and commit to GitHub
	repo = Repo('.git')
	file_list = [textFile] # Text file location
	commit_message = 'Test push'
	repo.index.add(file_list)
	repo.index.commit(commit_message)
	origin = repo.remote('origin')
	origin.push()

	# I need to figure out a way to automatically push without prompting for user/pass

main()





