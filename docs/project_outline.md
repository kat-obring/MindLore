# The goal 
The overall goal of the project is to build a content creation assistant. 
I want to be able to add ideas for content through a UI, and see a list of those ideas. 
Then I'd like to pick one of the ideas, and send it to chatGPT to develop a few angles for social media content, following style guides that I will provide in .md files. 
ChatGPT should send back 3 options for the user to choose from. These options should be displayed in the UI, where the user can choose one to send back to chatGPT, where it gets developed into into a full piece of social media content. The user can choose if the content should be optimised for a blog post, a Linkedin post, Bluesky or an email for my mailing list. 
The user then should have the option to edit the text directly in the UI. 

This can be a multiple step workflow. 

The project should have git pipeline, and tests should be run on every merge request. Merging will not be allowed until all tests pass. 
The application should be packaged in a docker container, so it's easy to deploy to share it with others. 
A DB should be used to store the content. 
