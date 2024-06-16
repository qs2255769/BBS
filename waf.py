import requests
import argparse
import random
import time

# Define a banner for the tool
banner = """
############################################
#       WAF Detection Tool by Muhammad Qasim
#       Test HTML tags against WAF
############################################
"""

# Define a list of common user agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
]

# Define HTML tags to test
# List of HTML tags to test
html_tags = [
    '<', '>', '</>', '<a>', '<abbr>', '<address>', '<area>', '<article>', '<aside>', '<audio>', '<b>', '<base>', '<bdi>', '<bdo>', '<blockquote>',
    '<body>', '<br>', '<button>', '<canvas>', '<caption>', '<cite>', '<code>', '<col>', '<colgroup>', '<data>', '<datalist>', '<dd>', '<del>',
    '<details>', '<dfn>', '<dialog>', '<div>', '<dl>', '<dt>', '<em>', '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<footer>', '<form>',
    '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<hr>', '<html>', '<i>', '<iframe>', '<img>', '<input>', '<ins>',
    '<kbd>', '<label>', '<legend>', '<li>', '<link>', '<main>', '<map>', '<mark>', '<menu>', '<meta>', '<meter>', '<nav>', '<noscript>', '<object>',
    '<ol>', '<optgroup>', '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>',
    '<samp>', '<script>', '<section>', '<select>', '<slot>', '<small>', '<source>', '<span>', '<strong>', '<style>', '<sub>', '<summary>', '<sup>',
    '<svg>', '<table>', '<tbody>', '<td>', '<template>', '<textarea>', '<tfoot>', '<th>', '<thead>', '<time>', '<title>', '<tr>', '<track>', '<u>',
    '<ul>', '<var>', '<video>', '<wbr>'
    


]

# Function to test payloads against the URL
def test_payloads(url, payloads, proxies=None):
    for payload in payloads:
        complete_url = f"{url}{payload}"
        headers = {'User-Agent': random.choice(user_agents)}
        
        # Try without proxy first
        try:
            response = requests.get(complete_url, headers=headers)
            content_length = len(response.content)
            
            if response.status_code == 200:
                print(f"Payload: {payload} | No Proxy | Length: {content_length} - \033[92mAllowed\033[0m (Green)")
            else:
                print(f"Payload: {payload} | No Proxy | Length: {content_length} - \033[91mBlocked\033[0m (Red)")
            
            time.sleep(2)
            continue  # Skip to the next payload if the request was successful

        except requests.exceptions.RequestException as e:
            print(f"Error testing payload {payload} without proxy: {e}")
        
        # Try with proxies if no proxy fails or gets blocked and proxies are provided
        if proxies:
            for proxy in proxies:
                try:
                    response = requests.get(complete_url, headers=headers, proxies=proxy)
                    content_length = len(response.content)
                    
                    if response.status_code == 200:
                        print(f"Payload: {payload} | Proxy: {proxy['http']} | Length: {content_length} - \033[92mAllowed\033[0m (Green)")
                    else:
                        print(f"Payload: {payload} | Proxy: {proxy['http']} | Length: {content_length} - \033[91mBlocked\033[0m (Red)")
                    
                    time.sleep(2)
                    break  # Exit proxy loop if request was successful
                    
                except requests.exceptions.RequestException as e:
                    print(f"Error testing payload {payload} with proxy {proxy['http']}: {e}")
                    continue  # Try the next proxy if request failed

def main():
    parser = argparse.ArgumentParser(description="Test WAF with various HTML tags and payloads.")
    parser.add_argument("-u", "--url", required=True, help="URL to test.")
    parser.add_argument("-p", "--payloads", help="Path to file with custom payloads.")
    parser.add_argument("-pp", "--proxies", help="Path to file with proxy list.")
    
    args = parser.parse_args()
    
    url = args.url
    payloads = html_tags
    proxies = None
    
    if args.payloads:
        try:
            with open(args.payloads, 'r') as file:
                payloads = file.read().splitlines()
        except Exception as e:
            print(f"Error reading payloads file: {e}")
            return
    
    if args.proxies:
        try:
            with open(args.proxies, 'r') as file:
                proxy_list = file.read().splitlines()
                proxies = [{"http": proxy, "https": proxy} for proxy in proxy_list]
        except Exception as e:
            print(f"Error reading proxies file: {e}")
            return
    
    print(banner)
    test_payloads(url, payloads, proxies)

if __name__ == "__main__":
    main()