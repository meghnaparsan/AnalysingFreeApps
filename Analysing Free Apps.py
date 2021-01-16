# # Profitable Mobile Applications
# 
# ## Project Description
#     
# The aim of this project is to analyze data of all the Mobile Applications available on Google Play store and App store and give an insight to developers to develop a mobile application that would be profitable for the company. In this Project, only Free and English supported Apps are taken into consideration.
# Two Reports [Google Play Store Report](https://www.kaggle.com/lava18/google-play-store-apps/home) and [Apple App Store Report](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home) are used to extract the result.
# 
# ## Steps to be followed
#     1) Open the csv file
#     2) Extract Data from it and convert it into a list
#     3) Data Cleaning
#         a. Remove incorrect data
#         b. Remove reduntant data
#         c. Remove data which is not needed for the analysis. (In this Project, only Free English langauge supported apps are needed).
#     4) Data Processing 
#         a. With the pattern extracted, deduce the hypothesis needed

# **Step 1:**
#     
#     Open the csv files from the local machine

# In[ ]:


from csv import reader

#open iOS file 
open_ios_file = open ('Downloads/AppleStore.csv', encoding = 'utf8')
read_ios_file = reader (open_ios_file)
list_ios_file = list (read_ios_file)
ios_header = list_ios_file [0] #Separate header from the list
ios_data = list_ios_file [1:]

#open google play store file
open_google_file = open ('Downloads/googleplaystore.csv', encoding = 'utf8')
read_google_file = reader (open_google_file)
list_google_file = list (read_google_file)
google_header = list_google_file [0] #Separate header from the list
google_data = list_google_file [1:]


# **Step 2:**
#     
#     extract_file() function is used to Extract data from the Files. It takes three Parameters (data_set, start and end). data_set is the list that contains the content of the file. start and end parameters take the starting and ending index of the file, til which the list is to be read

# In[ ]:


def extract_file(data_set, start, end):
    for each_row in data_set[start:end]:
        print (each_row)
        print("\n")
    print ("Length of the Data Set is: ", len(data_set))


# **Step 3: - Data Cleaning**
#     
#     a. Remove incorrect data - 10472th row of the play store data has irrelevant data. 
#     
# **(IMPORTANT: Don't run the below code more than once.)**

# In[ ]:


#del(google_data[10472])
#print (google_data[10472])
#len (google_data)


# b. Remove reduntant data
#     
#     The report contains many datasets which are repeated more than once. Such data must be removed before procesing the data. So, we create two lists. One will list all the duplicate datasets and the other list will contain all the Unique datasets.

# In[ ]:


#Get the list of duplicate apps present in the Google Play store Data Set
duplicate_apps_google = []
unique_apps_google = []

for each_row in google_data:
    app_name = each_row[0]
    if app_name in unique_apps_google:
        duplicate_apps_google.append(app_name)
    else:
        unique_apps_google.append(app_name)
    
print ("Number of Duplicates present:", len(duplicate_apps_google))

max_review_google = remove_duplicate(google_data, 3, 0) 
#google_data - List that is to be analysed. 3 - column number based on which duplicate data are deleted. 0 - app name

print ("Number of apps present after removing Duplicates: ", len(max_review_google))


# In[ ]:


#Get the list of duplicate apps present in the iOS App store Data Set
duplicate_apps_ios = []
unique_apps_ios = []

for each_row in ios_data:
    app_name = each_row[1]
    if app_name in unique_apps_ios:
        duplicate_apps_ios.append(app_name)
    else:
        unique_apps_ios.append(app_name)
        
print ("Number of duplciates present: ", len(duplicate_apps_ios))

max_review_ios = remove_duplicate(ios_data, 5, 1)
#ios_data - List that is to be analysed. 5 - column number based on which duplicate data are deleted. 1 - app name

print ("Number of apps present after removing Duplicates ", len (max_review_ios))


# The total number of duplicate Data points in the google data set is 1181 and in ios data set is 2. Duplicate datasets can be removed randomly. But that would make the analysis inaccurate. So, here we take the dataset that is more recent. For this case, the column "Ratings" is taken as the criterion and the dataset with the highest number of ratings is retained and all other data are deleted. For this purpose, we create a dictionary. The key of the dictionary would be the app name and the value of the key would be the highest review that app has got. All this would be done by a function remove_duplicate(data_set, index)

# In[ ]:


#Create a Dictionary with unique app name as the key and the highest rating of that app as value
def remove_duplicate(data_set, index, app_number):
    max_review_app = {}
    
    for each_row in data_set:
        review = each_row[index]
        app_name = each_row[app_number]
        
        if app_name in max_review_app and review > max_review_app[app_name]:
            max_review_app[app_name] = review
        elif app_name not in max_review_app:
            max_review_app[app_name] = review
    
    return max_review_app


# With the help of the dictionary, all the duplicate data are removed and a new clean list is created

# In[ ]:


ios_clean_data = create_no_duplicate_list(ios_data, max_review_ios, 5, 1)
print ("Length of the data sheet after removing duplicates: ", len(ios_clean_data))

google_clean_data = create_no_duplicate_list(google_data, max_review_google, 3, 0)
print ("Length of the data sheet after removing duplicates: ", len(google_clean_data))


# In[ ]:


#Create a list of clean data
def create_no_duplicate_list(data_set, dictonary, criterion_number, app_number):
    clean_data = []
    check_if_already_added = []
    for each_row in data_set:
        criterion = each_row [criterion_number]
        app_name = each_row [app_number]
        
        if (criterion == dictonary[app_name]) and (app_name not in check_if_already_added):
            clean_data.append(each_row)
            check_if_already_added.append(app_name)
    
    return clean_data


