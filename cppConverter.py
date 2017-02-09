# Aaron Robeson
# CS3200 Spring 2017
# Feb 7

import sys
import re

# This global variable will keep track of the current indentation level as indicated by parsed opening and closing braces {}
indentLevel = 0

# Parse function that takes a single line of C++ code and translates it to python
def parseLine(line):
  # print("Line: " + line)
  global indentLevel
  
  # First parse for strings so that regex won't be confused by reserved words
  stringRE = "\"[^\"]*\""
  stringsInLine = []
  match = re.search(stringRE, line)
  while match != None:
    # print("found string at: " + match.span())
    stringsInLine.append(line[match.span()[0]:match.span()[1]])
    line = line[:match.span()[0]] + "!!STRING!!" + str(len(stringsInLine)) + "!!" + line[match.span()[1]:]
    match = re.search(stringRE, line)
  
  # remove whitespace at start of line and replace with the current indent
  line = line.strip()
  
  # If line is a comment replace // with # and return the line
  if line[:2] == "//":
    return (indentLevel * "  ") + "#" + line[2:] + '\n'
  
  # check for declarations without assignment which should be removed
  decRE = "(int|double|string|float|char|bool|void|size_t)[^=]+;"
  match = re.match(decRE, line)
  if match != None:
    return ""
  
  # check for assignmens
  decRE = "(int|double|string|float|char|bool|void|size_t)[ ]*"
  match = re.match(decRE, line)
  if match != None:
    line = line[match.span()[1]:]
  
  # if line starts with #include remove it
  includeRE = "#include"
  match = re.match(includeRE, line)
  if match != None:
    return ""
  
  # if line starts with using remove it
  usingRE = "using"
  match = re.match(usingRE, line)
  if match != None:
    return ""
  
                        # replace keywords
  # true -> True
  trueRE = "true"
  match = re.search(trueRE, line)
  while match != None:
    line = line[:match.span()[0]] + "True" + line[match.span()[1]:]
    match = re.search(trueRE, line)

  # false -> False
  falseRE = "false"
  match = re.search(falseRE, line)
  while match != None:
    line = line[:match.span()[0]] + "False" + line[match.span()[1]:]
    match = re.search(falseRE, line)

  # || -> or
  orRE = "\|\|"
  match = re.search(orRE, line)
  while match != None:
    line = line[:match.span()[0]] + " or " + line[match.span()[1]:]
    match = re.search(orRE, line)

  # && -> and
  andRE = "&&"
  match = re.search(andRE, line)
  while match != None:
    line = line[:match.span()[0]] + " and " + line[match.span()[1]:]
    match = re.search(andRE, line)

  # ++ -> += 1
  plusplusRE = "\+\+"
  match = re.search(plusplusRE, line)
  while match != None:
    line = line[:match.span()[0]] + " += 1 " + line[match.span()[1]:]
    match = re.search(plusplusRE, line)
  
  # remove semicolons
  if line[-1:] == ';':
    line = line[:-1]
  
  # check for {
  if line == "{":
    indentLevel += 1
    return ""
    
  # check for }
  if line == "}":
    indentLevel -= 1
    return ""
  
  # check for main
  mainRE = "main[ ]*([^)]*)"#"int +main +("
  match = re.search(mainRE, line)
  if match != None:
    # this is the opening of the C++ main function, so replace it with python main (MUST CALL main() AT THE END OF THE FILE)
    line = "def main():"
  
  # check for cout
  coutRE = "cout[ ]*<<"
  match = re.search(coutRE, line)
  if match != None:
    line = line[:match.span()[0]] + "print( str(" + line[match.span()[1]:] + "), end=\"\")"
    
    # replace << with +
    lesslessRE = "<<"
    match = re.search(lesslessRE, line)
    while match != None:
      line = line[:match.span()[0]] + ") + str(" + line[match.span()[1]:]
      match = re.search(lesslessRE, line)
      
    # replace endl with '\n'
    endlRE = "endl"
    match = re.search(endlRE, line)
    while match != None:
      line = line[:match.span()[0]] + "\"\\n\"" + line[match.span()[1]:]
      match = re.search(endlRE, line)
      
  # check for cin
  cinRE = "cin[ ]*>>"
  match = re.search(cinRE, line)
  if match != None:
    line = line[match.span()[1]:] + " = input()"
  
  # check for if
  ifRE = "if[ ]*([^)]*)"
  match = re.search(ifRE, line)
  if match != None:
    line = line[:match.span()[1]+1] + ":" + line[match.span()[1]+1:]
  
  # check for else if
  elseifRE = "else[ ]+if"
  match = re.search(elseifRE, line)
  if match != None:
    line = line[:match.span()[0]] + "elif" + line[match.span()[1]:]
  
  # check for else
  elseRE = "else"
  match = re.search(elseRE, line)
  if match != None:
    line = line[:match.span()[0]] + "else:" + line[match.span()[1]:]
  
  # check for while
  whileRE = "while[ ]*([^)]*)"
  match = re.search(whileRE, line)
  if match != None:
    line = line[:match.span()[1]+1] + ":" + line[match.span()[1]+1:]
  
  # Add strings back in
  stringReplacementRE = "!!STRING!!\d+!!"
  match = re.search(stringReplacementRE, line)
  while match != None:
    stringToInsert = stringsInLine.pop(0)
    line = line[:match.span()[0]] + stringToInsert + line[match.span()[1]:]
    match = re.search(stringReplacementRE, line)
    
  # if line != "":
  line = (indentLevel * "  ") + line + '\n'
  return line

# Main function that checks for valid terminal input and passes each line of the given C++ file through the parseLine function placing the result in the output file
def main():
  
  # check if command line args are correct
  if len(sys.argv) != 3:
    print('Invalid parameters count. Must be 2', file=sys.stderr)
    print(help)
    sys.exit(-1)
  # open file and read line by line converting to cpp
  in_filename = sys.argv[1];
  out_filename = sys.argv[2];
  
  print("infile: " + in_filename)
  print("outfile: " + out_filename)
  
  with open(in_filename, 'r') as inFile:
    lines = inFile.readlines()  # probably would die on sources more than 100 000 lines :D
  with open(out_filename, 'w+') as outFile:
    for line in lines:
      outFile.write(parseLine(line))
    outFile.write("main()") # add a call to the main function at the end of the file to start the program

# Start the program by calling the main function
main()