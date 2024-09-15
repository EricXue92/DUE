from datetime import datetime
import json
import pathlib
import random
import torch
import numpy as np

# 设置np.random.seed(seed) 和 torch.manual_seed(seed), 重复实验
def set_seed(seed):
    if seed is None:
        seed = random.randint(0, 1000)
    np.random.seed(seed)
    torch.manual_seed(seed)
    return seed

# # Create a Path object for the "runs" directory 
# 为 runs 文件夹建立 路径对象 并建立文件夹

# path = pathlib.Path("runs")
# # Check if the path exists
# if path.exists():
#     print(f"The path {path} exists.")
# else:
#     print(f"The path {path} does not exist.")
#     # Create the directory if it does not exist # 创建路径path.mkdir() 
#     path.mkdir()
#     print(f"Directory {path} created.")

# 创建文件夹路径（默认路径+时间）
def get_results_directory(name, stamp = True):
    # 2024-06-30-Sunday-20-22-46
    timestamp = datetime.now().strftime("%Y-%m-%d-%A-%H-%M-%S")
    # 建立一个 路径对象 
    results_dir = pathlib.Path("runs")
    # name 默认为 default
    if name is not None:
        results_dir = results_dir / name
    # 新的文件路径 "runs/2024-06-30-Sunday-20-22-46"
    results_dir = results_dir / timestamp if stamp else results_dir
    # Create the directory and any missing parent directories
    results_dir.mkdir(parents=True)
    return results_dir

# The Hyperparameters class manages hyperparameters for a model, 
# allowing them to be easily saved, loaded, and updated. 
# It supports initialization from a file and dynamic updates via keyword arguments.
class Hyperparameters:
    # It can load hyperparameters from a file if a path is provided as the first argument.
    # Updates with any additional keyword arguments provided.
    def __init__(self, *args, **kwargs):
        #if len(args) == 1 and isinstance(args[0], Path):
            # self.load(args[0])
        if len(args) == 1:
            self.load(args[0])
        ##### 
        self.from_dict(kwargs)

    # convert hyperparameters to dictionary
    
    # class ExampleClass:
    #     def __init__(self, name, value):
    #         self.name = name
    #         self.value = value
    #     def to_dict(self):
    #         return vars(self)

    # example = ExampleClass(name="example", value=42)
    # example_dict = example.to_dict()
    # print(example_dict)  # Output: {'name': 'example', 'value': 42}

    #  Converts the hyperparameters into a dictionary format using vars(self)
    def to_dict(self):
        return vars(self) 

    # This method will dynamically set the attributes of MyClass instances 
    # based on the key-value pairs in the dictionary. 
    ###### 把一个字典的键值对 自动转换成 对象的属性
    def from_dict(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    # class MyClass:
    #     def from_dict(self, dictionary):
    #         for k, v in dictionary.items():
    #             setattr(self, k, v)
    # data = {
    #     "name": "Alice",
    #     "age": 30,
    #     "occupation": "Engineer"
    # }
    # obj = MyClass()
    # obj.from_dict(data)
    # print(obj.name)       # Alice
    # print(obj.age)        # 30
    # print(obj.occupation) # Engineer

    # Converts the hyperparameters to a JSON-formatted string for easy readability and storage
    def to_json(self):
        return json.dumps( self.to_dict(), indent = 4, sort_keys = True)

    # Saves the hyperparameters to a specified path in JSON format.
    def save(self, path):
        path.write_text( self.to_json() )
        
    # Loads hyperparameters from a JSON file and updates the object's attributes
    def load(self, path):
        if not isinstance(path, Path):
            path = Path(path)
        self.from_dict( json.loads( path.read_text() ) )
        
    #Checks if a hyperparameter exists using the hasattr function
    def __contains__(self, k):
        return hasattr(self, k)

    # rovides a readable string representation of the hyperparameters in JSON format
    def __str__(self):
        return f"Hyperparameters:\n { self.to_json() }"

''' 
# Create hyperparameters from a dictionary
hyperparams = Hyperparameters(learning_rate=0.01, batch_size=32)

# Save hyperparameters to a file
hyperparams.save( Path('hyperparams.json') ) # 建立一个hyperparams.json的文件, 并保存相关参数

# Load hyperparameters from a file
loaded_hyperparams = Hyperparameters(Path('hyperparams.json'))

# Print hyperparameters
print(loaded_hyperparams)

'''