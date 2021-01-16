Througout my four years as a CS major at UB, the most widely used platform for out-of-class interactions was Piazza.  It allows for you to asks questions or make announcements visible to the enitre class, or limit the visibility of your post to just teaching staff.   If you have a question that pertains to some personal situation/scenario, a private post might be the better choice.  If you missed class and would like to request the notes from one of your peers, a public post would increase the likelihood of recieving a response.

Piazza is often home to extremely helpful and engaging discussions between peers and teachers, especially when there's a project deadline close approaching.  But when the discussions escalate beyond something that can be resolved over a text-based communication service, and would require features such as audio, video, and screen-sharing, there is a very noticeable break in the work flow.  It's often a cumbersum process for to users coordinate which conferencing platform they're going to use and how they're going to send the invitations to eachother.

Brada solves this issue by creating a discussion forum that operates over Webex Teams, so when users are in the mood for a familiar UI that has all the basic features they've grown relaint on accessible to them, they can use the Brada web application.  But when it comes time  for them to require a full web conferencing system, they're just a click of a button away from joining a Webex Room with their TA's.   Since all users conversations have been moving by way of the webex api, their rooms, teams, and conversation history will all be visible from any Webex Teams client.

So how does this address our problem?  By supplying professors and teachers with the core tools that they are already used to using, improving them, and integrating those tools with Webex, we're cultivating a natural pathway from the Brada web app to the Webex Teams clients that would hopefully end with users recognizing the full power of Webex Teams and using it as their primary mode of communication.  

I think what's glaringly obvious is that most of Brada's features are pretty redundant, as in they can already be accomplished using the Webex Teams client.  But that's really the point I'm trying to make with this project.  Webex is already a product far superior to Zoom not just in terms of security, but reliability as well.    It has all the same features, and a far more expansive and powerful API.   But I believe that people need to grow more comfortable using it, and applications like Brada which narrow down the scope of the problem that webex is addressing and the space it's operating in, and again integrating ith with UI's that are already familiar to users, can really help facilitate that.


Current Features:

Admin: 
-Create an organization (which can represent a class or section)

-Import a list of students to your organization from a csv or excel file following the schema (Firstname,Lastname,Email)
-Import a list of teaching assistants to your organization from a csv or excel file following the schema (Firstname,Lastname,Email)

Student:

-Send private messages to just the teaching staff

-Brodacast messages to the entire class

Staff:

-Send private messages to any student in the class

-Broadcast messages to the entire class

-Broadcast messages to just the teaching staff.

Future Developments:

-utilize Bulk Actions to decrease the latency associated with API requests

-add in a button that opens the conversation in the webex teams client

-add in a button that launches a meeting with the participants of the current room

-many bug fixes

-many UI upgrades (such as differentiating between staff and students on the messages pannel of brada)

-allowing for attachments and markup

-possibly integrating a real time code editor.
