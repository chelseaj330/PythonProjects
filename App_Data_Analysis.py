#!/usr/bin/env python
# coding: utf-8

# ## Analysis of App User Data: Which App Types Attract the Most Users ##
# 
# For this project, I analyze the number of users for different kinds of freely downloadable apps.
# 
# Since the apps contained in the analyzed datasets make revenue only through in-app purchases, the goal of analysis is to figure which app types attract the most users, in order to boost revenue.

# In[1]:


from csv import reader

## Google Play/Android ##
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

## App Store ##
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# By printing the header for the Android data set, we can see the column names and identify which data types will be most useful for us. Below, the columns 'Type', 'Installs', 'Genres' and 'Content Rating' will most likely contain the most useful data for our goal.

# In[3]:


print(android_header)


# In[4]:


explore_data(android, 1, 4, True)


# Below, we will also print the header row for the Apple Store data in order to view the column names and the types of data available to us. 
# 
# Further information on these column names (which are somewhat vague) can be found [here](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)

# In[5]:


print(ios_header)


# In[6]:


explore_data(ios, 1, 4, True)


# Furthermore, it is brought to our attention through the discussion of the course that the Google Play data set contains an error in row 10472. To check this, we can print the header row and compare it against row 10472 to identify the error.

# In[7]:


print(android[10472])  # incorrect row
print('\n')
print(android_header)  # header
print('\n')
print(android[0])      # correct row


# "The row 10472 corresponds to the app Life Made WI-Fi Touchscreen Photo Frame, and we can see that the rating is 19. This is clearly off because the maximum rating for a Google Play app is 5. As a consequence, we'll delete this row." (taken from solution code)
# 
# Therefore, the next code block will be used to delete row 10472.

# In[8]:


print(len(android))
del android[10472]  # don't run this more than once
print(len(android))


# We can now continue by removing duplicate entries from teh Google Play dataset.

# Now that we've explored each data set and got a better idea of what each data set contains, we need to clean the data. The first task will be to check whether there are duplicate entries of data points within each data set. We will do this first for Android apps, and then for App Store apps. First, we will check the Android data for duplicate entries:

# In[9]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)    
    else:
        unique_apps.append(name)
        
print('Number of unique apps:', len(unique_apps))
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# As we can see from our results, there are quite a few duplicate entries present within the Google Play dataset. We will need to remove duplicate entries so that there is only a single entry for each app. Below, we will print a few lines of one duplicate app to see what criterion we can use to remove duplicate entries.

# In[10]:


for app in android:
    name = app[0]
    if name == 'FarmersOnly Dating':
        print(app)


# As can be seen above, the duplicate entries often differ in the number of reviews received, indicating that there are different entries for these apps from different points in time. We will need to keep the most recent entry (entry with the most reviews) and delete the duplicates.

# In[11]:


print('Expected length:', len(android) - 1181)


# We expect that our final dataset, once all duplicates are removed, will contain 9660 datapoints, each representing a unique app. To remove the duplicates, we will create a dictionary with each unique app name together with their highest number of reviews.

# In[12]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print(reviews_max)
        


# We can see that the length of our dictionary is quite long. Let's compare the expected length with the actual length.

# In[13]:


print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# We can see here that the expected and the actual lengths of the dictionary do in fact match.

# The next step is to change the value in the column "number of reviews" to a float in order to be able to analyze it further.

# In[14]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[15]:


explore_data(android_clean, 0, 3, True)


# Now that we've removed the duplicate entries by only keeping the entry for each app with the highest number of reviews, we now want to make sure that we only keep apps that are directed towards an English speaking audience. Therefore, we will have to clean the data again, removing any app that indicates a character in it's name outside of the English alphabet, numbering or punctuation system. To do this, we rely on ASCII codes and use the ord() commande to identify the numbers for different letters, and exclude those which do not fall in the ASCII range (0-127).

# In[16]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True
        
# For this function, we only return an app as False (e.g. non-English)
# if it has more than 3 non-ASCII characters in its name
# because some special symbols do exist within English app names
# such as emojis


# In[17]:


is_english(android_clean[3][0])
## This is a practice of the newly defined is_english function


# In[18]:


## Now we are going to use our define function is_english to test different 
## app names, as suggested in the exercise

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))


# Now that we have a working function for determining apps with english names, we will use it to go loop through each data set (android and ios) and add the app names determined ot be english to an empty list.

# In[19]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# We can see by comparing 2 of the datasets for the same platform (android_clean vs. android_english) that your function did work at removing some apps, as they are now 9659 rows of data vs. 9614 rows of data, respectively.

# The next step is to isolate the free apps, since our companys only builds apps that are free to download, with revenue consisting of in-app ads.

# In[20]:


print(android_english [1])

## We can see by printing a row from the android_english data set
## that the free data can be found in the 7th column
## for ios_english, it is the 4th column, which we can verify by
## going back to the original data set in Kaggle and viewing the
## header row

print(ios_english[0])
print(ios_english[1])


# Below, we run another for loop to separate the free apps from the non-free ones using the indicated columns and looping through each data set, while appending each that is returned as free to the new lists.

# In[21]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# We can now see above how many apps we have left in our final data set for each platform. Below, we explore just to make sure no data was cut.

# In[22]:


explore_data(android_final, 0, 3, True)


# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# Build a minimal Android version of the app, and add it to Google Play.
# If the app has a good response from users, we develop it further.
# If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets. For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of what are the most common genres for each market. For this, we'll need to build frequency tables for a few columns in our data sets.

# In[23]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
    


# By inspecting each data set, we can see that the genre information for iOS is contained in column 11 and for Android it is contained in columns 1 & 9. Therefore, we will now use our newly defined display_table function on both data sets.

# In[24]:


display_table(ios_final, 11)


# We can see that the most popular category within the iOS store is games, at 58%.

# In[25]:


display_table(android_clean, 1)


# In[26]:


display_table(android_final, 9)


# For the Google Play/Android store, there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.)

# While these are interesting insights, we want to see which genres has the most users. We can find how many people installed an app for the Android data by looking at column [5], Installs. However, there is no direct install data for the iOS data set. Instead, we will use ratings_count_tot, or column [5]. For each, we will calculate the average number of user ratings per app genre.

# In[32]:


genres_ios = freq_table(ios_final, 11)

for genre in genres_ios:
    total = 0
    len_genre = 0
    
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
            
    avg_n_ratings = total / len_genre

    print(genre, ':', avg_n_ratings)
    
    
## OPEN QUESTION:
## Is there a way to sort the results of this for loop?
   


# We can see here that navigation apps have the highest number of average downloads.

# Next, we will follow a similar process for the Google Play store/Android_final data set.

# In[28]:


display_table(android_final, 5) ## the Installs column


# As can be seen, the Installs data for Google Play is much more vague than that of iOS. We can't tell exactly how many installs any genre had, only a range. However, for our purposes, this is still enough info to determine which genre attracted the most users. We do, however, need to remove any special symbols like + and commas.

# In[30]:


categories_android = freq_table(android_final, 1)

for category in categories_android: 
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


    


# This gives us a complete list of the avergae number of installs for each category in the Google Play dataset.
# On average, communication apps have the highest number of average downloads within the Google Play store.
