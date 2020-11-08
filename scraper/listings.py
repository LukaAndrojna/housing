import config
import page_parser

import threading


class Listings:
    def __init__(self):
        self._successful_listings = [','.join(config.feature_names)]
        self._failed_listings = list()
        self._lock = threading.Lock()
    
    def parse_listing(self, ad):
        features, success = page_parser.get_listing_entry(ad)
        with self._lock:
            if success:
                self._successful_listings.append(features)
            else:
                self._failed_listings.append(features)
    
    def successful_output(self) -> str:
        return '\n'.join(self._successful_listings)
    
    def failed_output(self) -> str:
        return '\n'.join(self._failed_listings)