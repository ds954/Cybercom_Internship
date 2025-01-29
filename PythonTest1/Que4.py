# You are analyzing sports teams. Members of each team are stored in a list. The Coach is the first name in the list, the captain is the second name in the list, and other players are listed after that. These lists are stored in another list, which starts with the best team and proceeds through the list to the worst team last. Create a funtion to select the captain of the worst team.
lst1=["coach1","caption1","p1_1","p1_2"]
lst2=["coach2","caption2","p2_1","p2_2"]
lst3=["coach3","caption3","p3_1","p3_2"]
data=[lst1,
      lst2,
      lst3]

def select_worst_caption():
    print(data[-1][1])
select_worst_caption()
