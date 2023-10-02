import pandas as pd, numpy as np
import json

import math

import pickle
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import sys

import pymongo

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session

import datetime
import urllib.parse
import requests



# User Obj class

class User:
    username = ''
    password = ''
    f_name = ''
    l_name = ''
    phone = ''
    industry = ''
    compane_name = ''
    job_title = ''
    experience = 0
    homes_built = 0
    license_number = ''
    credits = 0.0
    def __init__(self):
        self.username = ''
        self.password = ''
        self.f_name = ''
        self.l_name = ''
        self.phone = ''
        self.industry = ''
        self.compane_name = ''
        self.job_title = ''
        self.experience = 0
        self.homes_built = 0
        self.license_number = ''
        self.credits = 0.0
    def setUserBasic(self,username,password,name):
        self.username = username
        self.password = password
        name_parts = name.split('-',1)
        if(len(name_parts)>1):
            self.f_name = name_parts[0]
            self.l_name = name_parts[1]
        elif(len(name_parts)==1):
            self.f_name = name_parts[0]
            self.l_name = ''
        elif(len(name_parts)==0):
            self.f_name = ''
            self.l_name = ''
        self.phone = ''
        self.industry = ''
        self.compane_name = ''
        self.job_title = ''
        self.experience = 0
        self.homes_built = 0
        self.license_number = ''
        self.credits = 0.0
    def setUser(self,username,password,f_name,l_name,phone):
        self.username = username
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.industry = ''
        self.compane_name = ''
        self.job_title = ''
        self.experience = 0
        self.homes_built = 0
        self.license_number = ''
        self.credits = 0.0
    def setUserComplete(self,username,password,f_name,l_name,phone,industry,company_name,job_title,experience,homes_built,license_number,credits):
        self.username = username
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.industry = industry
        self.compane_name = compane_name
        self.job_title = job_title
        self.experience = experience
        self.homes_built = homes_built
        self.license_number = license_number
        self.credits = 0.0
    def printUser(self):
        print('Username : ',self.username)
        print('Password : ',self.password)
        print('First Name : ',self.f_name)
        print('Last Name : ',self.l_name)
        print('Phone : ',self.phone)
        print('Industry : ',self.industry)
        print('Company Name : ',self.compane_name)
        print('Job Title : ',self.job_title)
        print('Experience : ',self.experience)
        print('Homes Built : ',self.homes_built)
        print('License Number : ',self.license_number)
        print('Credits : ',self.credits)


class userInputForm:
    min_area = 0
    max_area = 0
    bed_count = 0
    full_bath_count = 0
    half_bath_count = 0
    total_bath_count = full_bath_count + 0.5*half_bath_count
    story_count = 0
    garage_count = 0
    addr_city = ''
    addr_state = ''
    build_quality = ''
    basement_type = ''
    acquisition_cost = 0
    home_style = ''
    complete_address = ''

    def __init__(self,min_area,max_area,bed_count,full_bath_count,half_bath_count,story_count,garage_count,\
                 build_quality,basement_type,acquisition_cost,home_style,complete_address):
        self.min_area = min_area
        self.max_area = max_area
        self.bed_count = bed_count
        self.full_bath_count = full_bath_count
        self.half_bath_count = half_bath_count
        self.total_bath_count = self.full_bath_count + 0.5*self.half_bath_count
        self.story_count = story_count
        self.garage_count = garage_count
        self.addr_city = ''
        self.addr_state = ''
        self.build_quality = build_quality
        self.basement_type = basement_type
        self.acquisition_cost = acquisition_cost
        self.home_style = home_style
        self.complete_address = complete_address



class plan_obj:
    area_total = 0
    bedrooms_count = 0
    bathrooms_count = 0
    bathrooms_full_count = 0
    bathrooms_half_count = 0
    stories = 0
    area_first_floor = 0
    area_second_floor = 0
    area_third_floor = 0
    area_basement = 0
    area_garage = 0
    cars_capacity = 0
    width = 0
    depth = 0
    buy_url = ''
    plan_number = ''
    title = ''
    image_link = ''
    architectural_style = ''
        
    def __init__(self,area_total,bedrooms_count,bathrooms_count,bathrooms_full_count,\
                 bathrooms_half_count,stories,area_first_floor,area_second_floor,\
                 area_third_floor,area_basement,area_garage,cars_capacity,width,depth,buy_url,\
                 plan_number,title,image_link,architectural_style):
        self.area_total = area_total
        self.bedrooms_count = bedrooms_count
        self.bathrooms_count = bathrooms_count
        self.bathrooms_full_count = bathrooms_full_count
        self.bathrooms_half_count = bathrooms_half_count
        self.stories = stories
        self.area_first_floor = area_first_floor
        self.area_second_floor = area_second_floor
        self.area_third_floor = area_third_floor
        self.area_basement = area_basement
        self.area_garage = area_garage
        self.cars_capacity = cars_capacity
        self.width = 0
        self.depth = 0
        self.buy_url = buy_url
        self.plan_number = plan_number
        self.title = title
        self.image_link = image_link
        self.architectural_style = architectural_style


def getShortListedPlans(home_style,userInputObj):
    plans_data = pd.read_csv('data/architectural_plans_preprocessed.csv')

    if (home_style == 'CRAFTSMAN'):
        style_options = ['CRAFTSMAN','COTTAGE','BUNGALOW','TUDOR','NEW AMERICAN']
    if (home_style == 'RANCH'):
        style_options = ['RANCH']
    if (home_style == 'CAPE COD'):
        style_options = ['CAPE COD','COLONIAL','SOUTHERN TRADITIONAL','SHINGLE','COUNTRY','NEW ORLEANS']
    if (home_style == 'VICTORIAN'):
        style_options = ['VICTORIAN','GEORGIAN','TUDOR','LOUISIANA','EUROPEAN','FRENCH COUNTRY']
    if (home_style == 'TRADITIONAL'):
        style_options = ['TRADITIONAL','SOUTHERN','FARMHOUSE','HILL COUNTRY','NEW ORLEANS','NORTHWEST']
    if (home_style == 'CONTEMPORARY'):
        style_options = ['CONTEMPORARY','MODERN','MID CENTURY','MODERN FARMHOUSE','SCANDANAVIAN','PRARIE']
    if (home_style == 'SPANISH'):
        style_options = ['SPANISH','TUSCAN','ADOBE','SOUTHWEST']
    if (home_style == 'VACATION'):
        style_options = ['VACATION','CABIN','RUSTIC','LAKE HOUSE','A - FRAME','BARNDOMINIUM','MOUNTAIN','LOG']
    if (home_style == 'COASTAL'):
        style_options = ['COASTAL','MEDITTERANEAN','LOW COUNTRY','COASTAL CONTEMPORARY','FLORIDA']
    
    
    shortlisted_plans = plans_data.loc[(plans_data['area_total'] >= userInputObj.min_area) & (plans_data['area_total'] <= userInputObj.max_area) &\
                                        (plans_data['bathrooms_count']==userInputObj.total_bath_count) & (plans_data['bedrooms_count'] == userInputObj.bed_count) &\
                                        (plans_data['stories']==userInputObj.story_count) & (plans_data['cars_capacity']==userInputObj.garage_count) &\
                                        (plans_data['area_basement']==0 if userInputObj.basement_type=='NO' else plans_data['area_basement']>0 ) &\
                                        (plans_data['architectural_style'].isin(style_options)) ]

    shortlisted_plans_n = len(shortlisted_plans)
    shortlisted_plans_arr = []

    for idx in range(shortlisted_plans_n):
        plan = shortlisted_plans.iloc[idx]
        shortlisted_plans_arr.append(plan_obj(plan[0],plan[1],plan[2],plan[3],\
                     plan[4],plan[5],plan[6],plan[7],\
                     plan[8],plan[9],plan[10],plan[11],plan[12],plan[13],\
                     plan[14],plan[15],plan[16],plan[17],plan[18]))
    
    return shortlisted_plans_arr

