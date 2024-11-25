#!/usr/bin/python3

### Tasks ###

#    Test for domain registrar pages via page content and skip them.
#    Add line to input length of fuzzing and prefix/suffix/bothfix (both at the same time)/prefix-then-suffix (do both separately) mode as CLI parameters.
#    Some requests hang for too long, set a time limit for the requests.
#	 Seems like I'll need to make the character-adding feature a function rather than a loop, in order to implement variable length fuzzing
#!	 No need to provide character optionality... just fuzz numbers and letters altogether
# 	 python3 -c [fuzz length] -o [output filename] 
import requests

#!   import argparse
#!   parser = argparse.ArgumentParser(prog="DomFuzz",description="A domain fuzzer for discovering cryptic, hidden domains",epilog="Read the help dumbass")

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
tlds = ['.com', '.us', '.wtf','.org']
tlds_index = 3 #array length for fuzz()

domains = ["hack"]

new_word = ""

def send_request(domain, fd):
	header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0'}
	try:
		print(domain)
		request = requests.get(domain, timeout=0.5)
	except:
		return -1
	else: 
		if request.status_code == 200:
			fd.write(domain + '\n')
			print("\n############\n###FOUND!###\n############\n")

def fuzz(domain, iteration, index, tld_index):
	domain = "https://" + domain
	if iteration == 0:
		domain += alphabet[index]
	elif iteration == 1:
		domain += numbers[index]
	# Top Level Domain loop logic

	domain += tlds[tld_index]
	return domain

def main():
	fuzzcount = input("char # to fuzz: ")
	fuzzcount = int(fuzzcount)
	fd = open('fuzzed3', 'w')
	for domain in domains:
		while fuzzcount > 0:
			fuzzcount_int = fuzzcount
			i = 0
			print("Starting alphabet fuzzing...")
			while i < 26: #alphabet
				loop_tld_index = 0
				while loop_tld_index < 4:
					new_word = fuzz(domain, 0, i, loop_tld_index)
					if send_request(new_word, fd) == -1:
						print("Nope...")
					loop_tld_index += 1
				i += 1
			i = 0
			print("Starting number fuzzing...")
			while i < 10: #numbers
				loop_tld_index = 0
				while loop_tld_index < 4:
					new_word = fuzz(domain, 1, i, loop_tld_index)
					if send_request(new_word, fd) == -1:
						print("Nope...")
					loop_tld_index += 1 
				i += 1
			fuzzcount -= 1
	fd.close()

if __name__ == '__main__':
	main()


# Add https:// automatically to the beginning of the domain DONE
# TODO -- Work on trailing fuzzing first, then implement both. 
#^ Need to add variable length fuzzing.
