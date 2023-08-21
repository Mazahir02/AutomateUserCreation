# Import the necessary Java libraries for file handling
from java.io import FileInputStream

# Open the "details.properties" file for reading
propInputStream = FileInputStream("details1.properties")

# Create a Properties object and load the properties from the file
configProps = Properties()
configProps.load(propInputStream)

# Read the total number of domains to configure from the properties file
totalDomain_to_Configure = configProps.get("total.domain")

# Initialize a counter for the domains
counterDomain = 1

# Loop through each domain for configuration
while (counterDomain <= int(totalDomain_to_Configure)):
    # Read domain-specific properties from the properties file
    domainName = configProps.get("domain.name." + str(counterDomain))
    adminURL = configProps.get("admin.url." + str(counterDomain))
    adminUserName = configProps.get("admin.userName")
    adminPassword = configProps.get("admin.password")
    realmName = configProps.get("security.realmName")
    totalUsers_to_Create = configProps.get("total.username")

    try:
        # Attempt to connect to the WebLogic Server with admin credentials
        connect(adminUserName, adminPassword, adminURL)
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

    print 'Creating Users . . .'
    x = 1

    # Loop through user creation for the current domain
    while (x <= int(totalUsers_to_Create)):
        userName = configProps.get("create.user.name." + str(x))
        userPassword = configProps.get("create.user.password." + str(x))
        userDescription = configProps.get("create.user.description." + str(x))
        
        try:
            # Attempt to create a user
            cmo.createUser(userName, userPassword, userDescription)
            print '-----------User Created With Name : ', userName
        except:
            print '*************** Check If the User With the Name : ', userName, ' already Exists...'
        
        x = x + 1

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
