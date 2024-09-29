#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for App Store & Google Play Markets

# # Introduction
# 
# ### This Project aims to act as company that builds Android and iOS mobile apps, where the goal is to search for suitable mobile app profiles that are profitable for both App Store and Google Play markets. As a data analyst, the task in this project is to enable data-driven decisions with respect to the kind of apps the developers team build. The goal is to analyse the dataset to help the team understand what types and genres of apps are most likely to attract more users.
# 
# #### In this project, it is assumed that the company only build apps that are free to download and install, and the main source of revenue consists of in-app ads, meaning that the revenue for any given app is mostly influenced by the number of users that use the app. 
# 
# 

# In[1]:


from csv import reader

android_data = open('Downloads/googleplaystore.csv')
read_file = reader(android_data)
android = list(read_file)
android_header = android[0]
android = android[1:]

ios_data = open('Downloads/AppleStore.csv')
read_file = reader(ios_data)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[2]:


def explore_data(dataset, start, end, rows_and_columns = False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


print(android_header)
print('\n')
explore_data(android, 0, 5, True)


# In[4]:


print(ios_header)
print('\n')
explore_data(ios, 0, 5, True)


# In[ ]:


# 7191 ios apps, 10841 android apps


# In[5]:


print(android[10472])   # row with wrong data
print('\n')
print(android_header)
print('\n')
print(android[0])    # row with correct data


# In[6]:


del android[10472]   # deleting row with wrong data
print(len(android))


# In[7]:


duplicate_apps = []   # deleting duplicate apps
unique_apps = []

for app in android:   # loop android data and append duplicates to duplicate_list, else append to unique list
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# In[8]:


print('Expected length: ', len(android) - 1181)   # no. of rows left (expected)


# In[9]:


reviews_max = {}    # create dictionary (max review no.s of each app)

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews   # no. of max reviews of app
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[10]:


print('Actual length: ', len(android) - 1181)  # no. of rows left (actual)


# In[11]:


# Actual length of dataset matches expected length


# In[12]:


android_clean = []   # store cleaned dataset
already_added = []   # store app names

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews and (name not in already_added)):
        android_clean.append(app)   # add 
        already_added.append(name)


# In[13]:


explore_data(android_clean, 0, 5, True)  # to ensure value same as expected 


# In[14]:


def is_english(string):   # remove non-English apps
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1   # increment by 1 when non-ASCII character found
            
    if non_ascii > 3:   # remove apps with more than 3 non-ASCII characters
        return False
    else:
        return True
    
print(is_english('Instagram'))   # testing with a few apps
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# In[15]:


android_eng = []
ios_eng = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_eng.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_eng.append(app)


# In[16]:


explore_data(android_eng, 0, 5, True)  # English apps in android
print('\n')
explore_data(ios_eng, 0, 5, True)  # English apps in ios


# In[17]:


# only leaving apps suitable for target audience (English-speaking)

# android apps: 9614, ios apps: 6183


# In[18]:


android_free = []
ios_free = []

for app in android_eng:
    price = app[7]
    if price == '0':
        android_free.append(app)

for app in ios_eng:
    price = app[4]
    if price == '0.0':
        ios_free.append(app)

print(len(android_free))
print(len(ios_free))


# In[19]:


# only leaving apps that are free to download and install

# android apps: 8864, ios apps: 3222


# ## Finding the most common apps by Genre
# 
# The aim is to determine the kinds of apps that are likely to attract more users because revenue is highly influenced by the number of people using our apps. The goal is to find successful app profiles on both markets and add them on App Store and Google Play. This will be done by analyzing the most common favoured genres on both markets, using frequency tables.
# 
# ### Validation Strategy
# 
# 1. Build a minimal Android version of the app, and add it to Google Play. 
# 2. If the app has a good response from users, we then develop it further.
# 3. If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.

# In[24]:


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
            
    table_percentages = {}   # frequency table showing percentages
    for key in table:
        percentages = (table[key]/total) * 100
        table_percentages[key] = percentages
        
    return table_percentages

def display_table(dataset, index):   # transform freq table into list of tuples to sort list in descending order
    table = freq_table(dataset, index)
    table_display = []   
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[25]:


display_table(ios_free, -5)


# From the freq table, it is observed that more than half (58.16%) of the free apps in App Store available in English are Games, followed by Entertainment apps take up 7.88%, Photo & Video at near 5%, Education and Social Networking apps at 3.66% and 3.29% respectively. It can be deduced that on the App Store, entertaining and relaxing apps (Games, Photo & Video, Shopping, Social Networking etc.) are more popular as compared to productive and practical apps (Lifestyle, Productivity, Finance, Weatjer, Medical etc.). This could also be due to productivity apps are not offered free as widely as entertaining apps.

# In[27]:


