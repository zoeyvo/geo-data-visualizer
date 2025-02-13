# Organizing the CSV file and Extracting location
# Store to Json files for now. Will be database later
import os

# Need to install spaCy and its model: en_core_web_trf (https://spacy.io/usage)

# This code takes 10+ mins to run :(
# Results already in the 2 Json files

import pandas as pd
import spacy
import json

# Temporary structure to visualize data for now
# expert_profiles.json
class Profile:
  def __init__(self, name):
    self.name = name
    self.works = list()
    self.locations = list()
    
  def addWork(self, title, abstract):
    self.works.append(Work(title, abstract))
    
  def addLocation(self, location):
    self.locations.append(location)
    
def profileToJson(profile: Profile):
  worksJson = []
  for work in profile.works:
    worksJson.append({"title" : work.title, "abstract" : work.abstract})
  
  return {
    "works": worksJson,
    "locations": profile.locations
  }
  
# Temporary structure to visualize data for now
# location_based_profiles.json
class GeoProfileMapping:
  def __init__(self, name, location):
    self.name = name
    self.location = location
    self.relatedWorks = list()
    self.matchesCount = 0
    
  def addRelatedWork(self, title, abstract):
    self.relatedWorks.append(Work(title, abstract))
    self.matchesCount += 1
    
def geoProfileMappingToJson(mapping: GeoProfileMapping):
  worksJson = []
  for work in mapping.relatedWorks:
    worksJson.append({"title" : work.title, "abstract" : work.abstract})
  
  return {
    "matches" : mapping.matchesCount,
    "works" : worksJson
  }
  
class Work:
  def __init__(self, title, abstract):
    self.title = title
    self.abstract = abstract
    
  
nlp = spacy.load("en_core_web_trf")
file_path = os.path.join(os.pardir, os.pardir, "expert_profiles.csv")
file_path = os.path.abspath(file_path)  # Convert to absolute path if needed

data = pd.read_csv(file_path)
data = data.fillna('')

# Temporary storage. Convert to database later
profiles = dict()       # Expert's name : Profile
locations = dict()      # Location : dict of (Expert's name : GeoProfileMapping)

# Iterate through each line of CSV file
for _, row in data.iterrows():
  name = row["Name"]
  title = row["title"]
  abstract = row["abstract"]
  
  # Add work to correspoding expert's profile
  if name not in profiles:
    profiles[name] = Profile(name)
  profiles[name].addWork(title, abstract)
  
  # Extract location
  txt = nlp(title + ". " + abstract)
  processedLocation = set()
  for ent in txt.ents:
    if ent.label_ == "GPE":
      geo = ent.text
      
      # Handle when a location appears multiple times in a text
      if geo in processedLocation:
        continue
      else:
        processedLocation.add(geo)
      
      # Add location to corresponding expert's profile
      profiles[name].addLocation(geo)
      
      # For location-based-expert_profiles.json:
      # Initialize location/expert if necessary
      if geo not in locations:
        locations[geo] = dict()
      if name not in locations[geo]:
        locations[geo][name] = GeoProfileMapping(name, geo)
      
      # Add matching work to location
      locations[geo][name].addRelatedWork(title, abstract)
      
  
with open("data/json/expert_profiles.json", "w") as file_profiles:
  json.dump(profiles, file_profiles, default=profileToJson, indent=2)
  
with open("data/json/location_based_profiles.json", "w") as file_locations:
  json.dump(locations, file_locations, default=geoProfileMappingToJson, indent=2)
