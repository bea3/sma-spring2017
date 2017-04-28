import matplotlib.pyplot as plt
import numpy as np

# data to plot
n_groups = 11
rt_count = (90, 55, 40, 65, 90, 55, 40, 65, 90, 55, 40)
fave_count = (85, 62, 54, 20, 90, 55, 40, 65, 90, 55, 40)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, rt_count, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Retweet Count')

rects2 = plt.bar(index + bar_width, fave_count, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Favorite Count')

plt.xlabel('Tracked URLs')
plt.ylabel('Count')
plt.title('Retweet Count and Favorite Count by Tracked URL')
plt.xticks(index + bar_width,
           ('RBoKNShF4R',
            'SEO4CUuzjq',
            'O0xVQdZDkw',
            'ENPlJ9KnZc',
            'dhMehoWjdi',
            'BIgjUQMqYu',
            'MDsxTHHA1V',
            'C8HrSJjeFw',
            'd7OGHbmu71',
            '6kE6GvulfI',
            '5BjokX7HQ5'))
plt.legend()

plt.tight_layout()
plt.show()
