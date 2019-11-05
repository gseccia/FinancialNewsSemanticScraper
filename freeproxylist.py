# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:31:43 2018

@author: vcpierro
"""
from bs4 import BeautifulSoup
import datetime
import requests
import threading

"""
Decorator for synchronizing methods
"""
def synchronized_method(method):
    
    outer_lock = threading.Lock()
    lock_name = "__"+method.__name__+"_lock"+"__"
    
    def sync_method(self, *args, **kws):
        with outer_lock:
            if not hasattr(self, lock_name): setattr(self, lock_name, threading.Lock())
            lock = getattr(self, lock_name)
            with lock:
                return method(self, *args, **kws)  

    return sync_method

"""
A class to extract proxies from https://free-proxy-list.net/ (thread safe)
"""
class FreeProxyList():

    """
    Init method
    :param only_elite: an optional boolean param. Specifies if only the elite proxies 
    should be selected. Default is True
    :param update_frequency: an optional integer param. Specifies the frequency of update
    (in seconds). Default is 600 (10 minutes)
    :param return_string: an optional boolean param. Specifies if the port should be 
    returned as string or integer. Default False.
    """
    def __init__(self, only_elite=True, update_frequency=600, return_string=False):
        self.url = "https://free-proxy-list.net/"
        
        if not isinstance(only_elite, bool):
            raise Exception("The only_elite parameter should be boolean!")
        self.elite = only_elite
        
        if not isinstance(update_frequency, int):
            raise Exception("The update_frequency parameter should be int!")
            
        if not isinstance(return_string, bool):
            raise Exception("The return_string parameter should be boolean!")
            
        self.frequency = update_frequency
        self.format = return_string
        self.proxies = []
        self.last_updated = datetime.datetime.now()
        self.update_proxies()
    
    """
    The method will update the proxies, creating a list of tuples structured
    like (proxy, port). The list will be resetted and will contain only the new 
    proxies after the update
    """
    @synchronized_method
    def update_proxies(self):
        head = {
            'User-Agent'    :   'Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0'
        }
        r = requests.get(self.url, headers=head, timeout=20)
        if r.status_code != 200:
            raise Exception("Requests error! Code: "+str(r.status_code))
        soup = BeautifulSoup(r.content, 'lxml')
        self.proxies = []
        for row in soup.select("table#proxylisttable tbody tr"):
            cols = row.select("td")
            if self.elite:
                if cols[4].text == 'elite proxy':
                    p = {'ip':cols[0].text}
                    if self.format:
                        p['port'] = str(cols[1].text)
                    else:
                        p['port'] = int(cols[1].text)
                    self.proxies.append(p)
            else:
                p = {'ip':cols[0].text}
                if self.format:
                    p['port'] = str(cols[1].text)
                else:
                    p['port'] = int(cols[1].text)
                self.proxies.append(p)
        self.last_updated = datetime.datetime.now()
    
    """
    This method returns a proxy, removing it from the list. It also checks if
    the list last update is older than 10 minutes. In this case, it updates the
    list before returning the proxy
    """    
    @synchronized_method
    def get_proxy(self):
        diff = datetime.datetime.now() - self.last_updated
        if len(self.proxies) == 0 or diff.total_seconds() > self.frequency:
            self.update_proxies()
        
        return self.proxies.pop()
    
    """
    The method return the total seconds from the last update
    """
    @synchronized_method
    def last_checked(self):
        return (datetime.datetime.now() - self.last_updated).total_seconds()