def getSelectedPlanIdx(shortlisted_plans_arr, selectedPlanName):
    for idx,plan in enumerate(shortlisted_plans_arr):
        if(shortlisted_plans_arr[idx].plan_number == selectedPlanName):
            return idx


def convertPlanDictToPlanObj(selected_plan_dict):
    planObj = plan_obj(selected_plan_dict['area_total'],selected_plan_dict['bedrooms_count'],\
                       selected_plan_dict['bathrooms_count'],selected_plan_dict['bathrooms_full_count'],\
                       selected_plan_dict['bathrooms_half_count'],selected_plan_dict['stories'],\
                       selected_plan_dict['area_first_floor'],selected_plan_dict['area_second_floor'],\
                       selected_plan_dict['area_third_floor'],selected_plan_dict['area_basement'],\
                       selected_plan_dict['area_garage'],selected_plan_dict['cars_capacity'],\
                       selected_plan_dict['width'],selected_plan_dict['depth'],selected_plan_dict['buy_url'],\
                       selected_plan_dict['plan_number'],selected_plan_dict['title'],\
                       selected_plan_dict['image_link'],selected_plan_dict['architectural_style'])
    return planObj

def callToVoDataAPI(address):
    comp_resp = {'results': {'comparables': [{'deedSaleDate': '2023-07-24T00:00:00',
        'deedSaleAmount': 329500,
        'deedFirstMortgageAmount': 115000,
        'distance': 0.41266668,
        'fullStreetAddress': '3126 GAY DR',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1958',
        'taxAmount': 1565.16,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'EDGETT KAYLA',
        'ownerName2': 'SLOTE KEVIN',
        'bedrooms': 3,
        'bathrooms': 1.5,
        'squareFeet': 1274,
        'lotSizeSqFt': 17424,
        'pricePerSquareFoot': 258.63422,
        'avm': 331506,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.26225,
        'latitude': 33.72305},
       {'deedSaleDate': '2023-07-13T00:00:00',
        'deedSaleAmount': 250000,
        'deedFirstMortgageAmount': 282750,
        'distance': 0.38656813,
        'fullStreetAddress': '2932 VALLEY RIDGE DR',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1959',
        'taxAmount': 3205.0,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': ' ',
        'ownerName1': 'EL GATO REAL ESTATE CORP',
        'ownerName2': '',
        'bedrooms': 3,
        'bathrooms': 2.0,
        'squareFeet': 2004,
        'lotSizeSqFt': 17424,
        'pricePerSquareFoot': 124.750496,
        'avm': 257109,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.2701,
        'latitude': 33.721527},
       {'deedSaleDate': '2023-07-07T00:00:00',
        'deedSaleAmount': 248900,
        'deedFirstMortgageAmount': 224010,
        'distance': 0.39217213,
        'fullStreetAddress': '2823 OAKLAND TER',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1953',
        'taxAmount': 3139.18,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'MALONE HEATHER M',
        'ownerName2': '',
        'bedrooms': 3,
        'bathrooms': 1.0,
        'squareFeet': 1107,
        'lotSizeSqFt': 13068,
        'pricePerSquareFoot': 224.84192,
        'avm': 236356,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.274536,
        'latitude': 33.727818},
       {'deedSaleDate': '2023-07-03T00:00:00',
        'deedSaleAmount': 255000,
        'deedFirstMortgageAmount': 299975,
        'distance': 0.48084342,
        'fullStreetAddress': '2622 MIRIAM LN',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1956',
        'taxAmount': 3685.66,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': ' ',
        'ownerName1': 'M & E GONZALEZ EXPERT & HOMES LLC',
        'ownerName2': '',
        'bedrooms': 3,
        'bathrooms': 2.0,
        'squareFeet': 1530,
        'lotSizeSqFt': 13068,
        'pricePerSquareFoot': 166.66667,
        'avm': 317368,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.269905,
        'latitude': 33.720047},
       {'deedSaleDate': '2023-06-23T00:00:00',
        'deedSaleAmount': 345000,
        'deedFirstMortgageAmount': 333485,
        'distance': 0.43293914,
        'fullStreetAddress': '2233 BARBARA LN',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1956',
        'taxAmount': 4624.8,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'ADAMS TANYA',
        'ownerName2': '',
        'bedrooms': 3,
        'bathrooms': 2.0,
        'squareFeet': 1515,
        'lotSizeSqFt': 13068,
        'pricePerSquareFoot': 227.72278,
        'avm': 334259,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.2611,
        'latitude': 33.724003},
       {'deedSaleDate': '2023-06-22T00:00:00',
        'deedSaleAmount': 465000,
        'deedFirstMortgageAmount': 390000,
        'distance': 0.48733595,
        'fullStreetAddress': '2059 DELLWOOD PL',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1952',
        'taxAmount': 1938.2,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'CARLEY RYAN JOSHUA',
        'ownerName2': 'MCCAULEY AMIEE IRENE',
        'bedrooms': 4,
        'bathrooms': 3.0,
        'squareFeet': 2313,
        'lotSizeSqFt': 8712,
        'pricePerSquareFoot': 201.03761,
        'avm': 469715,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.27527,
        'latitude': 33.73018},
       {'deedSaleDate': '2023-06-21T00:00:00',
        'deedSaleAmount': 445000,
        'deedFirstMortgageAmount': 373835,
        'distance': 0.2867672,
        'fullStreetAddress': '2083 GLENDALE DR',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1953',
        'taxAmount': 2946.72,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'PYLE JESSE',
        'ownerName2': 'PYLE TAYLOR A',
        'bedrooms': 3,
        'bathrooms': 1.0,
        'squareFeet': 1164,
        'lotSizeSqFt': 8712,
        'pricePerSquareFoot': 382.3024,
        'avm': 457076,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.26365,
        'latitude': 33.729065},
       {'deedSaleDate': '2023-06-21T00:00:00',
        'deedSaleAmount': 407500,
        'deedFirstMortgageAmount': 305625,
        'distance': 0.40810144,
        'fullStreetAddress': '2844 TONEY DR',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1954',
        'taxAmount': 4480.98,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'DARYONNI BEROOZ',
        'ownerName2': '',
        'bedrooms': 3,
        'bathrooms': 2.5,
        'squareFeet': 1425,
        'lotSizeSqFt': 17424,
        'pricePerSquareFoot': 285.9649,
        'avm': 408472,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.27375,
        'latitude': 33.723557},
       {'deedSaleDate': '2023-06-02T00:00:00',
        'deedSaleAmount': 216500,
        'deedFirstMortgageAmount': 210005,
        'distance': 0.41796964,
        'fullStreetAddress': '2033 ROSEWOOD RD',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1954',
        'taxAmount': 2386.28,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': 'Y',
        'ownerName1': 'JENKO JULIA LYNN',
        'ownerName2': '',
        'bedrooms': 2,
        'bathrooms': 1.0,
        'squareFeet': 1070,
        'lotSizeSqFt': 13068,
        'pricePerSquareFoot': 202.33644,
        'avm': 177688,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.26241,
        'latitude': 33.73084},
       {'deedSaleDate': '2023-05-31T00:00:00',
        'deedSaleAmount': 230000,
        'deedFirstMortgageAmount': 225834,
        'distance': 0.41702503,
        'fullStreetAddress': '2089 BARBARA LN',
        'city': 'DECATUR',
        'state': 'GA',
        'zip': '30032',
        'yearBuilt': '1956',
        'taxAmount': 2438.94,
        'pool': None,
        'schoolDistrictName': 'DeKalb County School District',
        'ownerOccupied': ' ',
        'ownerName1': 'BERKE GRACE',
        'ownerName2': 'MCKINNEY AARON',
        'bedrooms': 3,
        'bathrooms': 1.0,
        'squareFeet': 1033,
        'lotSizeSqFt': 13068,
        'pricePerSquareFoot': 222.65247,
        'avm': 229024,
        'valuationDate': '2023-09-13T00:00:00',
        'longitude': -84.26105,
        'latitude': 33.72892}],
      'propertyAddress': {'id': 136275067,
       'fips': '13089',
       'fullAddress': '2998 MIRIAM CT',
       'apartmentUnitNumber': None,
       'carrierCode': None,
       'city': 'DECATUR',
       'county': 'DeKalb County',
       'direction': None,
       'directionSuffix': None,
       'houseNumber': '2998',
       'houseNumberPrefix': None,
       'houseNumberSuffix': None,
       'mailMode': 'CT',
       'quadrant': None,
       'stateProvince': 'GA',
       'streetName': 'MIRIAM',
       'zipCode4': None,
       'zipCode5': '30032',
       'longitude': -84.26783,
       'latitude': 33.726807},
      'originalRequest': {'firstname': '',
       'lastname': '',
       'addressLine1': '2998 MIRIAM CT',
       'addressLine2': '',
       'city': 'DECATUR',
       'state': 'GA',
       'zip': '30032'},
      'id': 624897923044352000,
      'created': '2023-09-21T09:21:14.8951003+00:00'},
     'isSuccess': True,
     'credits': 1,
     'message': ''}
    
    return comp_resp

