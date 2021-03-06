from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Driver init config
options = Options()
options.add_argument('-headless')


def extract_url(url=None, url_list=[]):
    if url is None:
        raise ValueError('URL input is not inputed.')

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(3)
    load_more_button = driver.find_element_by_id('loadMore')
    while True:
        try:
            load_more_button.click()
            time.sleep(1)
            load_more_button = driver.find_element_by_id('loadMore')
        except:
            break
    models = driver.find_element_by_id('models')
    listing = models.find_elements_by_class_name('card-body')
    for i in range(len(listing)):
        a_tag = listing[i].find_element_by_tag_name('a')
        url_list.append(a_tag.get_attribute('href'))
    driver.close()
    return url_list

def get_model_details(url_list=None, data_list=[]):
    if url_list is None:
        raise ValueError('URL List is empty.')
    driver = webdriver.Firefox(options=options)
    for url in url_list:
        driver.get(url)
        model_details_keys = driver.find_element_by_class_name('ModelDetails'
                        ).find_elements_by_class_name('col-3')
        model_details_values = driver.find_element_by_class_name('ModelDetails'
                        ).find_elements_by_class_name('col-9')
        model_details = zip(model_details_keys, model_details_values)
        data = {}
        for k, v in model_details:
            data[k.text] = v.text
        data_list.append(data)
    driver.close()
    return data_list

def csv_export(data_list=None, list_type=None):
    if data_list is None:
        raise EnvironmentError('There no datalist inputs.')
    if list_type is None:
        raise EnvironmentError('There no list_type inputs.')
    
    dt_now = datetime.datetime.now()
    time_stamp = dt_now.strftime('%Y%m%d_%H%M%S')
    csv_title_rows = ['Last', 'Style', 'Name', 'Leather', 'Color', 
                        'Outsole', 'Welt']
    with open('aldenmodelprojct-{}_{}.csv'.format(list_type, time_stamp), 'w',
                newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Last', 'Style', 'Name', 'Leather', 'Color', 
                        'Outsole', 'Welt'])
        for data in data_list:
            decoded_data_list = data.result()
            print(decoded_data_list)
            for data in decoded_data_list:
                Last = data['Last'] if 'Last' in data else ''
                Style = data['Style'] if 'Style' in data else ''
                Name =  data['Name'] if 'Name' in data else ''
                Leather = data['Leather'] if 'Leather' in data else ''
                Color  =  data['Color'] if 'Color' in data else ''
                Outsole = data['Outsole'] if 'Outsole' in data else ''
                Welt = data['Welt'] if 'Welt' in data else ''
                writer.writerow([Last, Style, Name, Leather, Color, 
                                Outsole, Welt])


if __name__ == '__main__':
    dt_now = datetime.datetime.now()
    print(dt_now.strftime('%Y%m%d_%H%M%S'))

    shoe_url_list = extract_url('https://aldenmodelproject.com/shoe/')
    boot_url_list = extract_url('https://aldenmodelproject.com/boot/')
    loafer_url_list = extract_url('https://aldenmodelproject.com/loafer/')

    dt_now = datetime.datetime.now()
    print(dt_now.strftime('%Y%m%d_%H%M%S'))
    shoe_data_list, boot_data_list, loafer_data_list = [], [], []
    with ThreadPoolExecutor(max_workers=3) as executor:
        shoe_data_list.append(executor.submit(get_model_details, 
                            shoe_url_list))
        boot_data_list.append(executor.submit(get_model_details, 
                            boot_url_list))
        loafer_data_list.append(executor.submit(get_model_details, 
                            loafer_url_list))
    dt_now = datetime.datetime.now()
    csv_export(shoe_data_list, 'shoe')
    csv_export(boot_data_list, 'boot')
    csv_export(loafer_data_list, 'loafer')

    dt_now = datetime.datetime.now()
    print(dt_now.strftime('%Y%m%d_%H%M%S'))
