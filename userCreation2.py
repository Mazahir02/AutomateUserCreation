# Import the necessary Java libraries for file handling
from java.io import FileInputStream, BufferedReader, InputStreamReader, File
from java.util import ArrayList
from java.lang import String

# Open the "details.properties" file for reading
propInputStream = FileInputStream("details2.properties")

# Create a Properties object and load the properties from the file
configProps = Properties()
configProps.load(propInputStream)

# Read the total number of domains to configure from the properties file
totalDomain_to_Configure = configProps.get("total.domain")

# Initialize empty lists to store usernames and passwords
usernames = []
passwords = []
descriptions = []

# Open the CSV file for reading
csvfile = File('<mention_Path>/userDetails.csv')
reader = BufferedReader(InputStreamReader(FileInputStream(csvfile)))

# Read the CSV file line by line
line = reader.readLine()
while line is not None:
    # Split the line into parts using a comma as the delimiter
    parts = line.split(",")
    if len(parts) >= 2:
        # Assuming the first part contains usernames, the second contains passwords,
        # and the third contains descriptions (modify as needed)
        username = parts[0]
        password = parts[1]
        description = parts[2]

        # Append the username, password, and description to their respective lists
        usernames.append(username)
        passwords.append(password)
        descriptions.append(description)

    # Read the next line
    line = reader.readLine()

# Close the CSV file when you're done with it
reader.close()

# Initialize a counter for the domains
counterDomain = 1

# Loop through each domain for configuration
while (counterDomain <= int(totalDomain_to_Configure)):
    # Read domain-specific properties from the properties file
    domainName = configProps.get("domain.name." + str(counterDomain))
    #adminURL = configProps.get("admin.url." + str(counterDomain))
    #adminUserName = configProps.get("admin.userName")
    #adminPassword = configProps.get("admin.password")
    realmName = configProps.get("security.realmName")
    totalGroups_to_Create = configProps.get("total.groups")
    totalUsers_to_Create = configProps.get("total.username")

    try:
        # Attempt to connect to the WebLogic Server with admin credentials
        #connect(adminUserName, adminPassword, adminURL)
        connect()
        serverConfig()

        # Construct the authenticator path
        authenticatorPath = '/SecurityConfiguration/' + domainName + '/Realms/' + realmName + '/AuthenticationProviders/DefaultAuthenticator'
        print authenticatorPath

        # Change the current working directory to the authenticator path
        cd(authenticatorPath)
    except:
        print 'Exception Raised'

    print ' '
    print ' '


    # Loop through the usernames and passwords
    for i in range(len(usernames)):
        username = usernames[i]
        password = passwords[i]
        description = descriptions[i]

        try:
                #Attempt to create a user
                cmo.createUser(username,password,description)
                print '-----------User created with Name : ', username
        except:
                print '*************** Check If the User With the Name : ', username, ' already Exists...'



    print ' '
    print ' '

    print 'Adding Group Membership of the Users:'

    # Loop through group creation and user membership addition
    for y in 1, 2:
        grpName = configProps.get("create.group.name." + str(y))
        groupMembers = configProps.get("create.group.name." + str(y) + ".members")
        usrName = ''

        try:
            for member in groupMembers:
                if member == ",":
                    # Add the user to the group
                    cmo.addMemberToGroup(grpName, usrName)
                    print 'USER:', usrName, 'Added to GROUP:', grpName
                    usrName = ''
                else:
                    usrName = usrName + member
        except:
            print 'Exception raised'

    print ' '
    print ' '
    counterDomain = counterDomain + 1