class comp_obj:
    address = ''
    zillow_link = ''
    distance = 0.0
    value = 0.0
    area = 0
    bed_count = 0
    bath_count = 0.0
    year = 0
    lot_area = 0
    avm = 0
    price_per_sq_ft = 0.0
        
    def __init__(self,address,distance,area,bed_count,bath_count,year,lot_area,avm,price_per_sq_ft):
        self.address = address
        self.distance = round(distance,3)
        self.value = 0.0
        self.area = area
        self.bed_count = bed_count
        self.bath_count = bath_count
        self.year = year
        self.lot_area = lot_area
        self.avm = avm
        self.zillow_link = ''
        self.price_per_sq_ft = round(price_per_sq_ft,2)
    def setValue(self,value):
        self.value = int(value)
    def print(self):
        print(self.address,',' ,self.distance,', ',self.area,', ',self.bed_count,\
              ',',self.bath_count,'',self.year,'',self.lot_area,',',self.value,\
              ',',self.avm,',',self.price_per_sq_ft,',',self.zillow_link)
    def setZillowLink(self):
        comp_addrs = self.address
        comp_addrs = comp_addrs.replace(',', '-')
        comp_addrs = comp_addrs.replace(' ', '-')
        self.zillow_link = 'https://www.zillow.com/homes/'+comp_addrs+'_rb/'


def adjustComparablePrice(query_property,comparable_property):
    q_year_build = query_property.year_build
    q_area = query_property.area
    q_baths_full = query_property.baths_full
    q_baths_half = query_property.baths_half
    q_bedrooms = query_property.bedrooms

    cmp_avm = comparable_property.avm
    cmp_year_build = comparable_property.year
    cmp_area = comparable_property.area
    cmp_price_per_sq_ft = comparable_property.price_per_sq_ft
    cmp_baths_total = comparable_property.bath_count
    cmp_baths_half,cmp_baths_full = math.modf(cmp_baths_total)
    cmp_baths_half =  cmp_baths_half *2
    cmp_lot_size = comparable_property.lot_area
    cmp_bedroom_count = comparable_property.bed_count

    diff_year = cmp_year_build - q_year_build
    diff_area = cmp_area - q_area
    diff_bath_full = int(cmp_baths_full - q_baths_full)
    diff_bath_half = int(cmp_baths_half - q_baths_half)
    adj_price = cmp_avm
    
    if(abs(diff_year)>=71):
        a_1 = cmp_avm*.15
    elif(abs(diff_year)>=41 & abs(diff_year)<=70):
        a_1 = cmp_avm*.1
    elif(abs(diff_year)>=21 & abs(diff_year)<=40):
        a_1 = cmp_avm*.05
    else:
        a_1 = 0
    if(diff_year<0):
        adj_price = adj_price + a_1
    else:
        adj_price = adj_price - a_1
    
    # print('Comp Price after year adj : ',adj_price)
    
    a_2 = abs(diff_area) * cmp_price_per_sq_ft
    if(diff_area<0):
        adj_price = adj_price + a_2
    else:
        adj_price = adj_price - a_2
    
    # print('Comp Price after area adj : ',adj_price)
    
    half_bath_base_price = 4000
    alpha_bh = 200
    
    if(diff_bath_half==0):
        if(diff_year<0):
            adj_price = adj_price + (abs(diff_year/10)*alpha_bh)
        else:
            adj_price = adj_price - (abs(diff_year/10)*alpha_bh)
    
    if(diff_bath_half!=0):
        if((diff_year<0) & (diff_bath_half<0)):
            adj_price = adj_price + abs(diff_bath_half)*half_bath_base_price + (abs(diff_year/10)*alpha_bh)
        if((diff_year<0) & (diff_bath_half>0)):
            adj_price = adj_price - (abs(diff_bath_half)*half_bath_base_price - (abs(diff_year/10)*alpha_bh))
        if((diff_year>0) & (diff_bath_half<0)):
            adj_price = adj_price + abs(diff_bath_half)*half_bath_base_price - (abs(diff_year/10)*alpha_bh)
        if((diff_year>0) & (diff_bath_half>0)):
            adj_price = adj_price - abs(diff_bath_half)*half_bath_base_price - (abs(diff_year/10)*alpha_bh)
    
    # print('Comp Price after half bath adj : ',adj_price)
    
    full_bath_base_price = 8000
    alpha_bf = 400
    
    if(diff_bath_full==0):
        if(diff_year<0):
            adj_price = adj_price + (abs(diff_year/10)*alpha_bf)
        else:
            adj_price = adj_price - (abs(diff_year/10)*alpha_bf)
    
    if(diff_bath_full!=0):
        if((diff_year<0) & (diff_bath_full<0)):
            adj_price = adj_price + abs(diff_bath_full)*full_bath_base_price + (abs(diff_year/10)*alpha_bf)
        if((diff_year<0) & (diff_bath_full>0)):
            adj_price = adj_price - (abs(diff_bath_full)*full_bath_base_price - (abs(diff_year/10)*alpha_bf))
        if((diff_year>0) & (diff_bath_full<0)):
            adj_price = adj_price + abs(diff_bath_full)*full_bath_base_price - (abs(diff_year/10)*alpha_bf)
        if((diff_year>0) & (diff_bath_full>0)):
            adj_price = adj_price - abs(diff_bath_full)*full_bath_base_price - (abs(diff_year/10)*alpha_bf)

    return adj_price

