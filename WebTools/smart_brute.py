'''
This script was developed from example of brute forcing phpmyadmin site to assisst in developing similar Tools for self
assessment of own web applications

#POST1

Cookie: phpMyAdmin=bde288434629d8f3e69b26d107633223


set_session=bde288434629d8f3e69b26d107633223&pma_username=ok&pma_password=okasd&server=1&target=index.php&lang=en&debug=0&token=a3809bbcae52f70e6beeef86b20ff414


# Resp1


Set-Cookie: phpMyAdmin=bde288434629d8f3e69b26d107633223; path=/
Set-Cookie: phpMyAdmin=51094657b2bc41758bccb0c61d6d6da1; path=/


   <input type="hidden" name="token" value="b6827a7ae7418c42e289d9213a75c482">


# POST 2



Cookie: phpMyAdmin=51094657b2bc41758bccb0c61d6d6da1


set_session=51094657b2bc41758bccb0c61d6d6da1&pma_username=sdfg&pma_password=sdfgdfgsdfg&server=1&target=index.php&lang=en&debug=0&token=b6827a7ae7418c42e289d9213a75c482


#######

So need to write a python program that does following:

1. grabs from every response the token from html body 
AND second cookie which is not equal to the cookie from initial GET or POST request

2. make a POST request with

set_session=CURRENT_COOKIE&pma_username=root&pma_password=PASS_LIST&server=1&target=index.php&lang=en&debug=0&token=FORM_TOKEN

3. evaluate to not have "Login Failed" in reposnse body
'''

import requests
import re
#import base64
import sys

URL = sys.argv[1]
USER_FILE = sys.argv[2]
PASS_FILE = sys.argv[3]

def main():

    print(f"Bruting for {URL}\n with users in {USER_FILE}\n and passwords in {PASS_FILE}")

    return 0


if __name__ == "__main__":
    main()