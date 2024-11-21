class Task:
    def __init__(self, createdByUid, createdByName, assignedToUid, assignedToName, description):
        self.createdByUid = createdByUid 
        self.createdByName = createdByName 
        self.assignedToUid = assignedToUid 
        self.assignedToName = assignedToName 
        self.description = description 
        self.done = False