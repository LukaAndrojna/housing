propety_types = {
    'Stanovanje': 'apartment',
    'Hiša': 'house',
    'Vikend': 'cottage house',
    'Posest': 'land',
    'Poslovni prostor': 'business premise',
    'Garaža': 'garage',
    'Počitniški objekt': 'holiday home'
    
}

feature_names = ['location','floor_area','type','built','adapted','land','floor','price','m2_price','offer_type','propety_type','region','subregion','commune']

DEFAULT_URL = 'https://www.nepremicnine.net'
#SUB_GROUPS = ['/oglasi-najem/', '/oglasi-nakup/']
SUB_GROUPS = ['/oglasi-prodaja/', '/oglasi-oddaja/']