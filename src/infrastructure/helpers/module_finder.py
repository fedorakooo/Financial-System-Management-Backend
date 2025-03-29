import os


class ModuleFinder:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def get_modules(self) -> list:
        """"Searches for all Python files in the specified directory and its subdirectories."""

        module_paths = []

        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    module_path = os.path.relpath(os.path.join(root, file), self.base_directory)
                    module_name = module_path.replace(os.path.sep, ".")[:-3]  # Убираем .py
                    module_paths.append(self.base_directory + "." + module_name)

        return module_paths
