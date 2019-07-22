#!/usr/bin/env python
# coding: utf-8

# <h1> **Exploring Posts from Hacker News' website**

# In this project, we are going to analyze a data set of community posts from the site Hacker News to see:
# 
# 1) Whether "Show HN" or "Ask HN" posts receive more comments on averages
# 
# 2) If posts created at certain times receive more comments on average

# In[3]:


from csv import reader
opened_file = open("hacker_news.csv")
read_file = reader(opened_file)
hn = list(read_file)
headers = hn[0]
hn_1 = hn[1:]

print(headers)

print(hn_1[:5])


# We'll first filter through this data to pull out any posts that start with "Ask HN" or "Show HN".

# In[11]:


ask_posts = []

show_posts = []

other_posts = []

for row in hn_1:
    title = row[1]
    title_1 = title.lower()
    
    if title_1.startswith('ask hn'):
        ask_posts.append(row)
    elif title_1.startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

print(len(ask_posts))

print(len(show_posts))

print(len(other_posts))
        


# In[ ]:





# In[5]:


print(ask_posts[:5])


# In[6]:


print(show_posts[:5])


# Now that we have the complete lists for both Ask HN and Show HN posts, we will find which post type received more comments on average.
# 
# We will do this by calculating the total comments for all of the Ask posts and finding the average by dividing this total by the overall number of Ask posts found.

# In[7]:


total_ask_comments = 0

for post in ask_posts:
    num_comments = int(row[4])
    
    total_ask_comments = total_ask_comments + num_comments

print(total_ask_comments)

print(len(ask_posts))

avg_ask_comments = total_ask_comments / len(ask_posts)

print((avg_ask_comments))


# In[10]:


total_show_comments = 0

for post in show_posts:
    num_comments = int(row[4])
    
    total_show_comments = total_show_comments + num_comments

print(total_show_comments)

print(len(show_posts))

avg_show_comments = total_show_comments / len(show_posts)

print((avg_show_comments))


# From this analysis, we can see that both Show and Ask posts receive an equal number of commments on average.

# In[9]:


import datetime as dt

result_list = []

for post in ask_posts:
    created_at = row[6]
    
    num_comments = int(row[4])
    
    result_list.append(created_at, num_comments)
    
counts_by_hour = {}

comments_by_hour = {}

for row in result_list:
    hour = row[0]

    hour_dt= datetime.strptime(hour, "%H:%M:%S")


# In[ ]:





# In[ ]:




