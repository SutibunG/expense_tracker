class User:

    def __init__(self, user_id, username): #__init__ is initializes attributes, it's called everytime you create a new object from the class
        self.id = user_id
        self.username = username
        print("new user being created...")

    #def follow(self, user):
        #user.followers += 1
        #self.following += 1
    
#user_1 = User("001", "Sutibun")
#user_2 = User("002", "Jocu")
#print(user_1.id)

#user_1.follow(user_2)