def getComparablesObjsArray(comp_resp):
    comps_received_n = len(comp_resp['results']['comparables'])
    cmp_items_arr = []
    
    for i in range(comps_received_n):
    
        cmp_avm = comp_resp['results']['comparables'][i]['avm']
        cmp_year_build = int(comp_resp['results']['comparables'][i]['yearBuilt'])
        cmp_area = comp_resp['results']['comparables'][i]['squareFeet']
        cmp_price_per_sq_ft = comp_resp['results']['comparables'][i]['pricePerSquareFoot']
        cmp_baths_total = comp_resp['results']['comparables'][i]['bathrooms']
        cmp_baths_half,cmp_baths_full = math.modf(cmp_baths_total)
        cmp_baths_half =  cmp_baths_half *2
        cmp_lot_size = comp_resp['results']['comparables'][i]['lotSizeSqFt']
        cmp_bedroom_count = comp_resp['results']['comparables'][i]['bedrooms']
        cmp_distance = comp_resp['results']['comparables'][i]['distance']
        cmp_address = comp_resp['results']['comparables'][i]['fullStreetAddress'] + ',' + \
                        comp_resp['results']['comparables'][i]['city'] + ',' + \
                        comp_resp['results']['comparables'][i]['state'] + ',' + \
                        comp_resp['results']['comparables'][i]['zip']
        cmp_items_arr.append(comp_obj(cmp_address,cmp_distance,cmp_area,cmp_bedroom_count,cmp_baths_total,\
                                      cmp_year_build,cmp_lot_size,cmp_avm,cmp_price_per_sq_ft))
    return cmp_items_arr

def setAndGetAdjustedValuesofComparables(cmp_items_arr,query_prop):
    comparables_adjst_prices = [adjustComparablePrice(query_prop,cmp_item) for cmp_item in cmp_items_arr]
    for idx,cmp_item in enumerate(cmp_items_arr):
        cmp_item.setZillowLink()
        cmp_item.setValue(comparables_adjst_prices[idx])
        # cmp_item.print()
    return comparables_adjst_prices

def setVACofQueryPropertyObj(query_prop,cmp_items_arr,comparables_adjst_prices):
    sorted_comps_idx=np.argsort(comparables_adjst_prices)
    mid_comps_adjst_prices = [cmp_items_arr[i].value for i in sorted_comps_idx[2:8].tolist()]
    q_vac = int(np.mean(mid_comps_adjst_prices))
    query_prop.setVAC(q_vac)

def getCompsIdxUsedforVAC(comparables_adjst_prices):
    sorted_comps_idx=np.argsort(comparables_adjst_prices)
    return sorted_comps_idx[2:8].tolist()

def convertComparableDictToComparableObj(comparable_dict):
    comparableObj = comp_obj(comparable_dict['address'],comparable_dict['distance'],\
                            comparable_dict['area'],comparable_dict['bed_count'],\
                            comparable_dict['bath_count'],comparable_dict['year'],\
                            comparable_dict['lot_area'],comparable_dict['avm'],\
                            comparable_dict['price_per_sq_ft'])
    return comparableObj


class queryPropertyForComps:
    year_build = 0
    area = 0
    area_basement = 0
    area_garage = 0
    baths_full = 0
    baths_half = 0
    bedrooms = 0
    vac = 0
    def __init__(self,year_build,area,area_basement,area_garage,baths_full,baths_half,bedrooms):
        self.year_build = int(year_build)
        self.area = int(area)
        self.area_basement = int(area_basement)
        self.area_garage = int(area_garage)
        self.baths_full = int(baths_full)
        self.baths_half = int(baths_half)
        self.bedrooms = int(bedrooms)
    def setVAC(self,vac):
        self.vac = vac
    def print(self):
        print('Year build : ',self.year_build)
        print('Area : ',self.area)
        print('Area Basement: ',self.area_basement)
        print('Area Garage : ',self.area_garage)
        print('Baths-full : ',self.baths_full)
        print('Bath-half : ',self.baths_half)
        print('Bedrooms : ',self.bedrooms)
        print('VAC : ',self.vac)


def initializeQueryPropertyFromSelectedArchitectural(selectedPlan):
    today = datetime.date.today()
    q_year = today.year
    q_area = selectedPlan.area_total
    q_area_basement = selectedPlan.area_basement
    q_area_garage = selectedPlan.area_garage
    q_baths_full = selectedPlan.bathrooms_full_count
    q_baths_half = selectedPlan.bathrooms_half_count
    q_bedrooms = selectedPlan.bedrooms_count
    queryPropertyObj = queryPropertyForComps(q_year,q_area,q_area_basement,q_area_garage,q_baths_full,q_baths_half,q_bedrooms)
    return queryPropertyObj

