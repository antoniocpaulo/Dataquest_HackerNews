#!/usr/bin/env python
# coding: utf-8

# # Hacker News 
# 
# Hacker News is a site started by the startup incubator Y Combinator, where user-submitted stories (known as "posts") are voted and commented upon, similar to reddit. Hacker News is extremely popular in technology and startup circles, and posts that make it to the top of Hacker News' listings can get hundreds of thousands of visitors as a result. 
# 
# The present analysis intends to determine which of type of post, `Ask HN` or `Show HN`, receive more comments on average. Plus, the time component is introduced to check if there is a posting time that receives more comments on average.
# 
# The current data set has approximately 20,000 rows with each row containing the following columns:
# * `id`: The unique identifier from Hacker News for the post
# * `title`: The title of the post
# * `url`: The URL that the posts links to, if it the post has a URL
# * `num_points`: The number of points the post acquired, calculated as the total number of upvotes minus the total number of downvotes
# * `num_comments`: The number of comments that were made on the post
# * `author`: The username of the person who submitted the post
# * `created_at`: The date and time at which the post was submitted

# ---
# ## Read and Store file in dataset variable `hn`
# 
# Below `reader` class form `csv` module is used to read `.csv` file, which is then stored under `hn` variable.

# In[1]:


from csv import reader
hn = list(reader(open("hacker_news.csv")))

def print_first_5_rows(dataset):
    for row in dataset[:5]:
        print(row)
        print('\n')

print_first_5_rows(hn)


# ---
# ## Separate header row from dataset

# In[2]:


headers = hn[0]
hn = hn[1:]

print(headers)
print_first_5_rows(hn)


# ---
# ## Create lists containing `Ask HN` and `Show HN` rows
# 
# Below dataset rows will be split into 3 lists, `ask_posts` will be used for the `Ask HN` (stores the questions asked in Hacker News platform), `show_posts` list to store `Show HN` rows (stores posts of users that want to show something), and the remaining rows shall be stored under `other_posts`.

# In[3]:


ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)

#check number of posts in ask_posts, show_posts and other_posts
print('The number of posts in ask_posts is: {}'.format(len(ask_posts)))
print('The number of posts in show_posts is: {}'.format(len(show_posts)))
print('The number of posts in other_posts is: {}'.format(len(other_posts)))


# ---
# ## Which type of post receives more comments on average?
# 
# Determine which list `ask_posts` or `show_posts` contain more comments.

# In[4]:


total_ask_comments = 0
for row in ask_posts:
    total_ask_comments += int(row[4])

avg_ask_comments = total_ask_comments / len(ask_posts)
print('The average number of comments in ask_posts is: {:.2f}'.format(avg_ask_comments))    

total_show_comments = 0
for row in show_posts:
    total_show_comments += int(row[4])

avg_show_comments = total_show_comments / len(show_posts)
print('The average number of comments in show_posts is: {:.2f}'.format(avg_show_comments))    


# As the average number of comments in `ask_posts` is almost 40% larger than that of the `show_posts`, there is a clear tendency that posts containg questions received more adherence from the Hacker News community. 
# 
# For the next step - "if there is a best period to post" - one will only use the `ask_posts` list.

# ---
# ## Posting time vs number of comments
# 
# If ask posts are created at a certain time are they more likely to attract a larger number of comments? We'll use the following steps to perform this analysis:
# 
# * Calculate the amount of ask posts created in each hour of the day, along with the number of comments received.
# * Calculate the average number of comments ask posts receive by hour created.

# In[5]:


# start by importing datetime module to transform dates in datetime objects
import datetime as dt

results_list = []
for row in ask_posts:
    created_at = row[6]
    n_comments = int(row[4])
    results_list.append([created_at, n_comments])
    
counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"
for row in results_list:
    date = dt.datetime.strptime(row[0], date_format)
    hour = date.strftime("%H")
    n_comments = row[1]
    if hour in counts_by_hour:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += n_comments
    else:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = n_comments
        


# In[6]:


