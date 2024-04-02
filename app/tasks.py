import json
from threading import Event
from app.data_ingestor import DataIngestor

# This is a class representing the implementation of a task from the server.
class Task():

    def __init__(self) -> None:
        pass

    def __init__(self, job_id: int, data_ingestor: DataIngestor) -> None:
        self.job_id = job_id
        self.data_ingestor = data_ingestor
        self.result = None
        self.isDone = Event()
        self.isDone.clear()

    # Each subclass will need to implement its own execution implementation.
    def execute(self):
        raise Exception("Task class can't make an action!!")
    
    # The function saves the result of the task into a file.
    def save_to_file(self):
        with open(f"./results/result{self.job_id}.txt", "w") as file:
            json.dump(self.result, file)
            self.isDone.set()

    # The function contains an atomic operation that checks if the task is finished.
    def isFinish(self):
        return self.isDone.is_set()
    
    # The function is used to make the main thread wait until the completion of this task.
    def waitToFinish(self):
        self.isDone.wait()

    
# The class calculates the average for each state.
class TaskStatesMean(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]

    def execute(self):

        collector = {}
        question = self.question
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:

                state = line["LocationDesc"]
                value = float(line["Data_Value"])
                if state in collector:
                    old_value, count = collector[state]
                    collector[state] = (old_value + value, count + 1)
                else:
                    collector[state] = (value, 1)

        result = {}
        for state, (value,count) in collector.items():
            result[state] = value / count

        sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
        self.result = sorted_result 


# The class calculates the average for only one state.
class TaskOneStateMean(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]
        self.state = data["state"]

    def execute(self):

        sum = 0
        count = 0
        question = self.question
        state = self.state
        for line in self.data_ingestor.data_bases:

            if question == line["Question"] and state == line["LocationDesc"]:
                sum += float(line["Data_Value"])
                count += 1

        result = {}
        result[state] = sum / count

        self.result = result


# The class displays the top 5 best states for the given query.
class TaskBestFive(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]
        self.isBestMax = data_ingestor.isBestMaxQuestion(self.question)

    def execute(self):

        collector = {}
        question = self.question
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:

                state = line["LocationDesc"]
                value = float(line["Data_Value"])
                if state in collector:
                    old_value, count = collector[state]
                    collector[state] = (old_value + value, count + 1)
                else:
                    collector[state] = (value, 1)

        result = {}
        for state, (value,count) in collector.items():
            result[state] = value / count

        #I check the type of the question to determine whether to sort in ascending or descending order.
        top_5_result = {}
        if self.isBestMax:
            sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
            top_5_result = {k: v for k, v in list(sorted_result.items())[:5]}
        else:
            sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
            top_5_result = {k: v for k, v in list(sorted_result.items())[:5]}

        self.result = top_5_result


# The class displays the 5 worst states for the given query.
class TaskWorstFive(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]
        self.isBestMax = data_ingestor.isBestMaxQuestion(self.question)

    def execute(self):

        collector = {}
        question = self.question
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:

                state = line["LocationDesc"]
                value = float(line["Data_Value"])
                if state in collector:
                    old_value, count = collector[state]
                    collector[state] = (old_value + value, count + 1)
                else:
                    collector[state] = (value, 1)

        result = {}
        for state, (value,count) in collector.items():
            result[state] = value / count

        # I check the type of the question to determine whether to sort in ascending or descending order.
        worst_5_result = {}
        if self.isBestMax:
            sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
            worst_5_result = {k: v for k, v in list(sorted_result.items())[:5]}
        else:
            sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
            worst_5_result = {k: v for k, v in list(sorted_result.items())[:5]}

        self.result = worst_5_result


# The class calculates the global average.
class TaskGlobalMean(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]

    def execute(self):

        sum = 0
        count = 0
        question = self.question
        for line in self.data_ingestor.data_bases:
            if question == line["Question"]:
                sum += float(line["Data_Value"])
                count += 1
                
        result = {"global_mean": sum / count}
        self.result = result
    

# The class calculates the difference from the global average for each state.
class TaskDiffFromMean(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]

    def execute(self):

        collector = {}

        global_sum = 0
        global_count = 0        
        question = self.question
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:
                
                state = line["LocationDesc"]
                value = float(line["Data_Value"])
                if state in collector:
                    old_value, count = collector[state]
                    collector[state] = (old_value + value, count + 1)
                else:
                    collector[state] = (value, 1)
                
                global_sum += value
                global_count += 1

        result = {}
        for state, (value,count) in collector.items():
            result[state] = (global_sum / global_count) - (value / count)

        sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
        self.result = sorted_result
    

# The class calculates the difference from the global average for each state.
class TaskStateDiffFromMean(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]
        self.state = data["state"]

    def execute(self):

        state_sum = 0
        state_count = 0
        global_sum = 0
        global_count = 0
        question = self.question
        state = self.state
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:
            
                if state == line["LocationDesc"]:
                    state_sum += float(line["Data_Value"])
                    state_count += 1

                global_sum += float(line["Data_Value"])
                global_count += 1

        result = {state: (global_sum / global_count) - (state_sum / state_count)}

        self.result = result
    

# The class calculates the average for each category separately and for each state.
class TaskMeanByCategory(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]

    def execute(self):

        collector = {}
        question = self.question
        for line in self.data_ingestor.data_bases:

            if question == line["Question"]:

                state = line["LocationDesc"]
                category = line["StratificationCategory1"]
                subCategory = line["Stratification1"]
                value = float(line["Data_Value"])
                if category == '' or subCategory =='':
                    continue

                key = (state,category,subCategory)
                if key in collector:
                    old_value, count = collector[key]
                    collector[key] = (old_value + value, count + 1)
                else:
                    collector[key] = (value, 1)

        result = {}
        for key, (value,count) in collector.items():
            result[key] = value / count

        sorted_result = dict(sorted(result.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])))
        self.result = self.convert_tuple_keys_to_string(sorted_result)

    # I got an error, and I had to convert each tuple in the keys into strings.
    def convert_tuple_keys_to_string(self, dict):
        return {str(key): value for key, value in dict.items()}


# The class calculates the average for each category separately and for a specific state.
class TaskStateMeanByCategory(Task):

    def __init__(self, job_id: int, data: dict, data_ingestor: DataIngestor) -> None:
        super().__init__(job_id, data_ingestor)
        self.question = data["question"]
        self.state = data["state"]

    def execute(self):

        collector = {}
        question = self.question
        state = self.state
        for line in self.data_ingestor.data_bases:

            if question == line["Question"] and state == line["LocationDesc"]:

                category = line["StratificationCategory1"]
                subCategory = line["Stratification1"]
                value = float(line["Data_Value"])
                if category == '' or subCategory =='':
                    continue

                key = (category,subCategory)
                if key in collector:
                    old_value, count = collector[key]
                    collector[key] = (old_value + value, count + 1)
                else:
                    collector[key] = (value, 1)

        result = {}
        for key, (value,count) in collector.items():
            result[key] = value / count

        sorted_result = dict(sorted(result.items(), key=lambda x: (x[0][0], x[0][1])))
        self.result = {self.state: self.convert_tuple_keys_to_string(sorted_result)}

    # I got an error, and I had to convert each tuple in the keys into strings.
    def convert_tuple_keys_to_string(self, dict):
        return {str(key): value for key, value in dict.items()}
    
