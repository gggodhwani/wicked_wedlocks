import csv
import glob
import simplejson
CSV_DATA_FOLDER = "assets/data/csv/"
DISTRICT_OUT_FILE = "assets/data/json/district_data.json"
STATES_OUT_FILE = "assets/data/json/states_data.json"
DEFAULT_DISTRICT_CODE = "000"
FEMALE_AGE_LIMIT = "18"
MALE_AGE_LIMIT = "21"

'''
DATA FIELDS DESCRIPTION
tf : Total number of female citizens under age 18
mf : Currently married female citizens under age 18
wf : Widowed female citizens under age 18
sf : Separated female citizens under age 18
df : Divorced female citizens under age 18
rf : Ratio of female citizens undergone child marriage to the total female population under age 18
tm : Total number of male citizens under age 21
mm : Currently married male citizens under age 21
wm : Widowed male citizens under age 21
sm : Separated male citizens under age 21
dm : Divorced male citizens under age 21
rm : Ratio of male citizens undergone child marriage to the total male population under age 21
'''

class DataTransformer(object):
    ''' Ingests all the CSV files and transforms these to a single JSON file for all indian districts and states
    '''

    def __init__(self):
        self.districts_data_map = {}
        self.states_data_map = {}
        self.populate_data_maps()

    def get_csv_filenames_from_dir(self, dir_name):
        return glob.glob("%s*.csv" % dir_name)

    def populate_data_maps(self):
            csv_filename_list = self.get_csv_filenames_from_dir(CSV_DATA_FOLDER) 
            for csv_filename in csv_filename_list:
                with open(csv_filename, "rb") as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    next(csv_reader, None)  # skip the headers
                    for row in csv_reader:
                        if not "Less than" in row[4]: 
                            continue
                        if row[1] == DEFAULT_DISTRICT_CODE:
                            self.populate_area_data(0, self.states_data_map, row)
                        else:
                            self.populate_area_data(1, self.districts_data_map, row)

    def populate_area_data(self, area_type_id, area_map, row):
        area_key = int(row[area_type_id]) 
        if not area_key in area_map:
            area_map[area_key] = {}
        region_type = row[3][0].lower()
        if not region_type in area_map[area_key]:
            area_map[area_key][region_type] = {}
        if FEMALE_AGE_LIMIT in row[4]:
            area_map[area_key][region_type]["tf"] = int(row[7])
            area_map[area_key][region_type]["mf"] = int(row[13])
            area_map[area_key][region_type]["wf"] = int(row[16])
            area_map[area_key][region_type]["sf"] = int(row[19])
            area_map[area_key][region_type]["df"] = int(row[21])
            if area_map[area_key][region_type]["tf"] == 0:
                area_map[area_key][region_type]["rf"] = 0
            else:
                area_map[area_key][region_type]["rf"] = round(((float(row[13]) + float(row[16]) + float(row[19]) + float(row[21]))/float(row[7])), 4)
        elif MALE_AGE_LIMIT in row[4]:
            area_map[area_key][region_type]["tm"] = int(row[6])
            area_map[area_key][region_type]["mm"] = int(row[12])
            area_map[area_key][region_type]["wm"] = int(row[15])
            area_map[area_key][region_type]["sm"] = int(row[18])
            area_map[area_key][region_type]["dm"] = int(row[20])
            if area_map[area_key][region_type]["tm"] == 0:
                area_map[area_key][region_type]["rm"] = 0
            else:
                area_map[area_key][region_type]["rm"] = round(((float(row[12]) + float(row[15]) + float(row[18]) + float(row[20]))/float(row[6])), 4)
         
    def generate_data_files(self):
        with open(STATES_OUT_FILE, "wb") as out_file:
            simplejson.dump(self.states_data_map, out_file)
        with open(DISTRICT_OUT_FILE, "wb") as out_file:
            simplejson.dump(self.districts_data_map, out_file)

if __name__ == '__main__':
    obj = DataTransformer() 
    obj.generate_data_files()         
