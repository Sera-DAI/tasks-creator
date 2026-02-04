from dataclasses import dataclass

@dataclass
class Task:
    id: id
    title: title
    description: description
    completed: completed=False
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }
        