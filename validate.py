
def validate_name(name):
	try:
		
		if name =='':
			return ['invalid name( cannot be empty )']
		for i in name:
			
			if not i.isalpha() and i != ' ':
				return ['invalid name( must only contain alphabet )']
		fname = ''
		for x in name.split():
			fname = fname +' '+ x.strip().lower().capitalize()
			
		return ['0', fname.strip()]
		
	except:
		return '2'
	
def validate_address(address):
	try:
		faddress = ''
		address = address.strip()
		if address =='':
			return ['invalid address( cannot be empty )']
		
		if len(address) > 120:
			return ['invalid address( maximum 120 character)'] 	
		for x in address.split('\n'):
			faddress = faddress + ',' + x.strip()
		return ['0', faddress.strip()]
		
	except:
		return '2'

def validate_phone(phone):
	try:
		
		phone = phone.strip()
		for i in phone:
			if not i.isdigit():
				return ['invalid number( only digits )'] 
		if len(phone) !=10:
			return ['invalid number( 10 digits )']
	

		return ['0', phone.strip()]
		
	except:
		return '2'

def validate_email(eid):
	try:
		
		eid = eid.strip()

		if len(eid) >= 70:
			return ['invalid email id( only 70 characters )']
	
		if   not (len(eid.split('@')) == 2 and len(eid.split('@')[1].split('.') )== 2 and len(eid.split(' ')) == 1):
			return ['invalid email id (in format "abc@xyz.com")']
		return ['0', eid.strip()]
		
	except:
		return '2'
print(validate_email("abc@x yz.com"))