# calculate the average number of comments for posts created during each hour of the day.
avg_by_hour = []
for hour in counts_by_hour:
    average = comments_by_hour[hour] / counts_by_hour[hour]
    avg_by_hour.append([hour, average])

#for row in sorted(avg_by_hour):
#    print("The average number of comments in hour: {} is {:.2f}".format(row[0], row[1]))


# To make the result analysis easier another list is going to be created which will store first the number of comments per hour and then the corresponding hour.

# In[7]:


swap_avg_by_hour = []
for row in avg_by_hour:
    swap_avg_by_hour.append([row[1], row[0]])

#print(swap_avg_by_hour)


# In[8]:


# Use the sorted() function to sort swap_avg_by_hour in descending order. 
sorted_swap = sorted(swap_avg_by_hour, reverse=True)

print("Top 5 Hours for Ask Posts Comments")
for row in sorted_swap[:6]:
    date = dt.datetime.strptime(row[1], "%H")
    time = date.strftime("%H:%M")
    print("{}: {:.2f} average comments per post".format(time, row[0]))


# Taking into account the results shown above and that my timezone is GMT (Greenwich Meridian Time) and that of the dataset is ET (Eastern Time = GMT-5), I would create a post at around 20:00 (= 15:00 + 5:00) to increase the chance of having a larger number of comments in my post.

# ---
# 
# # NEXT STEPS
# 
# * Determine if show or ask posts receive more points on average.
# * Determine if posts created at a certain time are more likely to receive more points.
# * Compare your results to the average number of comments and points other posts receive.
# * Use Dataquest's data science project style guide to format your project.

# ---
# ## Determine which post receives more points on average

# In[9]:


total_ask_points = 0
for row in ask_posts:
    total_ask_points += int(row[3])
    
average_points_ask = total_ask_points / len(ask_posts)
print('The average number of points in ask_posts is: {:.2f}'.format(average_points_ask))

total_show_points = 0
for row in show_posts:
    total_show_points += int(row[3])
    
average_points_show = total_show_points / len(show_posts)
print('The average number of points in show_posts is: {:.2f}'.format(average_points_show))


# As the show_posts receives more points on average, the next study will only use this variable. The next study objective is to check if there is a time more prone to receive more comments.

# In[10]:


results_points_list = []
for row in show_posts:
    created_at = row[6]
    n_points = int(row[3])
    results_points_list.append([created_at, n_points])
    
counts_by_hour = {}
points_by_hour = {}
for row in results_points_list:
    date = dt.datetime.strptime(row[0], date_format)
    hour = date.strftime("%H")
    n_points = row[1]
    if hour in counts_by_hour:
        counts_by_hour[hour] += 1
        points_by_hour[hour] += n_points
    else:
        counts_by_hour[hour] = 1
        points_by_hour[hour] = n_points


# In[11]:


# calculate the average number of points for show posts created during each hour of the day.
avg_pts_by_hour = []
for hour in counts_by_hour:
    average = points_by_hour[hour] / counts_by_hour[hour]
    avg_pts_by_hour.append([hour, average])

#for row in sorted(avg_pts_by_hour):
#    print("The average points in hour: {} is {:.2f}".format(row[0], row[1]))


# In[12]:


swap_avg_pts_by_hour = []
for row in avg_pts_by_hour:
    swap_avg_pts_by_hour.append([row[1], row[0]])

#print(swap_avg_pts_by_hour)


# In[13]:


# Use the sorted() function to sort swap_avg_by_hour in descending order. 
sorted_pts_swap = sorted(swap_avg_pts_by_hour, reverse=True)

print("Top 5 Hours for Show Posts Points")
for row in sorted_pts_swap[:6]:
    date = dt.datetime.strptime(row[1], "%H")
    time = date.strftime("%H:%M")
    print("{}: {:.2f} average points per post".format(time, row[0]))


# There is no match between the points of `show_posts` and the comments in `ask_posts` in a given hour, meaning that when one it maximum the other is not.
