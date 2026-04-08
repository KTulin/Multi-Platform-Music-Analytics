# Multi-Platform-Music-Analytics
This project compares how music performs across platforms using audio features and engagement metrics. It includes data analysis and an interactive Streamlit dashboard to help identify where a track is likely to perform better.

<img width="1305" height="589" alt="Screenshot 2026-04-08 at 11 29 19 AM" src="https://github.com/user-attachments/assets/1a5caa56-1b9b-4be4-9c2e-31465fda7fac" />
The main graph in the Performance Insights tab is a scatter plot that compares how each track performs across Spotify and YouTube. The horizontal axis represents Spotify streams, while the vertical axis shows YouTube views, allowing you to see how a song balances its presence between the two platforms. Because music data can vary massively between tracks, both axes use a logarithmic scale, making it easier to visualize small and extremely large values together without distortion.

Each point on the graph represents a single track, and its size reflects overall popularity based on stream count—the larger the point, the bigger the track. The color indicates which platform the track performs best on, helping you quickly identify whether a song is more Spotify-driven or YouTube-driven.

By looking at where points cluster, you can spot patterns: tracks in the top-right area are strong performers on both platforms, while those leaning more toward one axis suggest platform-specific success. Overall, the graph is designed to give a quick, intuitive understanding of reach, balance, and standout hits across platforms.

<img width="1312" height="612" alt="Screenshot 2026-04-08 at 11 29 38 AM" src="https://github.com/user-attachments/assets/14533887-b5d5-4d0a-b55c-9ff7adcf6124" />


The second tab, Engagement Lab, focuses on understanding how actively audiences interact with music rather than just how many people view it. Instead of raw reach, it highlights engagement rate, which is calculated from likes and comments relative to total views. This helps distinguish between passive listening and genuine fan interest.

The main visualization is a horizontal bar chart that ranks either artists or tracks based on their average engagement rate. When viewing all artists, it compares overall fan interaction levels across different artists. When a specific artist is selected, it breaks this down further to show which of their tracks generate the most audience response. The color intensity reinforces this, with higher engagement appearing more prominent, making standout performers immediately visible.

Alongside the chart, a leaderboard presents the top tracks with the highest engagement, giving a clearer, report-style summary of the strongest performers. Together, these elements help identify what content resonates most with listeners, separating songs that simply gain views from those that actually build an active and loyal audience.




#HOW TO RUN
1. clone the repository:
   
