import re
import logging
from urllib.parse import urlparse

def extract_features(url):
    """Extract 23 features from URL for phishing detection"""
    features = {}
    
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        path = parsed_url.path
        full_url = url
        
        features['length_url'] = len(full_url)
        features['length_hostname'] = len(hostname)
        
        ip_pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
        features['ip'] = 1 if re.search(ip_pattern, hostname) else 0
        
        features['nb_dots'] = full_url.count('.')
        features['nb_qm'] = full_url.count('?')
        features['nb_eq'] = full_url.count('=')
        features['nb_slash'] = full_url.count('/')
        features['nb_www'] = 1 if 'www' in hostname.lower() else 0
        
        digits_in_url = sum(c.isdigit() for c in full_url)
        features['ratio_digits_url'] = digits_in_url / len(full_url) if len(full_url) > 0 else 0
        
        digits_in_host = sum(c.isdigit() for c in hostname)
        features['ratio_digits_host'] = digits_in_host / len(hostname) if len(hostname) > 0 else 0
        
        subdomain = hostname.split('.')[0] if '.' in hostname else ''
        common_tlds = ['com', 'org', 'net', 'edu', 'gov', 'mil', 'int', 'uk', 'de', 'jp', 'fr', 'au', 'us', 'ca', 'cn', 'in', 'ru', 'br', 'za']
        features['tld_in_subdomain'] = 1 if subdomain in common_tlds else 0
        
        domain_parts = hostname.split('.')
        main_domain = domain_parts[1] if len(domain_parts) > 1 else domain_parts[0] if domain_parts else ''
        features['prefix_suffix'] = 1 if '-' in main_domain else 0
        
        words = re.findall(r'[a-zA-Z]+', hostname)
        features['shortest_word_host'] = min([len(w) for w in words]) if words else 0
        
        words = re.findall(r'[a-zA-Z]+', full_url)
        features['longest_words_raw'] = max([len(w) for w in words]) if words else 0
        
        words = re.findall(r'[a-zA-Z]+', path)
        features['longest_word_path'] = max([len(w) for w in words]) if words else 0
        
        phishing_keywords = [
            'secure', 'account', 'banking', 'confirm', 'login', 'signin',
            'verify', 'update', 'password', 'credential', 'paypal', 'apple',
            'microsoft', 'amazon', 'ebay', 'netflix', 'facebook', 'google',
            'bank', 'logon', 'wallet', 'authenticate'
        ]
        features['phish_hints'] = sum(1 for keyword in phishing_keywords if keyword in full_url.lower())
        
        features['nb_hyperlinks'] = 0
        features['ratio_intHyperlinks'] = 0.0
        features['empty_title'] = 0
        features['domain_in_title'] = 0
        features['domain_age'] = -1
        features['google_index'] = 0
        features['page_rank'] = 0
        
        logging.info(f"23 features extracted for URL: {url[:50]}...")
        
    except Exception as e:
        logging.error(f"Error extracting features: {str(e)}")
        features = {
            'length_url': 0, 'length_hostname': 0, 'ip': 0, 'nb_dots': 0,
            'nb_qm': 0, 'nb_eq': 0, 'nb_slash': 0, 'nb_www': 0,
            'ratio_digits_url': 0.0, 'ratio_digits_host': 0.0,
            'tld_in_subdomain': 0, 'prefix_suffix': 0,
            'shortest_word_host': 0, 'longest_words_raw': 0,
            'longest_word_path': 0, 'phish_hints': 0,
            'nb_hyperlinks': 0, 'ratio_intHyperlinks': 0.0,
            'empty_title': 0, 'domain_in_title': 0,
            'domain_age': -1, 'google_index': 0, 'page_rank': 0
        }
    
    return features

def get_feature_names():
    """Return list of 23 feature names in exact order"""
    return [
        'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_qm',
        'nb_eq', 'nb_slash', 'nb_www', 'ratio_digits_url', 'ratio_digits_host',
        'tld_in_subdomain', 'prefix_suffix', 'shortest_word_host',
        'longest_words_raw', 'longest_word_path', 'phish_hints', 'nb_hyperlinks',
        'ratio_intHyperlinks', 'empty_title', 'domain_in_title', 'domain_age',
        'google_index', 'page_rank'
    ]

def get_feature_descriptions():
    """Return descriptions for each feature"""
    return {
        'length_url': 'Total length of the URL',
        'length_hostname': 'Length of the hostname',
        'ip': 'Contains IP address instead of domain name',
        'nb_dots': 'Number of dots in the URL',
        'nb_qm': 'Number of question marks',
        'nb_eq': 'Number of equals signs',
        'nb_slash': 'Number of forward slashes',
        'nb_www': 'Contains "www"',
        'ratio_digits_url': 'Ratio of digits to total characters in URL',
        'ratio_digits_host': 'Ratio of digits to total characters in hostname',
        'tld_in_subdomain': 'Top-level domain appears in subdomain',
        'prefix_suffix': 'Contains hyphen in domain name',
        'shortest_word_host': 'Length of shortest word in hostname',
        'longest_words_raw': 'Length of longest word in URL',
        'longest_word_path': 'Length of longest word in path',
        'phish_hints': 'Number of phishing-related keywords',
        'nb_hyperlinks': 'Number of hyperlinks on the page',
        'ratio_intHyperlinks': 'Ratio of internal hyperlinks',
        'empty_title': 'Page has empty title',
        'domain_in_title': 'Domain name appears in page title',
        'domain_age': 'Age of the domain in days',
        'google_index': 'Page is indexed by Google',
        'page_rank': 'Google PageRank score'
    }

def is_valid_url(url):
    """Check if URL format is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False