def predictConstructionCostFromModel(q_state,q_city,q_quality,q_story_count,q_basement_type,q_area):
    dir_name = 'cost_estimation_model/'
    
    state_mapping_file =  pd.read_csv(dir_name+'state_mapping.csv')
    state_val_dict = {}
    for state_name,state_mapping in zip(state_mapping_file['State'],state_mapping_file['Mapping']):
        state_val_dict[state_name] = state_mapping
    # reverse_state_mapping = [state for state in state_mapping['State']]

    city_mapping_file =  pd.read_csv(dir_name+'city_mapping.csv')
    city_val_dict = {}
    for city_name,city_mapping in zip(city_mapping_file['City'],city_mapping_file['Mapping']):
        city_val_dict[city_name] = city_mapping
    # reverse_city_mapping = [city for city in city_mapping['City']]

    quality_mapping_file =  pd.read_csv(dir_name+'quality_mapping.csv')
    quality_val_dict = {}
    for quality_name,quality_mapping in zip(quality_mapping_file['Quality'],quality_mapping_file['Mapping']):
        quality_val_dict[quality_name] = quality_mapping
    # reverse_quality_mapping = [quality for quality in quality_mapping['Quality']]

    basement_mapping_file =  pd.read_csv(dir_name+'basement_mapping.csv')
    basement_val_dict = {}
    for basement_name,basement_mapping in zip(basement_mapping_file['Basement'],basement_mapping_file['Mapping']):
        basement_val_dict[basement_name] = basement_mapping
    # reverse_basement_mapping = [basement for basement in basement_mapping['Basement']]

    user_input = [q_state,q_city,q_quality,q_story_count,q_basement_type,q_area]
    print(user_input)
    user_input_numeric = [state_val_dict[user_input[0]],city_val_dict[user_input[1]],quality_val_dict[user_input[2]],\
                     user_input[3],basement_val_dict[user_input[4]],user_input[5]]
    user_input_numeric = np.array(user_input_numeric).reshape(1,-1)
    print(user_input_numeric)

    pred_model = pickle.load(open(dir_name+'prediction_model.sav', 'rb'))
    MSACC = pred_model.predict(user_input_numeric)
    return MSACC[0]

def calculateTotalConstructionCost(MSACC, area, area_basement,area_garage, basement_type, unfinished_scaling_factor):
    total_construction_cost = MSACC * area + area_garage*MSACC*unfinished_scaling_factor
    if(basement_type=='FINISHED'):
        total_construction_cost += area_basement*MSACC
    if(basement_type=='UNFINISHED'):
        total_construction_cost += area_basement*MSACC*unfinished_scaling_factor
    return int(total_construction_cost)

class KPI:
    vac = 0
    construction_cost = 0
    total_project_cost = 0
    acquisition_cost = 0
    equity = 0
    def __init__(self,vac,construction_cost,acquisition_cost):
        self.vac = int(vac)
        self.construction_cost = int(construction_cost)
        self.acquisition_cost = int(acquisition_cost)
        self.total_project_cost = self.construction_cost + self.acquisition_cost
        self.equity = self.vac - self.total_project_cost  
        
    def print(self):
        print('KPIs')
        print('VAC : ',self.vac)
        print('Construction Cost : ',self.construction_cost)
        print('Total Project Cost : ',self.total_project_cost)
        print('Equity : ', self.equity )

    def setConstructionCost(self,construction_cost):
        self.construction_cost = int(construction_cost)
        self.total_project_cost = self.construction_cost + self.acquisition_cost
        self.equity = self.vac - self.total_project_cost

    def setVAC(self,vac):
        self.vac = int(vac)
        self.equity = self.vac - self.total_project_cost


class ReGridResponse:
    p_cord = []
    p_lat = 0.0
    p_lng = 0.0
    p_area = 0.0
    p_school_dist = ''
    p_sfr = ''
    p_tax_amount = 0
    p_city = ''
    p_state = ''
    p_street_adr = ''
    query_address = ''
    p_parcel_id = ''
    def __init__(self,p_cord,p_lat,p_lng,p_area,p_school_dist,p_sfr,p_tax_amount,\
                 p_city,p_state,p_street_adr,p_query_address,p_parcel_id):
        self.p_cord = p_cord
        self.p_lat = p_lat
        self.p_lng = p_lng
        self.p_area = p_area
        self.p_school_dist = p_school_dist
        self.p_sfr = p_sfr
        self.p_tax_amount = p_tax_amount
        self.p_city = p_city
        self.p_state = p_state
        self.p_street_adr = p_street_adr
        self.p_query_address = p_query_address
        self.p_parcel_id = p_parcel_id

def convertReGridResponseDictToRegridResponseObj(regridResponse_dict):
    regridObj = ReGridResponse(regridResponse_dict['p_cord'],regridResponse_dict['p_lat'],\
                            regridResponse_dict['p_lng'],regridResponse_dict['p_area'],\
                            regridResponse_dict['p_school_dist'],regridResponse_dict['p_sfr'],\
                            regridResponse_dict['p_tax_amount'],regridResponse_dict['p_city'],\
                            regridResponse_dict['p_state'],regridResponse_dict['p_street_adr'],\
                            regridResponse_dict['p_query_address'],regridResponse_dict['p_parcel_id'])
    return regridObj

def callReGridAPI(address):
    api_key_regrid = 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNjkzODE1NDI3LCJleHAiOjE2OTY0MDc0MjcsInUiOjMxMDE2MCwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnNiIn0.vw0oFi2qODn3TKy_aQ6U8EevoHfouwFxpEuOipbC2TU'
    url_regrid_1 = 'https://app.regrid.com/api/v1/search.json?query='
    url_regrid_2 = '&strict=1&limit=1&token='+api_key_regrid
    address_uri_encoded = urllib.parse.quote(address)
    api_endpoint_regrid = url_regrid_1  + address_uri_encoded + url_regrid_2
    resp = requests.get(api_endpoint_regrid)
    p_cord = resp.json()['results'][0]['geometry']['coordinates']
    p_lat = resp.json()['results'][0]['properties']['fields']['lat']
    p_lng = resp.json()['results'][0]['properties']['fields']['lon']
    p_area = resp.json()['results'][0]['properties']['fields']['ll_gissqft']
    p_school_dist = resp.json()['results'][0]['properties']['fields']['schldscrp']
    p_sfr = resp.json()['results'][0]['properties']['fields']['structstyle']
    p_tax_amount = resp.json()['results'][0]['properties']['fields']['city_taxable_val']
    p_city = resp.json()['results'][0]['properties']['fields']['scity']
    p_state = resp.json()['results'][0]['properties']['fields']['state2']
    p_street_adr = resp.json()['results'][0]['properties']['headline']
    p_parcel_id = resp.json()['results'][0]['properties']['fields']['parcelnumb']
    regridRespObj = ReGridResponse(p_cord,p_lat,p_lng,p_area,p_school_dist,p_sfr,p_tax_amount,\
                                   p_city,p_state,p_street_adr,address,p_parcel_id)
    return regridRespObj

