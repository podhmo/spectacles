from spectacles.config_parse import read_config_file

def main():
    context = read_config_file("./demo.cfg")
    modules = context["finding"]["action"]("models.py")
    print list(context["source"]["model_collector"](modules[0]))

if __name__ == "__main__":
    main()
