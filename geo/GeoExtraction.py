# Organizing the CSV file and Extracting location
# Store to Json files for now. Will be database later

# Need to install spaCy and its model: en_core_web_trf (https://spacy.io/usage)

# This code takes 10+ mins to run :(
# Results already in the 2 Json files

import pandas as pd
import spacy
import json

# Temporary structure to visualize data for now
# profiles.json
class Profile:
  def __init__(self, name):
    self.name = name
    self.titles = list()
    self.locations = list()
    
  def addTitle(self, title):
    self.titles.append(title)
    
  def addLocation(self, location):
    self.locations.append(location)
    
def profileToJson(profile: Profile):
  return {
    "titles": profile.titles,
    "locations": profile.locations
  }
  
# Temporary structure to visualize data for now
# locations.json
class GeoProfileMapping:
  def __init__(self, name, location):
    self.name = name
    self.location = location
    self.relatedWork = list()
    self.matchesCount = 0
    
  def addRelatedWork(self, work):
    self.relatedWork.append(work)
    self.matchesCount += 1
    
def geoProfileMappingToJson(mapping: GeoProfileMapping):
  return {
    "matches" : mapping.matchesCount,
    "works" : mapping.relatedWork
  }
    
  
nlp = spacy.load("en_core_web_trf")
data = pd.read_csv("geoset_capstone_init.csv")

# Temporary storage. Convert to database later
profiles = dict()       # Expert's name : Profile
locations = dict()      # Location : dict of (Expert's name : GeoProfileMapping)

# Iterate through each line of CSV file
for _, row in data.iterrows():
  name = row["Name"]
  title = row["title"]
  
  # Add title to correspoding expert's profile
  if name not in profiles:
    profiles[name] = Profile(name)
  profiles[name].addTitle(title)
  
  # Extract location
  txt = nlp(title)
  for ent in txt.ents:
    if ent.label_ == "GPE":
      geo = ent.text
      
      # Add location to corresponding expert's profile
      profiles[name].addLocation(geo)
      
      # For locations.json:
      # Initialize location/expert if necessary
      if geo not in locations:
        locations[geo] = dict()
      if name not in locations[geo]:
        locations[geo][name] = GeoProfileMapping(name, geo)
      
      # Add matching work to location
      locations[geo][name].addRelatedWork(title)
      
  
with open("profiles.json", "w") as file_profiles:
  json.dump(profiles, file_profiles, default=profileToJson, indent=2)
  
with open("locations.json", "w") as file_locations:
  json.dump(locations, file_locations, default=geoProfileMappingToJson, indent=2)
