import json
import facebook

def main():
	token = "FACEBOOK_temp_token"
	graph = facebook.GraphAPI(token)
	page_name = input("Enter a page name: ")
	
	# list of required fields
	fields = ['id','name','about','likes','link','band_members']
	
	fields = ','.join(fields)
	
	page = graph.get_object(page_name, fields=fields)
		
	print(json.dumps(page,indent=4))

if __name__ == '__main__':
	main()