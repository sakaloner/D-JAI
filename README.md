![djai demo](demo.gif)

# DJAI

This project explores the use of Large Language Models (LLMs) to enhance interactions with software. The core idea is to utilize the capability of LMs to associate words with each other and create queries for specific moods/situations.

As a proof of concept, a system has been developed that leverages LLMs to provide music playlist recommendations using natural language processing. For instance, you can ask the system to create a playlist suitable for studying for a math test. The LM analyzes this input and generates relevant tags. A vector database then groups the songs occupying the nearest cosine similarity space based on these tags and it outputs the best matching songs to the playlist query.

The strength of the recommendation system lies in its foundation of tagging songs and playlists. This makes it easier to match user queries with suitable music recommendations.

In addition to this, the project includes functions for controlling a music player (specifically, mplayer) allowing for the searching and downloading of music from YouTube and searching songs from the local filesystem.

