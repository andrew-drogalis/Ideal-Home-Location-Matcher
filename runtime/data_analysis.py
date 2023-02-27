import json
from runtime.utilities.calculation_utilities import location_radius_search, check_coordinates_distance
from runtime.utilities.state_abbreviations import states_abbreviation_list
from thefuzz import process

class IdealHomeDataAnalysis():

    """ For Full Methodology: https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher/wiki """

    def __init__(self):
        
        # Import Natural Disaster Ranked Data
        with open('./data_ranking/ranked_data/State_Natural_Disaster_Ranked_Data.json', newline='') as f: 
            self.state_natural_disaster_data = json.load(f)

        # Import Weather Ranked Data
        with open('./data_ranking/ranked_data/Weather_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_weather_data = json.load(f)

        # Import Zipcode Prefix Ranked Data
        with open('./data_ranking/ranked_data/Zipcode_Prefix_Ranked_Data.json', newline='') as f: 
            self.zipcode_prefix_data = json.load(f)

        # Import Zipcode Ranked Data
        with open('./data_ranking/ranked_data/Zipcode_Ranked_Data.json', newline='') as f: 
            self.zipcode_data = json.load(f)

        # Import Zipcode Coordinate Data
        with open('./data_ranking/ranked_data/Zipcode_Coordinates_Data.json', newline='') as f: 
            self.zipcode_coordinate_data = json.load(f)

        # List of all Zipcode Coordinates - Not State Specific
        self.merged_zipcode_coordinate_data = [zipcode for state_coordinate_list in [*self.zipcode_coordinate_data.values()] for zipcode in state_coordinate_list]

        # Store Coordinates of Family & Work Locations
        self.saved_coordinates_list = [[], [], []]


    def find_middle_distance(self):

        if self.saved_coordinates_list[0] and self.saved_coordinates_list[1] and not self.saved_coordinates_list[2]:
            return check_coordinates_distance(self.saved_coordinates_list[0], self.saved_coordinates_list[1])
    
        elif self.saved_coordinates_list[0] and self.saved_coordinates_list[2] and not self.saved_coordinates_list[1]:
            return check_coordinates_distance(self.saved_coordinates_list[0], self.saved_coordinates_list[2])

        elif self.saved_coordinates_list[0] and self.saved_coordinates_list[1] and self.saved_coordinates_list[2]:
            return check_coordinates_distance(self.saved_coordinates_list[0], self.saved_coordinates_list[1], self.saved_coordinates_list[2])

        return 0


    def family_details_frame_1b(self, **kwargs):
        
        
        self.frame1b_results = ''


    def work_frame_2(self, **kwargs):
        
        if self.saved_coordinates_list[0]:
            # Send All Zipcode Data
            results_citys = location_radius_search(max_distance=max_distance, city_search_list=self.merged_zipcode_coordinate_data,
                coordinate_1=self.saved_coordinates_list[0], coordinate_2=self.saved_coordinates_list[1])
        
            self.frame1_results = results_citys
        else:
            self.frame1_results = [*self.merged_zipcode_coordinate_data]

        self.frame2_results = ''


    def income_frame_3(self):
        
        
        self.frame3_results = ''


    def area_classification_frame_4(self, **kwargs):
        
        
        self.frame4_results = ''


    def weather_frame_5(self, **kwargs):
        
        
        self.frame5_results = ''


    def natural_disaster_risk_frame_6(self, **kwargs):
       
       self.frame6_results = ''

    def results_frame_7(self):
       

       return {}

    def city_name_zipcode_matcher(self, state: str = '', city: str = '', zipcode: str = '', index: int = 0):
        # Catch Errors
        if not state:
            return 'Provide State'

        if not city and not zipcode:
            return 'Provide City or Zipcode'

        # Check Full State Name Provided
        if state in [*states_abbreviation_list.values()]:
            state_coordinate_list = self.zipcode_coordinate_data[state]

        # Check Abbreviated State Name Provided
        elif state.upper() in [*states_abbreviation_list.keys()]:
            state = states_abbreviation_list[state.upper()]
            state_coordinate_list = self.zipcode_coordinate_data[state]
        else:
            result = process.extractOne(state, [*states_abbreviation_list.values()])
            if int(result[1]) > 90:
                state = result[0]
                state_coordinate_list = self.zipcode_coordinate_data[state]
            else:
                return 'Please Provide Valid US State'

        # List of All Cities in State
        state_city_names = [[*city.keys()][0] for city in state_coordinate_list]

        if zipcode:
            for city_name in state_city_names:
                if zipcode in city_name:
                    state_city_name = city_name
                    primary_city_result = city_name.split(', ')[0]
                    break
            else:
                return 'Please Provide Valid Zipcode'

        elif city:
            # Fuzzy Match City 
            city_result = process.extract(city, state_city_names)
            primary_city_list = []
            for city_str in city_result:
                common_city_names = city_str[0].split(', ')
                primary_city_list.append(common_city_names[0])
            primary_city_result = process.extract(city, primary_city_list)
            # Compare Primary City with Common City Names
            if city_result[0][1] >= primary_city_result[0][1]:
                state_city_name = city_result[0][0]
                common_city_names = state_city_name.split(', ')
                primary_city_result = process.extract(city, common_city_names)[0][0]
            else:
                primary_city_result = primary_city_result[0][0]
                state_city_name = city_result[primary_city_list.index(primary_city_result)][0]
            zipcode = state_city_name.split(', ')[-1]
        
        self.saved_coordinates_list[index] = state_coordinate_list[state_city_names.index(state_city_name)][state_city_name]

        return f'{primary_city_result}, {state} {zipcode}'