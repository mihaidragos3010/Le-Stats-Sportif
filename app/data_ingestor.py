import csv

# The class responsible for reading the data.
class DataIngestor:

    def __init__(self, csv_path: str):

        self.init_struct(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    # Reading a statistical file into a list of dictionaries.
    def init_struct(self, csv_path: str) -> None:
        self.data_bases = []
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader: 
                self.data_bases.append(row)


    def isBestMaxQuestion(self, question: str) -> bool:
        return question in self.questions_best_is_max
    
    def isBestMinQuestion(self, question: str) -> bool:
        return question in self.questions_best_is_min
        
    
        



                
                





                
            

            


