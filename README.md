# class-scheduler
This project explores test driven development to implement a program that helps users schedule classes by taking inputs of when the class should be, day and times, 
and some specifications on the features the users would like for the classroom to find a room for the class.
The main data structure in this program is a 2-3 balance tree.

# Specification
Utilize Black Box testing to design and implement a classroom recommender and scheduler program, taking in inputs from the users and returning suitable classrooms for a class to be scheduled in.

# Hierarchy Design
![uml](https://github.com/ployniti/class-scheduler/assets/145937137/2bc39184-12fc-4131-b5fd-c6acc12df1a0)

I started off with designing my hierarchy of rooms. 
Each unique classroom type is derived from a base classroom class that has the basic specifications of the rooms such as the room number, occupancy, and features such as whether the room is 
zoom enabled and whether the room has a whiteboard. The three different classroom types are `Lab`, `Lecturehall`, and `Seminar`. All three room types have at least one unique data member from one another. 
For example, a Lab object would have a computer number member and a Seminar object would have a boolean data whether there is a round table in the room, fitting for a discussion based class. 

Following the design of our hierarchy, I implemented some tests for the hierarchy using `Pytest` prior to its implementation. 

To create somewhat of a database of an array of linear linked lists of available rooms, I leveraged the random library to generate a random set of available rooms that the users can search from with each run of the program.

# Run Instructions
Run `python main.py` in terminal.