class ZoneInfo:
    zoning_url = ''
    zoning_classification = ''
    zoning_code = ''
    zoning_far = ''
    zoning_lot_coverage = ''
    zoning_building_height = ''
    zoning_min_front_setback = ''
    zoning_min_rear_setback = ''
    zoning_min_side_setback = ''
    state = ''
    city = ''
    def __init__(self,url,classification,code,far,lot_coverage,building_height,front_setback,rear_setback,side_setback):
        self.zoning_url = url
        self.zoning_classification = classification
        self.zoning_code = code
        self.zoning_far = far
        self.zoning_lot_coverage = lot_coverage
        self.zoning_building_height = building_height
        self.zoning_min_front_setback = front_setback
        self.zoning_min_rear_setback = rear_setback
        self.zoning_min_side_setback = side_setback
        self.state = ''
        self.city = ''

def convertZoneInfoDictToZoneInfoObj(zoneInfo_dict):
    zoneInfoObj = ZoneInfo(zoneInfo_dict['zoning_url'],zoneInfo_dict['zoning_classification'],\
                            zoneInfo_dict['zoning_code'],zoneInfo_dict['zoning_far'],\
                            zoneInfo_dict['zoning_lot_coverage'],zoneInfo_dict['zoning_building_height'],\
                            zoneInfo_dict['zoning_min_front_setback'],zoneInfo_dict['zoning_min_rear_setback'],\
                            zoneInfo_dict['zoning_min_side_setback'])
    return zoneInfoObj


def callZoneomicsAPI(address):
    zone_resp = {'statusCode': 200,
                 'success': True,
                 'data': {'city_id': 3372,
                  'zone_code': 'R-60',
                  'zone_name': 'Single Family Residential',
                  'zone_type': 'Residential',
                  'zone_sub_type': 'Single Family',
                  'zone_guide': '',
                  'link': 'https://www.zoneomics.com/code/decatur-GA/chapter_3/#R-85',
                  'min_lot_area_sq_ft': '9000',
                  'min_lot_width_ft': '60',
                  'max_building_height_ft': '35',
                  'max_far': '0.4',
                  'max_coverage_percentage': '50',
                  'max_impervious_coverage_percentage': 'NA',
                  'min_front_yard_ft': 'NA',
                  'min_side_yard_ft': '10',
                  'min_side_yard_at_least_one_ft': 'NA',
                  'min_side_yard_both_ft': 'NA',
                  'min_rear_yard_ft': '30',
                  'min_landscaped_space_percentage': 'NA',
                  'open_space_percentage': 'NA',
                  'private_open_space_percentage': 'NA',
                  'notes': 'NA',
                  'far_link': 'NA',
                  'map_link': 'https://gis.interdev.com/cityofdecatur/',
                  'other_link': 'NA',
                  'maximum_far': '0.4',
                  'maximum_coverage': '50',
                  'zoing_table_link': 'https://library.municode.com/ga/decatur/codes/code_of_ordinances?nodeId=PTIVUNDEORDEGE_ART1GEPR_S1.2ZODI_1.2.1ESZODI',
                  'zoning_code_date': '23-Nov-22',
                  'minimum_lot_depth_ft': '120',
                  'minimum_lot_width_ft': '60',
                  'minimum_rear_yard_ft': '30',
                  'minimum_side_yard_ft': '10',
                  'minimum_lot_area_sq_ft': '9000',
                  'adu_permitted_municipal': 'No',
                  'max_density_du_per_acre': 'NA',
                  'building_height_definition': 'Height is measured as the vertical distance from the mean finished ground level at the front of the building to the highest point of a roof.',
                  'maximum_building_height_ft': 'Primary: 35, Accessory: (1 story: 16, 2 stories: 25)',
                  'maximum_density_du_per_acre': 'NA',
                  'minimum_building_area_sq_ft': 'NA',
                  'adu_permitted_state_override': 'No',
                  'maximum_building_height_stories': '3',
                  'lat': 33.7815388,
                  'lng': -84.3058161},
                 'message': []}
    zoning_url = zone_resp['data']['zoing_table_link']
    zoning_classification = zone_resp['data']['zone_type']
    zoning_code = zone_resp['data']['zone_code']
    zoning_far = zone_resp['data']['max_far']
    zoning_lot_coverage = zone_resp['data']['max_coverage_percentage']
    zoning_building_height = zone_resp['data']['max_building_height_ft']
    zoning_min_front_setback = zone_resp['data']['min_front_yard_ft']
    zoning_min_rear_setback = zone_resp['data']['min_rear_yard_ft']
    zoning_min_side_setback = zone_resp['data']['min_side_yard_ft']
    zoneInfoObj = ZoneInfo(zoning_url,zoning_classification,zoning_code,zoning_far,\
                          zoning_lot_coverage,zoning_building_height,zoning_min_front_setback,
                          zoning_min_rear_setback,zoning_min_side_setback)
    return zoneInfoObj


def searchKeyInSession(key_name,email_address):
    if email_address in session:
        session_entries_n = len(session[email_address])
        for i in range(session_entries_n):
            if(key_name in list(session[email_address][i].keys())):
                return True
    return False

def searchKeyIndexInSession(key_name,email_address):
    if email_address in session:
        session_entries_n = len(session[email_address])
        for i in range(session_entries_n):
            if(key_name in list(session[email_address][i].keys())):
                return i
    return -1

app = Flask(__name__)

app.secret_key = 'abcdef'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)
@app.route('/signup',methods=['POST'])
def signup():
    data = request.get_json()
    email_address = data['email']
    name = data['name']
    password = data['password']
    userObj = User()
    userObj.setUserBasic(email_address,password,name)
    user_dict = vars(userObj)
    userObj.printUser()
    
    if email_address not in session:
        session[email_address] = []
    session[email_address].append({'username':userObj.username})
    print(session[email_address])
    return jsonify({'status' : 'success'})

@app.route('/signin',methods=['POST'])
def signin():
    data = request.get_json()
    email_address = data['email']
    password = data['password']
    if email_address not in session:
        session[email_address] = []
    session[email_address].append({'username':email_address})
    return jsonify({'status' : 'success'})

@app.route('/signout',methods=['POST'])
def signout():
    data = request.get_json()
    email_address = data['email']
    if email_address in session:
        session.pop(email_address)
        session.modified = True
    return jsonify({'status' : 'success'})

@app.route('/checkstatus',methods=['POST'])
def checkSignInStatus():
    print('request received')
    
    data = request.get_json()
    email_address = data['email']
    if email_address in session:
        return jsonify({'status' : 'signedin'})
    return jsonify({'status' : 'not signedin'})

@app.route('/check',methods=['GET'])
def check():
    print('request received')
    data = request.get_json()
    email_address = data['email']
    print(session[email_address])
    return jsonify({'status' : 'success'})

