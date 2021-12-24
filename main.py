from utils.onlyOneType import ParseData
from utils.validator import ValidateInput
import sys


if __name__ == "__main__":
    neededInput = sys.argv

    vdator = ValidateInput(neededInput)
    data = vdator.validateArgv()
    if data == False:
        print("Cant Proceed Data")
    else:
        print()
        parseData = ParseData(data["data"])
        returned = parseData.mainProccess(data["year"],data["type"])
        parseData.writeJsonedFile(returned)
    