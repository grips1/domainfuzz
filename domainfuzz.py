#!/usr/bin/python3

#domain fuzzer
#keywords = cyber, sploit, 0day, l33t
#test it with 1 chracter of ?a and ?d "cybera, cyberb, cyber1, etc." DONE
#need to find python summary file with syntax
#check for "domain for sale" false positives
#requests.get throws an error if the protocol specified doesn't exist (http(s))
import requests

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
keywords = ["https://books", "https://audiobooks", "https://audio", "https://book", "https://epub"]
new_word = "temp"

def send_request(domain, fd):
	header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:128.0) Gecko/20100101 Firefox/128.0'}
	try:
		print(domain)
		request = requests.get(domain)
	except:
		return -1
	else: 
		if request.status_code == 200:
			fd.write(domain + '\n')
			print("############\n###FOUND!###\n############")

def concatenate(domain, iteration, index):
	if iteration == 1:
		domain += alphabet[index]
	elif iteration == 2:
		domain += numbers[index]
	
	domain += ".com"
	return domain
#to implement more than one ?l, I could nest the for loop twice, but then how do I add even more ?l's? Cant have a loop for each letter

def main():
	fd = open('fuzzed3', 'w')
	for word in keywords:
		i = 0
		while i < 26: #alphabet
			new_word = concatenate(word, 1, i)
			if send_request(new_word, fd) == -1:
				print("Not found!")
			i += 1
		i = 0
		while i < 10: #numbers
			new_word = concatenate(word, 2, i)
			if send_request(new_word, fd) == -1:
				print("NOT FOUND!")
			i += 1

	fd.close()

if __name__ == '__main__':
	main()

"""		while i < 10: #numbers
			send_request(new_word)
			i += 1
"""

#somewhere down the line, need to have: fd.close()