@app.route('/populateDashBoard',methods=['GET'])
def populateDashBoard():
    data = request.get_json()
    email_address = data['email']
    min_area = data['min_area']
    max_area = data['max_area']
    bed_count = data['bed_count']
    full_bath_count = data['full_bath_count']
    half_bath_count = data['half_bath_count']
    total_bath_count = full_bath_count + 0.5*half_bath_count
    story_count = data['story_count']
    garage_count = data['garage_count']
    build_quality = data['build_quality'].upper()
    basement_type = data['basement_type'].upper()
    acquisition_cost = data['acquisition_cost']
    home_style = data['home_style'].upper()
    complete_address = data['complete_address']
    userInputObj = userInputForm(data['min_area'],data['max_area'],data['bed_count'],data['full_bath_count'],\
                                 data['half_bath_count'],data['story_count'],data['garage_count'],\
                                 data['build_quality'],data['basement_type'],data['acquisition_cost'],\
                                 data['home_style'],complete_address)

    userInputObj_dict = vars(userInputObj)
    if(searchKeyInSession('user_input',email_address)==False):
        print('User Input not in session. Appending')
        session[email_address].append({'user_input':userInputObj_dict})
        session.modified = True
    else:
        print('User Input in session. Updating')
        key_idx = searchKeyIndexInSession('user_input',email_address)
        session[email_address][key_idx].update({'user_input':userInputObj_dict})
        session.modified = True
        
    
    shortListedPlans = getShortListedPlans(home_style,userInputObj)
    plans_dict_arr = [vars(x) for x in shortListedPlans]
    print('Shortlisted plan count : ',len(shortListedPlans))

    if(searchKeyInSession('architectural_plans',email_address)==False):
        print('Plans not in session. Appending')
        session[email_address].append({'architectural_plans':plans_dict_arr})
        session.modified = True
    else:
        print('Plans in session. Updating')
        key_idx = searchKeyIndexInSession('architectural_plans',email_address)
        session[email_address][key_idx].update({'architectural_plans':plans_dict_arr})
        session.modified = True
    
    selectedPlanIdx = getSelectedPlanIdx(shortListedPlans, shortListedPlans[0].plan_number)
    selectedPlan = shortListedPlans[selectedPlanIdx]
    selectedPlan_dict = vars(selectedPlan)
    selectedPlanObj = convertPlanDictToPlanObj(selectedPlan_dict)
    query_prop = initializeQueryPropertyFromSelectedArchitectural(selectedPlanObj)

    if(searchKeyInSession('selected_architectural_plan',email_address)==False):
        print('Selected Plan not in session. Appending')
        session[email_address].append({'selected_architectural_plan':selectedPlan_dict})
        session.modified = True
    else:
        print('Selected Plan in session. Updating')
        key_idx = searchKeyIndexInSession('selected_architectural_plan',email_address)
        session[email_address][key_idx].update({'selected_architectural_plan':selectedPlan_dict})
        session.modified = True

    if(searchKeyInSession('comparables',email_address)==False):
        print('Comparables not in session. Appending')
        comp_resp = callToVoDataAPI(complete_address)
        cmp_items_arr = getComparablesObjsArray(comp_resp)
        cmp_items_dict_arr = [vars(x) for x in cmp_items_arr]
        session[email_address].append({'comparables':cmp_items_dict_arr})
        session.modified = True
    else:
        print('Comparables in session. Fetching')
        key_idx = searchKeyIndexInSession('comparables',email_address)
        cmp_items_arr = [convertComparableDictToComparableObj(comparable_dict) for comparable_dict in session[email_address][key_idx]['comparables']]
        
    comparables_adjst_prices = setAndGetAdjustedValuesofComparables(cmp_items_arr,query_prop)
    setVACofQueryPropertyObj(query_prop,cmp_items_arr,comparables_adjst_prices)
    cmpsIdx_used_for_VAC = getCompsIdxUsedforVAC(comparables_adjst_prices)
    cmps_key_idx = searchKeyIndexInSession('comparables',email_address)
    cmp_items_dict_arr = [vars(x) for x in cmp_items_arr]
    session[email_address][cmps_key_idx].update({'comparables':cmp_items_dict_arr})
    session.modified = True
    # query_prop.print()

    query_prop_dict = vars(query_prop)
    
    if(searchKeyInSession('query_prop',email_address)==False):
        print('Query Property not in session. Appending')
        session[email_address].append({'query_prop':query_prop_dict})
        session.modified = True
    else:
        print('Query Property in session. Updating')
        key_idx = searchKeyIndexInSession('query_prop',email_address)
        session[email_address][key_idx].update({'query_prop':query_prop_dict})
        session.modified = True 
    
    if(searchKeyInSession('parcel_info',email_address)==False):
        print('Parcel Info not in session. Appending')
        reGridRspObj = callReGridAPI(complete_address)
        reGridRspObj_dict = vars(reGridRspObj)
        session[email_address].append({'parcel_info':reGridRspObj_dict})
        session.modified = True
    else:
        print('Parcel Info in session. Fetching')
        key_idx = searchKeyIndexInSession('parcel_info',email_address)
        reGridRspObj = convertReGridResponseDictToRegridResponseObj(session[email_address][key_idx]['parcel_info'])

    userInputObj.addr_city = reGridRspObj.p_city 
    userInputObj.addr_state = reGridRspObj.p_state
    userInputObj_dict = vars(userInputObj)
    user_input_idx = searchKeyIndexInSession('user_input',email_address)
    session[email_address][user_input_idx].update({'user_input':userInputObj_dict})
    
    MSACC = predictConstructionCostFromModel(userInputObj.addr_state,userInputObj.addr_city,\
                                             build_quality,story_count,basement_type,query_prop.area)
    # print(MSACC)
    total_construction_cost = calculateTotalConstructionCost(MSACC, query_prop.area, query_prop.area_basement,\
                                                             query_prop.area_garage, basement_type, 0.55)
    total_project_cost = total_construction_cost+acquisition_cost
    equity = query_prop.vac - total_project_cost
    kpiObj = KPI(query_prop.vac,total_construction_cost,acquisition_cost)
    # kpiObj.print()
    kpiObj_dict = vars(kpiObj)
    if(searchKeyInSession('kpi',email_address)==False):
        print('KPI not in session. Appending')
        session[email_address].append({'kpi':kpiObj_dict})
        session.modified = True
    else:
        print('KPI in session. Updating')
        key_idx = searchKeyIndexInSession('kpi',email_address)
        session[email_address][key_idx].update({'kpi':kpiObj_dict})
        session.modified = True

    if(searchKeyInSession('zoning_info',email_address)==False):
        print('zoning_info not in session. Appending')
        zoneInfoObj = callZoneomicsAPI(complete_address)
        zoneInfoObj.city = reGridRspObj.p_city 
        zoneInfoObj.state = reGridRspObj.p_state
        zoneInfoObj_dict = vars(zoneInfoObj)
        session[email_address].append({'zoning_info':zoneInfoObj_dict})
        session.modified = True
    else:
        print('Zoning Info in session. Fetching')
        key_idx = searchKeyIndexInSession('zoning_info',email_address)
        zoneInfoObj = convertZoneInfoDictToZoneInfoObj(session[email_address][key_idx]['zoning_info'])

    if(searchKeyInSession('cmps_used_for_vac',email_address)==False):
        cmpsIdx_used_for_VAC = getCompsIdxUsedforVAC(comparables_adjst_prices)
        session[email_address].append({'cmps_used_for_vac':cmpsIdx_used_for_VAC})
    else:
        key_idx = searchKeyIndexInSession('cmps_used_for_vac',email_address)
        session[email_address][key_idx].update({'cmps_used_for_vac':cmpsIdx_used_for_VAC})

    dashboard_resp = {}
    dashboard_resp['address'] = complete_address
    dashboard_resp['user_input'] = userInputObj_dict
    dashboard_resp['parcel_info'] = reGridRspObj_dict
    dashboard_resp['architectural_plans'] = plans_dict_arr
    dashboard_resp['selected_plan'] = selectedPlan_dict
    dashboard_resp['kpi'] = kpiObj_dict
    dashboard_resp['zoning_info'] = zoneInfoObj_dict
    return jsonify({'data' : dashboard_resp})

