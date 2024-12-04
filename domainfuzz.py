#!/usr/bin/python3

### Tasks ###
#@ Add https:// automatically to the beginning of the domain DONE
#@    Some requests hang for too long, set a time limit for the requests. DONE
# Where do I take this? Maybe I can just use a crunch-generated wordlist, add https:// and a .TLD and be done with it? 

#    HIGHEST PRIORITY: Add line to input length of fuzzing and prefix/suffix/bothfix (both at the same time)/prefix-then-suffix (do both separately) mode as CLI parameters.
	# HC's implementation of brute forcing is of a fixed length by default. ?l?l?l?l doesn't increment by itself, but rather uses the `--increment` flag. Assume a fixed length given by the user and implement --increment in the future...
#    Test for domain registrar pages via page content and skip them. (Implement scraping, can use Web Scraping with Python for reference)
#	 Seems like I'll need to make the character-adding feature a function rather than a loop, in order to implement variable length fuzzing
# 	 Designed python3 -c [fuzz length] -o [output filename] [SCAN FOR PORTS? SCAN FOR VULNS? SCRAPE?]
#	 Add vuln/port scanning with nmap/msf or should it be up to the user?

import requests

#!   import argparse
#!   parser = argparse.ArgumentParser(prog="DomFuzz",description="A domain fuzzer for discovering cryptic, hidden domains",epilog="Read the help dumbass")

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
tlds = ['.com', '.us', '.wtf']

domain_keywords = ["hack", "game"]

new_word = ""

#def send_request(domain, fd):
def send_request(domain, tld_index):
	header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0'}
	try:
		domain = "https://" + domain + tlds[tld_index]
		print("TRYING:" + domain )
		#0.2s for testing; increase later
		request = requests.get(domain, timeout=0.2)
	except:
		print("\n~~~Doesn't Exist~~~\n")
		return -1
	else: 
		if request.status_code == 200:
			#fd.write(domain + '\n')
			print("\n############\n###FOUND!###\n############\n")
		else:
			print("\n\n!!!NONE-200!!! --> " + str(request.status_code) + "\n\n")

def fuzz(domain, charset_identifier, recurse, tld_index):
	if charset_identifier == 0:
		for index in range(len(alphabet)):
			temp_domain = domain + alphabet[index]
			for rec in range(recurse):
				recurse -= 1
				fuzz(temp_domain, charset_identifier, recurse, tld_index)
			send_request(temp_domain, tld_index)

	elif charset_identifier == 0:
		for index in range(len(numbers)):
			temp_domain = domain + numbers[index]
			for rec in range(recurse):
				recurse -= 1
				fuzz(temp_domain, charset_identifier, recurse, tld_index) 
			send_request(temp_domain, tld_index)

def main():
	recursion_count = input("Recursion count: ")
	recursion_count = int(recursion_count)

	for domain in domain_keywords:
		print("Starting alphabet fuzzing...")
		loop_tld_index = 0
		while loop_tld_index < len(tlds):
			new_word = fuzz(domain, 0, recursion_count, loop_tld_index)
			loop_tld_index += 1

		print("Starting number fuzzing...")
		loop_tld_index = 0
		while loop_tld_index < len(tlds):
			new_word = fuzz(domain, 1, recursion_count, loop_tld_index)
			loop_tld_index += 1 
		print("\n\nFINISHED FOR KEYWORD " + domain + "!!!\n\n")
	print("Finished scanning all given domains!")

if __name__ == '__main__':
	main()


# TODO -- Work on trailing fuzzing first, then implement both. Implement ?l - ?l?l?l first, 
#^ Need to add variable length fuzzing.