# c. Remove data which is not needed for the analysis.
#    
#    Non English apps are removed from the list. The range of English alphabets fall within the range of 0 to 127. There may be some app apps that has special characters or emojis and still be an English App. To avoid data loss, 3 non english characters are allowed in a string of app name.

# In[ ]:


#function to check if the string is in English language or not.
def check_language(string_name):
    count = 0
    for element in string_name:
        if (ord(element) > 127):
            count = count + 1
    if count < 3:
        return True


# In[ ]:


ios_english_apps = []
google_english_apps = []

for each_row in google_clean_data:
    app_name = each_row[0]
    if (check_language(app_name)):
        google_english_apps.append(each_row)
        
for each_row in ios_data:
    app_name = each_row[1]
    if (check_language(app_name)):
        ios_english_apps.append(each_row)

print ("Number of English apps (Google Play store): ", len (google_english_apps))
print ("Number of english apps (iOS App store): ", len (ios_english_apps))


# After isloating all the English apps, isloate all the free english apps

# In[ ]:


google_free_apps = create_list_free_apps(google_english_apps, 7)
print ("Number of free apps (Google play store): ", len(google_free_apps))

ios_free_apps = create_list_free_apps(ios_english_apps, 4)
print ("Number of free apps (iOS app store): ", len(ios_free_apps))


# In[ ]:


#function to filter all the free english apps
def create_list_free_apps(data_set, price_number):
    free_apps = []
    for row in data_set:
        price = row[price_number]
        if price == '0':
            free_apps.append(row)
    
    return free_apps


# Now that the data is cleaned, next step is analyse the data and derive a conclusion. Since, the app being developed is going to be free, the only source of revenue for the company is ads. So, in order to increase the revenue of the company, more people should visit. This will lead to more number of people seeing the ad which will in turn increase the revenue of the company.
# 
# We will be considering the "Prime Genre" column of App store report and "Genre" and "Cateogory" of Google play store report to derive a conclusion. 
# 
# First, a frequency table should be created and sorted in descending order. This will show us the genre that has highest number of apps. With this information, the desired result could be obtained. 
# 
# The function generate_freq_table() takes two parameters. One is the list which is cleaned and the other is the index which would sepcify the column for which the frequency table is to be created. 

# In[ ]:


#Generate freqency table

def generate_freq_table(data_set, index):
    freq_table = {}
    for each_row in data_set:
        value = each_row[index]
        if value in freq_table:
            freq_table[value] += 1
        else:
            freq_table[value] = 1
    
    length = len(data_set)
    
    #Return frequency in percentage for better understanding
    for each_row in freq_table:
        freq_table[each_row] = (freq_table[each_row] / length) * 100
    return freq_table


# In[ ]:


ios_genre = display_table(ios_free_apps, 11) #11 is the prime genre column
for row in ios_genre:        
    print (row[1], ' : ', row[0])   
print ("\n\n\n")

google_category = display_table(google_free_apps, 1) #1 is the category column
for row in google_category:
    print (row[1], ' : ', row[0])
print ("\n\n\n")

google_genre = display_table(google_free_apps, 9) #9 is the Genre column
for row in google_genre:
    print (row[1], ' : ', row[0])
print ("\n\n\n")


# Sorting a dictionary would throw error because dictionary is sorted according to the key and not according to the value of the key. To overcome this problem, the dictionary is converted into a tuple and then these tuples are added to a list and then sorted 

# In[ ]:


#Function to convert the dictionary into a tuple

def convert_tuble(data_set, index):
    table = generate_freq_table(data_set, index)
    table_display = []
    for key in table:
        tuble_value = (table[key], key)
        table_display.append(tuble_value)
    
    sorted_table = sorted(table_display, reverse = True)
        
    return sorted_table
    


# From the output, it is evident that app store is dominated by apps for fun and the google play store has a quite balanced result with both fun and productive apps. 
# 
# To find the most popular genre, we can use the Number of "Intalls" as a parameter. But this is missing in App Store report. So, as a proxy for Number of Install, we take the "Total Number of Ratings" for the App store data.

# In[ ]:


#For each genre, find the average Rating Count Total. 

genre_ios = convert_tuble(ios_free_apps, 11)

for genre_ind in genre_ios:
    rating = 0
    length_genre = 0
    for each_row in ios_free_apps:
        if genre_ind[1] == each_row[11]:
            rating = rating + float (each_row[5])
            length_genre = length_genre + 1
    average = rating/length_genre
    print (genre_ind[1] ,  average)
            


# Here, we can see that genre like Naviagation and Social media have the highest ratings. It's because of giants like Google map, Facebook and other popular apps. 

# To analyis the google Play store report, let's take the Installs column. Here Number of install given are not precise. It is given as 1000+ or 1, 00, 000+ installs. In order to solve this problem, lets take 1000+ as 1000. (same for all other values)

# In[ ]:


#print (google_header)

google_category = convert_tuble(google_free_apps, 1)

for each_category in google_category:
    length = 0
    installs_total = 0
    for each_row in google_free_apps:
        if each_category[1] == each_row[1]:
            installs_str = each_row[5]
            installs_str = installs_str.replace(',', '')
            installs_str = installs_str.replace ('+', '')
            installs = float (installs_str)
            installs_total += installs
            length += 1
    average = installs_total / length
    print (each_category[1], " : ", average)
    

