#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 17:04:14 2018

@author: johnnyhsieh
"""

from boa.interop.System.Runtime import Log, GetTrigger, CheckWitness
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash
from boa.interop.System.Blockchain import GetHeight, GetHeader
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import Log, Notify

Push = RegisterAction('event', 'operation', 'msg')

def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No domain name supplied")
        return 0

    if operation == 'owner':
        if nargs == 0:
            print("No domain name supplied")
            return 0
        domain_name = args[0]
        return QueryDomain(domain_name)

    elif operation == 'release':
        if nargs == 0:
            print("No domain name supplied")
            return 0
    
        domain_name = args[0]
        return DeleteDomain(domain_name)

    elif operation == 'register':
        if nargs < 2:
            print("required arguments: [domain_name] [owner]")
            return 0
        
        domain_name = args[0]
        owner = args[1]
        
        
        return RegisterDomain(domain_name, owner)

    elif operation == 'transfer':
        if nargs < 2:
            print("required arguments: [domain_name] [to_address]")
            return 0
        domain_name = args[0]
        to_address = args[1]
        return TransferDomain(domain_name, to_address)
    
    elif operation == 'setAddress':
       if nargs < 2:
           print("required arguments: [domain_name] [to_address]")
           return 0
       domain_name = args[0]
       to_address = args[1]
       return SetAddress(domain_name,to_address)
   
    elif operation == 'addIPFS':
        if nargs < 2:
             print("required arguments: [domain_name] [IPFSHash]")
             return 0
        domain_name = args[0]
        IPFS = args[1]
        return AddIPFSHash(domain_name,IPFS)
    
    elif operation == 'setSubdomain':
        if nargs == 0:
            print("required arguments: [domain_name] [subdomain]")
            return 0
        domain_name = args[0]
        subdomain = args[1]
        return SetSubdomain(domain_name,subdomain)
    
    elif operation == 'getAddress':
        if nargs == 0:
            print("no address supply")
            return 0
        
        domain_name = args[0]
        return GetAddress(domain_name)
        
    elif operation == 'getIPFS':
        if nargs == 0:
            print("no domain supply")
            return 0
        
        domain_name = args[0]
        return GetIPFSHash(domain_name)
    



def QueryDomain(domain_name):
    msg = concat("QueryDomain: ", domain_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, domain_name)
    if not owner:
        Notify("Domain is not yet registered")
        return False

    Notify(owner)
    return owner


def RegisterDomain(domain_name, owner):
    msg = concat("RegisterDomain: ", domain_name)
    Notify(msg)
    
    '''
    Check if the domain contain .
    if ture then return false
    '''
    if detectStr(domain_name) == 1:
        Notify("Domain has incorrect char inside")
        return False
        

    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the sender")
        return False

    context = GetContext()
    exists = Get(context, domain_name)
    if exists:
        Notify("Domain is already registered")
        return False

    Put(context, domain_name, owner)
    msg2 = [domain_name,"is owned by ",owner]
    Notify(msg2)
    return True


def TransferDomain(domain_name, to_address):
    msg = concat("TransferDomain: ", domain_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, domain_name)
    if not owner:
        Notify("Domain is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    if not len(to_address) != 34:
        Notify("Invalid new owner address. Must be exactly 34 characters")
        return False

    Put(context, domain_name, to_address)
    msg2 = [domain_name,"is owned by " ,to_address]
    Notify(msg2)
    return True


def DeleteDomain(domain_name):
    msg = concat("DeleteDomain: ", domain_name)
    Notify(msg)

    context = GetContext()
    owner = Get(context, domain_name)
    if not owner:
        Notify("Domain is not yet registered")
        return False

    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False

    Delete(context, domain_name)
    msg2 = [domain_name,"is release "]
    Notify(msg2)
    return True

def SetAddress(domain_name,to_address):
    msg = concat("SetAddress: ", domain_name)
    Notify(msg)
    context = GetContext()
    owner = Get(context, domain_name)
    if not CheckWitness(owner):
        Notify("Owner argument is not the same as the sender")
        return False
    if not len(to_address) != 34:
        Notify("Invalid new owner address. Must be exactly 34 characters")
        return False
    
    Put(context,"{domain_name}.neo", to_address)
    return True
    


def GetAddress(domain_name):
    msg = concat("GetAddress: ", domain_name)
    Notify(msg)
    if QueryDomain(domain_name) == False:
       return False
    context = GetContext()
    address = Get(context, "{domain_name}.ons")
    return address

def AddIPFSHash(domain_name,IPFS):
    msg = concat("AddIPFS: ",domain_name)
    Notify(msg)
    context = GetContext()
    owner = Get(context, domain_name)
    if not owner:
        Notify("Domain is not yet registered")
        return False
    
    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot transfer")
        return False
    
    Put(context,"{domain_name}.ipfs",IPFS)
    return True

    
def SetSubdomain(domain_name,subdomain):
    msg = concat("SetSubdomain: ",domain_name,subdomain)
    Notify(msg)
    context = GetContext()
    owner = Get(context, domain_name)
    if not owner:
        Notify("Domain is not yet registered")
        return False
    
    if not CheckWitness(owner):
        Notify("Sender is not the owner, cannot set subdomain")
        return False
    
    domain = concat(subdomain,".")
    domain = concat(domain,domain_name)
    
    Put(context,domain, owner)
    
    msg2 = [domain,"is owned by ",owner]
    Notify(msg2)
    return True
    
def GetIPFSHash(domain_name):
    msg = concat("GetIPFSHash: ", domain_name)
    Notify(msg)
    if QueryDomain(domain_name) == False:
       return False
    context = GetContext()
    address = Get(context, "{domain_name}.ipfs")
    return address


def detectStr(detect):
    for i in range(0, len(detect)):
        if substr(detect, i, 1) == ".":
            return True
        
    return False