@app.route('/changeArchitecturalPlan',methods=['GET'])
def changeArchitecturalPlan():
    data = request.get_json()
    email_address = data['email']
    plan_number = data['plan_number']
    # return jsonify({'status' : 'success'})
    # plans_arr = session[email_address][1][]
    archi_plans_idx = searchKeyIndexInSession('architectural_plans',email_address)
    plan_count = len(session[email_address][archi_plans_idx]['architectural_plans'])
    for i in range(plan_count):
        if(session[email_address][archi_plans_idx]['architectural_plans'][i]['plan_number'] == plan_number):
            selected_plan_dict = session[email_address][archi_plans_idx]['architectural_plans'][i]
    # print(plans_arr)
    selectedPlanObj = convertPlanDictToPlanObj(selected_plan_dict)
    # session[email_address].pop()
    selected_archi_plan_idx = searchKeyIndexInSession('selected_architectural_plan',email_address)
    session[email_address][selected_archi_plan_idx].update({'selected_architectural_plan':selected_plan_dict})
    session.modified = True

    comps_idx = searchKeyIndexInSession('comparables',email_address)
    new_cmp_items_arr = [convertComparableDictToComparableObj(comparable_dict) 
                         for comparable_dict in session[email_address][comps_idx]['comparables']]
    new_query_prop = initializeQueryPropertyFromSelectedArchitectural(selectedPlanObj)
    
    new_comparables_adjst_prices = setAndGetAdjustedValuesofComparables(new_cmp_items_arr,new_query_prop)
    setVACofQueryPropertyObj(new_query_prop,new_cmp_items_arr,new_comparables_adjst_prices)
    new_cmpsIdx_used_for_VAC = getCompsIdxUsedforVAC(new_comparables_adjst_prices)
    comps_for_vac_idx = searchKeyIndexInSession('cmps_used_for_vac',email_address)
    session[email_address][comps_for_vac_idx].update({'cmps_used_for_vac':new_cmpsIdx_used_for_VAC})
    new_query_prop.print()

    new_query_prop_dict = vars(new_query_prop)
    query_prop_idx = searchKeyIndexInSession('query_prop',email_address)
    session[email_address][query_prop_idx].update({'query_prop':new_query_prop_dict})
    session.modified = True


    kpi_idx = searchKeyIndexInSession('kpi',email_address)
    changedKPIObj = KPI(new_query_prop.vac,session[email_address][kpi_idx]['kpi']['construction_cost'],\
                      session[email_address][kpi_idx]['kpi']['acquisition_cost'])
    changedKPIObj_dict = vars(changedKPIObj)
    session[email_address][kpi_idx].update({'kpi':changedKPIObj_dict})
    session.modified = True
    
    return jsonify({'kpi' : changedKPIObj_dict})
    
@app.route('/changeBuildQuality',methods=['GET'])
def changeBuildQuality():
    data = request.get_json()
    email_address = data['email']
    build_quality = data['build_quality']
    kpi_idx = searchKeyIndexInSession('kpi',email_address)
    kpi_dict = session[email_address][kpi_idx]['kpi']
    # print(kpi_dict)
    # session['email_address'][1]['user_input']['addr_state'],session['email_address'][1]['user_input']['addr_city'],build_quality,\
    # session['email_address'][1]['user_input']['story_count'],session['email_address'][1]['user_input']['basement_type'],q_prop.area
    user_input_idx = searchKeyIndexInSession('user_input',email_address)
    addr_state = session[email_address][user_input_idx]['user_input']['addr_state']
    addr_city = session[email_address][user_input_idx]['user_input']['addr_city']
    story_count = session[email_address][user_input_idx]['user_input']['story_count']
    basement_type = session[email_address][user_input_idx]['user_input']['basement_type']

    session[email_address][user_input_idx]['user_input'].update({'build_quality':build_quality})
    session.modified = True

    # user_input_idxx = searchKeyIndexInSession('user_input',email_address)
    # print('User Input Idx in session : ',user_input_idxx)
    
    # print('user build quality : ',  build_quality)
    # print('build quality in session : ',session[email_address][user_input_idxx]['user_input']['build_quality'])
    

    query_prop_idx = searchKeyIndexInSession('query_prop',email_address)
    area = session[email_address][query_prop_idx]['query_prop']['area']
    area_basement = session[email_address][query_prop_idx]['query_prop']['area_basement']
    area_garage = session[email_address][query_prop_idx]['query_prop']['area_garage']
    
    MSACC = predictConstructionCostFromModel(addr_state,addr_city,build_quality,story_count,basement_type,area)
    print(MSACC)
    total_construction_cost = calculateTotalConstructionCost(MSACC, area, area_basement,\
                                                             area_garage, basement_type, 0.55)
    kpi_idx = searchKeyIndexInSession('kpi',email_address)
    changedKPIObj = KPI(session[email_address][kpi_idx]['kpi']['vac'],total_construction_cost,\
                      session[email_address][kpi_idx]['kpi']['acquisition_cost'])
    changedKPIObj_dict = vars(changedKPIObj)
    session[email_address][kpi_idx].update({'kpi':changedKPIObj_dict})
    session.modified = True
    kpi_dict = session[email_address][kpi_idx]['kpi']
    return jsonify({'kpi' : kpi_dict})

@app.route('/getComparables',methods=['GET'])
def getComparables():
    data = request.get_json()
    email_address = data['email']
    if email_address in session:
        key_idx = searchKeyIndexInSession('comparables',email_address)
        if(key_idx !=-1):
            cmps_response = session[email_address][key_idx]['comparables']
            return jsonify({'comparables' : cmps_response})
        else:
            return jsonify({'status' : 'Failed. No comparables found'})
    return jsonify({'status' : 'Failed. You are not signed in'})

@app.route('/getSessionObj',methods=['GET'])
def getSessionObj():
    data = request.get_json()
    email_address = data['email']
    return jsonify({'data' : session[email_address]})


@app.route('/generateReport',methods=['GET'])
def generateReport():
    data = request.get_json()
    email_address = data['email']
    receiver_email = data['receiver_email']
    return jsonify({'status' : 'success'})
    
    
    
app.run()