display_table(android_free, 1)   # displaying Category column


# In[28]:


display_table(android_free, -4)   # displaying Genres column


# For Google Play, it is seen that the available apps seem significantly different under the Category column, where more apps are designed for productivity and practical purposes (Family (~19%), Tools (8.46%), Business (4.59%), Finance (3.7%) etc.) than entertainment.
# 
# Further observation on Google Play shows that under the Family category, many of the apps are games for children. 
# 
# However, practical apps still dominates overall, which is also confirmed by the results in the Genres column.   

# ## Analyzing Most Popular Genres and Apps (App Store)

# In[29]:


genres_ios = freq_table(ios_free, -5)

for genre in genres_ios:   # taking total no. of user ratings as proxy
    total = 0
    len_genre = 0
    for app in ios_free:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre   # average no. of user ratings per app genre
    print(genre, ':', avg_n_ratings)


# On average, Navigation apps have highest no. of user ratings (86090.33), followed by Reference and Social Networking apps with 74942.11 and 71548.35. Below shows the apps with the highest number of ratings under Navigation and Reference.

# In[30]:


for app in ios_free:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print app name and no. of ratings


# This shows that even though the average number of Navigation apps is the highest, it is heavily influenced by specific popular ones such as Waze and Google Maps, with near half a million users combined.

# In[31]:


for app in ios_free:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# Similar scenario occurs in Reference apps as well, with 74942 user ratings on average, it is significantly dominated by Bible and Dictionary.com. This pattern applies to app genres such as Social Networking, where popular apps (Instagram, Snapchat, X) and Music (Spotify, YouTube Music, Shazam) heavily skews the average number of user ratings.   

# #### Taking a few things into account:
# 
# 1. The popularity of a genre in App Store
# 2. App Store is dominated by entertaining and relaxing apps, hence a productive/practical app might have a higher chance to stand out among the many apps
# 
# #### Recommendation: 
# 
# Turn a popular book into an interactive app with features such as including built-in dictionary and Thesaurus, an audio version of the book, built-in highlighter, bookmark, and notes, quizzes about the contents, a discussion board to connect readers with similar interest etc. Essentially, allowing users a fun and easy experience while reading.

# ## Analyzing Most Popular Genres and Apps (Google Play)

# In[32]:


display_table(android_free, 5) # No. of Installs column


# In[ ]:


# result shows to be not as accuate as wanted, as the values of installs are not precise, eg. 100+ and 5000+


# In[33]:


categories_android = freq_table(android_free, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_free:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)   # convert no.s to float
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, Communication apps have highest number of installs (38,456,119), while below shows the apps that influeced the number of installs under Communication.

# In[34]:


for app in android_free:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# As expected, popular apps like WhatsApp Messenger, Messenger, Skype, Google Chrome, Gmail, and Hangouts (over 1 billion installs for each) heavily skews the average number of installs in Communication. 
# 
# Similar to App Store, this pattern also applies for categories like Social (dominated by Facebook, Instagram, etc.) and Video Players (dominated by YouTube, MX Player, etc.), and Productivity (dominated by Dropbox, Google Calendar, etc.) where niche categories are highly dominated by extremely popular apps.
# 
# As shown below, when removed apps under Communication with over 100 million installs, the average is significantly reduced (around ten times).

# In[35]:


under_100m = []

for app in android_free:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100m.append(float(n_installs))
        
sum(under_100m) / len(under_100m)


# As book and reference showed potential in App Store, in addition, this genre seems to be quite popular in Google Play too (8,767,811). Hence, decided to dive into this specific genre.

# In[36]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# In[37]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# Despite including a large variety of apps under the book and reference genre, from software for processing and collections of libraries, dictionaries, tutorials on programming or languages, etc., there is still a small number of popular apps that are skewing the average. 
# 
# The below cell shows apps that have number of installs between 1,000,000 and 100,000,000. This is to help with brainstorming an app recommendation by understanding the app types with popularity at somewhere in between.

# In[38]:


for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# To prevent competition from existing popular apps under this genre, which includes software for processing and reading ebooks, as well as different collections of libraries and dictionaries, apps with similar features are not recommended to be built.
# 
# Following the observation of quite a number of books under Quran are built, it could be a good idea to curate an app based on a popular/trending book. However, as there are many dictionaries and e-book libraries, it is recommended to include attractive features such as a built-in dictionary and Thesaurus, an audio version of the book, built-in highlighter, bookmark, and notes, related quizzes, a discussion board to for readers to connect etc.

# # Conclusion
# 
# Throughout this project, App Store and Google Play app profiles were analysed thoroughly, with the goal of providing a feasible app recommendation to be built in both App Store and Google Play. 
# 
# It was concluded that turning a popular or trending book into an app, including attractive and tailored features to the target audience would be strongly profitable for both markets.
