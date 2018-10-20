import sys
import re

class LogicMcLogic:
    R = []
    docs = []

    # Takes file assigning values to the rule set R
    def setR(this):
        # Split input by line
        #input = open(sys.argv[1], 'r').read().splitlines()
        input = open('RuleSet.txt', 'r').read().splitlines()
        Rules = []

        # Split each line into sublist of characters
        for i in input:
            Rules.append(re.sub("[^A-Za-z]", " ", i).split())
        this.R = Rules

    # Transforms line of logic into printable string
    def logicLine(this,r):
        # ['a'] into "a"
        if len(r) < 2:
            return str(r[0])

        # ['b', 'a'] into "a => b"
        elif 2 < len(r) < 4:
            return ""+r[1]+" => "+r[0]

        #['z','a','b','c', ...] into "a^b^c^... => z"
        else:
            statement = ""+r[1]
            for i in r[2:]:
                statement += "^"+i
            statement += " => "+r[0]
            return statement
    # Use atoms to solve rules
    def solve(this, goals):
        # If empty goal set then succeeded
        if goals == []:
            return "Succeed";

        # Extract goal goal from begining of list and redefine list
        a = goals[0]
        goals = goals[1:]

        # Iterate through rule set to solve the rules with atoms
        for i,r in enumerate(this.R):
            # If r[0] = a = goals[0]/ rule entailment is same as atom then do work
            if r[0] == a:
                # Append each element of r after first to goals for testing
                for x in r[1:]: goals.append(x)

                # If the rest of goals succeed then copy to docs and return success
                if this.solve(goals) == "Succeed":
                    this.docs = ["Succeeded rule %d (phrase " %(i+1) + this.logicLine(r) + ") with atom " + str(a) + ". Remaining atoms: " + str(goals)]+ this.docs
                    return "Succeed"

                # Copy failed statement to docs and return failed
                this.docs = ["Failed after rule %d (phrase " %(i+1) + this.logicLine(r) + ") with atom " + str(a) + ". Remaining atoms: " + str(goals)] + this.docs
                return "Failed"

        # When user inputs atom that does not exist in rule set
        return "Fail: User query not within the rule set"

# Create Logic class and set up rules from file
lml = LogicMcLogic()
lml.setR()

# Scan in user query and convert to list
atoms = input("Enter atom(s): ")
atoms = re.sub("[^A-Za-z]", "", atoms)
g =[]
for x in atoms:
    g.append(x)

# Solve with user provided atoms
lml.solve(g)

# Print out information before and during calculation
print("Atoms: ", g)
for x in lml.docs:
    print(x)
