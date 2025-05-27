#!/usr/bin/env python

# from texttable import Texttable
import requests
from bs4 import BeautifulSoup as bs
from make_colors import make_colors
import sys, os
import traceback
import re
import argparse
try:
	from pydebugger.debug import debug
except:
	def debug(*args, **kwargs):
		return ''
# from makelist import makeList

def get_data_currencies(content):
    # html = bs_obj.prettify()
    # Pola untuk menangkap kode dan nama mata uang
    pattern = re.compile(
        r'<a href="/currency/([a-z]{3})-[^/]+/" class="[^"]*?">\s*<div[^>]*?>.*?</div>\s*<span class="currencyCode">([A-Z]{3})<!-- --> -</span>\s*<!-- -->\s*(.*?)</a>',
        re.DOTALL
    )

    currencies = []
    for match in pattern.finditer(content):
        slug_code = match.group(1).upper()
        code = match.group(2).upper()
        name = match.group(3).strip()
        currencies.append({
            "code": code,
            "name": name,
            "slug_code": slug_code,
        })

    return currencies

def currency():
	content = requests.get("https://www.xe.com/iso4217.php").content
	# b = bs(content, 'html.parser')
	data = get_data_currencies(content.decode())
	debug(data = data)
	# all_currentcy = b.find_all('td', {'class':"tblBrdrLn"})
	# debug(all_currentcy = all_currentcy)
	# data = {}
	# # table = Texttable()
	# # table.header(['CODE','NAME'])
	# # table.set_cols_align(["c", "c"])
	# # table.set_cols_width([10, 50])
	# for i in all_currentcy:
	# 	# debug(i = i)
	# 	if i.find('a'):
	# 		key = i.find('a').text.strip()
	# 		value = all_currentcy[all_currentcy.index(i) + 1].text
	# 		data.update({key:value})
	# 		# table.add_row([key, value])
	# # print(table.draw())
	# debug(data = data)
	# # makeList([[i, data.get(i)] for i in data], 2)
	return data

def convert(fr, to, data):
	url = 'https://www.google.com/finance/quote/{}-{}'.format(fr.upper(), to.upper())
	try:
		content = requests.get(url).content
	except Exception as e:
		print(make_colors("ERROR:", 'lc') + " " + make_colors(e, 'lw', 'r'))
		if os.getenv('DEBUG'):
			print(make_colors("ERROR FULL:", 'ly'))
			print(make_colors(traceback.format_exc(), 'lw', 'r'))
		sys.exit(e)
	
	b = bs(content, 'html.parser')
	base = b.find('div', {'class':'YMlKec fxKbKc'})
	debug(base = base)
	if base: 
		base = base.text
		debug(base = base)
		base0 = base
		base = re.sub(",", "", base)
		debug(base = base)
		base = float(base)
		debug(base = base)
		debug(data = data)
		base = base * float(data)
		debug(base = base)
		data = "{:,.2f}".format(base)
		debug(data = data)
		return data, base0
	return 0

def usage():
	parser = argparse.ArgumentParser()
	parser.add_argument('FROM', action = 'store', help = 'Convert From (code)', nargs='?')
	parser.add_argument('TO', action = 'store', help = 'Convert To (code)', nargs='?')
	parser.add_argument('NUMBER', action = 'store', help = 'Data Number to Convert to', nargs='?')
	parser.add_argument('-l', '--list', action = 'store_true', help = 'List currency Code')
	parser.add_argument('-f', '--find', action = 'store', help = 'Find currency Code')
	if len(sys.argv) == 1:
		parser.print_help()
	else:
		args = parser.parse_args()
		if args.list:
			data = currency()
			for i in data:
				print(make_colors(i.get('code'), 'lc') + " --> " + make_colors(i.get('name'), 'ly'))
		elif args.find:
			data = currency()
			found = []
			for i in data:
				if args.find.lower() in i.get('name').lower() or args.find.lower() in i.get('code').lower():
					found.append(i)
			if not found:
				print(make_colors("NOT FOUND:", 'lw', 'r') + " " + make_colors(args.find, 'lc'))
				sys.exit(1)
			debug(found = found)
			unique = list({tuple(d.items()) for d in found})
			result = [dict(t) for t in unique]
			debug(result = result)
			for i in result:
				print(make_colors(i.get('code'), 'lc') + " --> " + make_colors(i.get('name'), 'ly'))
		elif args.FROM and args.TO and args.NUMBER:
			data, base = convert(args.FROM, args.TO, args.NUMBER)
			print(make_colors(args.FROM.upper(), 'ly') + " [" + make_colors(base, 'lm') + "] " + make_colors('-->', 'lg') + " " + make_colors(args.TO.upper(), 'bl') + " :" + make_colors(args.TO.upper() + ". " + data, 'lw', 'r'))

if __name__ == '__main__':
	usage()
	# currency()

	# if len(sys.argv) == 1:
	# 	print(make_colors("USAGE:", 'ly') + " " + make_colors(os.path.basename(__file__)[-4:], 'lc') + " " + make_colors("FROM", 'lc') + " " + make_colors("TO", 'lm') + " " + make_colors("DATA", 'lw', 'bl'))
	# 	print(make_colors("EXAMPLE:", 'lc') + " " +\
	# 	make_colors(os.path.basename(__file__)[-4:], 'lc') + " " + make_colors("USD", 'lc') + " " + make_colors("IDR", 'lm') + " " + make_colors("4000", 'lw', 'bl'))
	# else:
	# 	args = sys.argv[1:]
	# 	debug(args = args)
	# 	if '-l' in args or '--list' in args:
	# 		try:
	# 			args.remove('-l')
	# 		except:
	# 			pass
	# 		try:
	# 			args.remove('--list')
	# 		except:
	# 			pass
	# 		data = currency()
	# 		for i in data.keys():
	# 			print(make_colors(i, 'lc') + " --> " + make_colors(data.get(i), 'ly'))
	# 	debug(args = args)
	# 	if len(args) > 0:
	# 		convert(*args)

