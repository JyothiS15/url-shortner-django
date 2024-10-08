"""
List of tests to cover

#############################
# functional tests
#############################
1. Generate short URL for a valid URL input
2. Do not re-generate short URL if already generated
3. {hostname}/short_url should redirect to the original url



#############################
# non-functional tests
#############################
1. Check if API endpoint takes in value with invalid URL format
2. Check if UI takes in value with invalid URL format
3. Check if API takes in extra params, if yes, does it consume ?
4. Check if short URL is regenerated for different URL by running the function
1000 times.
5. Check if API input takes empty values and also check with giving urls of
2000 character long.

"""
